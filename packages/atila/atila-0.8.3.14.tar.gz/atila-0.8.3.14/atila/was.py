import os, sys
import time
from hmac import new as hmac
from hashlib import sha1, sha256, md5
import base64
import pickle
import random
from rs4 import jwt
from aquests.protocols.http import http_date
from skitai import wsgiappservice
from skitai.corequest import tasks
import skitai
from skitai.exceptions import HTTPError
import uuid

def otp (serial):
    serial = int (md5 (str (serial).encode ()).hexdigest ()[-8:], 16)
    return md5 (str (round (time.time () - serial, -1)).encode ()).hexdigest ()

class WAS (wsgiappservice.WAS):
    # mehiods remap ------------------------------------------------
    def __getattr__ (self, name):
        if self.in__dict__ ("app"): # atila app
            attr = self.app.create_on_demand (self, name)
            if attr:
                setattr (self, name, attr)
                return attr

        try:
            return self.objects [name]
        except KeyError:
            raise AttributeError ("'was' hasn't attribute '%s'" % name)

    # URL builders -------------------------------------------------
    def urlfor (self, thing, *args, **karg):
        # override with resource default args
        if not isinstance (thing, str) or thing.startswith ("/") or thing.find (":") == -1:
            return self.app.urlfor (thing, *args, **karg)
        return self.apps.build_url (thing, *args, **karg)
    ab = urlfor

    def urlpatch (self, thing, **karg):
        # override with current args
        defaults = self.request.PARAMS
        defaults.update (self.request.URL)
        karg ["__defaults__"] = defaults
        return self.urlfor (thing, **karg)
    partial = urlpatch

    def baseurl (self, thing):
        # resource path info without parameters
        return self.urlfor (thing, __resource_path_only__ = True)
    basepath = baseurl

    def urlspec (self, thing):
        # resource path info without parameters
        return self.urlfor (thing, __resource_spec_only__ = True)

    # event -------------------------------------------------
    def broadcast (self, event, *args, **kargs):
        return self.apps.bus.emit (event, self, *args, **kargs)
    emit = broadcast

    # passowrd en/decrypt -----------------------------------
    def encrypt_password (self, password):
        salt = base64.b64encode(os.urandom (16))
        dig = hmac (password.encode (), salt, sha256).digest()
        signature = base64.b64encode (dig)
        return salt.decode (), signature.decode ()

    def verify_password (self, password, salt, signature):
        dig = hmac (password.encode (), salt.encode (), sha256).digest()
        signature_ = base64.b64encode (dig).decode ()
        return signature == signature_

    def make_uid (self, s = None):
        if s is None:
            s = str (uuid.uuid4 ())
        return base64.encodebytes (md5 (s.encode ()).digest ()) [:-3].decode ().replace ('/', '-').replace ('+', '.')

    # JWT token --------------------------------------------------
    def mkjwt (self, claim, salt = None, alg = "HS256"):
        assert "exp" in claim, "exp claim required"
        return jwt.gen_token (salt or self.app.salt, claim, alg)

    def dejwt (self, token = None, salt = None):
        return self.request.dejwt (token, salt or self.app.salt)

    # otp ---------------------------------------------------
    def otp (self, serial):
        return otp (serial)

    def validate_otp (self, opt, serial):
        now = time.time ()
        serial = int (md5 (str (serial).encode ()).hexdigest ()[-8:], 16)
        if opt == md5 (str (round (now - serial, -1)).encode ()).hexdigest ():
            return True
        if opt == md5 (str (round (now + 10 - serial, -1)).encode ()).hexdigest ():
            return True
        if opt == md5 (str (round (now - 10 - serial, -1)).encode ()).hexdigest ():
            return True
        return False

    # onetime token  ----------------------------------------
    def _unserialize_token (self, string):
        def adjust_padding (s):
            paddings = 4 - (len (s) % 4)
            if paddings != 4:
                s += ("=" * paddings)
            return s

        string = string.replace (" ", "+")
        try:
            base64_hash, data = string.split('?', 1)
        except ValueError:
            return
        client_hash = base64.b64decode(adjust_padding (base64_hash))
        data = base64.b64decode(adjust_padding (data))
        mac = hmac (self.app.salt, None, sha1)
        mac.update (data)
        if client_hash != mac.digest():
            return
        return pickle.loads (data)

    def mkott (self, obj, timeout = 1200, session_key = None):
        wrapper = {
            'object': obj,
            'timeout': time.time () + timeout
        }
        if session_key:
            token = hex (random.getrandbits (64))
            tokey = '_{}_token'.format (session_key)
            wrapper ['_session_token'] = (tokey, token)
            self.session.mount (session_key, session_timeout = timeout)
            self.session [tokey] = token
            self.session.mount ()

        data = pickle.dumps (wrapper, 1)
        mac = hmac (self.app.salt, None, sha1)
        mac.update (data)
        return (base64.b64encode (mac.digest()).strip().rstrip (b'=') + b"?" + base64.b64encode (data).strip ().rstrip (b'=')).decode ("utf8")

    def deott (self, string):
        wrapper = self._unserialize_token (string)
        if not wrapper:
            return

        # validation with session
        tokey = None
        has_error = False
        if wrapper ['timeout']  < time.time ():
            has_error = True
        if not has_error:
            session_token = wrapper.get ('_session_token')
            if session_token:
                # verify with session
                tokey, token = session_token
                self.session.mount (tokey [1:-6])
                if token != self.session.get (tokey):
                    has_error = True
        if has_error:
            if tokey:
                del self.session [tokey]
                self.session.mount ()
            return
        elif tokey:
            self.session.mount ()

        obj = wrapper ['object']
        return obj

    def rvott (self, string):
        # revoke token
        wrapper = self._unserialize_token (string)
        session_token = wrapper.get ('_session_token')
        if not session_token:
            return
        tokey, token = session_token
        self.session.mount (tokey [1:-6])

        if not self.session.get (tokey):
            self.session.mount ()
            return
        del self.session [tokey]
        self.session.expire ()
        self.session.mount ()

    mktoken = token = mkott
    rmtoken = rvott
    detoken = deott

    # CSRF token ------------------------------------------------------
    CSRF_NAME = "XSRF_TOKEN" #axios compat
    @property
    def csrf_token (self):
        if self.CSRF_NAME not in self.cookie:
            if self.app.debug:
                tok = '3649c350861db268'
            else:
                tok = hex (random.getrandbits (64)) [2:]
            self.cookie [self.CSRF_NAME] = tok
        return self.cookie [self.CSRF_NAME]

    @property
    def csrf_token_input (self):
        return '<input type="hidden" name="{}" value="{}">'.format (self.CSRF_NAME, self.csrf_token)

    def remove_csrf (self):
        try:
            del self.cookie [self.CSRF_NAME]
        except KeyError:
            pass

    def verify_csrf (self, keep = True):
        token = self.request.get_header ('X-{}'.format (self.CSRF_NAME.replace ("_", "-")), self.request.args.get (self.CSRF_NAME))
        if not token:
            return False
        if self.csrf_token == token:
            if not keep:
                del self.cookie [self.CSRF_NAME]
            return True
        return False
    csrf_verify = verify_csrf

    # response shortcuts -----------------------------------------------
    REDIRECT_TEMPLATE =  (
        "<html><head><title>%s</title></head>"
        "<body><h1>%s</h1>"
        "This document may be found "
        '<a HREF="%s">here</a></body></html>'
    )
    def redirect (self, url, status = "302 Object Moved", body = None, headers = None):
        redirect_headers = [
            ("Location", url),
            ("Cache-Control", "max-age=0"),
            ("Expires", http_date.build_http_date (time.time ()))
        ]
        if type (headers) is list:
            redirect_headers += headers
        if not body:
            body = self.REDIRECT_TEMPLATE % (status, status, url)
        return self.response (status, body, redirect_headers)

    def render (self, template_file, _do_not_use_this_variable_name_ = {}, **karg):
        return self.app.render (self, template_file, _do_not_use_this_variable_name_, **karg)

    def render_or_API (self, template_file, _do_not_use_this_variable_name_ = {}, **karg):
        if self.request.acceptable ('application/json'):
            return self.API (None, _do_not_use_this_variable_name_, **karg)
        return self.render (template_file, _do_not_use_this_variable_name_ = {}, **karg)

    def API (self, *args, **karg):
        api = self.response.API (*args, **karg)
        try: api.set_json_encoder (self.app.config.get ("JSON_ENCODER"))
        except AttributeError: pass
        return api

    def Fault (self, *args, **karg):
        fault = self.response.Fault (*args, **karg)
        try: fault.set_json_encoder (self.app.config.get ("JSON_ENCODER"))
        except AttributeError: pass
        return fault

    @property
    def Error (self):
        return HTTPError

    def File (self, *args, **karg):
        return self.response.File (*args, **karg)

    def Static (self, *args, **karg):
        return self.response.Static (*args, **karg)

    def proxypass (self, alias, path, timeout = 3):
        def respond (was, rs):
            resp = rs.dispatch ()
            resp.reraise ()
            [was.response.update (k, v) for k, v in resp.headers.items () if k not in ("Content-Length",)]
            return was.response (
                "{} {}".format (resp.status_code, resp.reason),
                resp.content
            )
        headers = dict ([(k, v) for k, v in self.request.headers.items ()])
        headers ["Accept"] = "*/*"
        return self.get ("{}/{}".format (alias, path), headers = headers, timeout = timeout).then (respond)
    ProxyPass = proxypass
