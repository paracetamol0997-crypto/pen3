import time
from importlib import import_module
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.cache import patch_vary_headers

class DualSessionMiddleware(SessionMiddleware):
    """
    Subclasses Django's SessionMiddleware to isolate sessions for Students and Teachers
    so that both portals can run simultaneously in different tabs of the same browser
    without session collisions or logging each other out.
    """
    def __init__(self, get_response):
        super().__init__(get_response)
        engine = import_module(settings.SESSION_ENGINE)
        self.SessionStore = engine.SessionStore

    def _get_cookie_name(self, request):
        path = request.path_info
        if path.startswith('/teacher'):
            return 'teacher_sessionid'
        elif path.startswith('/student'):
            return 'student_sessionid'
        return 'sessionid'

    def process_request(self, request):
        cookie_name = self._get_cookie_name(request)
        request._role_cookie_name = cookie_name
        session_key = request.COOKIES.get(cookie_name)
        request.session = self.SessionStore(session_key)

    def process_response(self, request, response):
        cookie_name = getattr(request, '_role_cookie_name', None) or self._get_cookie_name(request)
        session_key = request.COOKIES.get(cookie_name)

        try:
            modified = request.session.modified
            empty = request.session.is_empty()
        except AttributeError:
            return response

        if empty:
            if session_key:
                response.delete_cookie(
                    cookie_name,
                    path=settings.SESSION_COOKIE_PATH,
                    domain=settings.SESSION_COOKIE_DOMAIN,
                    samesite=settings.SESSION_COOKIE_SAMESITE,
                )
        else:
            if modified or settings.SESSION_SAVE_EVERY_REQUEST:
                if request.session.get_expire_at_browser_close():
                    max_age = None
                    expires = None
                else:
                    max_age = request.session.get_expiry_age()
                    expires_time = time.time() + max_age
                    expires = time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', time.gmtime(expires_time))

                request.session.save()
                response.set_cookie(
                    cookie_name,
                    request.session.session_key,
                    max_age=max_age,
                    expires=expires,
                    domain=settings.SESSION_COOKIE_DOMAIN,
                    path=settings.SESSION_COOKIE_PATH,
                    secure=settings.SESSION_COOKIE_SECURE or None,
                    httponly=settings.SESSION_COOKIE_HTTPONLY or None,
                    samesite=settings.SESSION_COOKIE_SAMESITE,
                )
                patch_vary_headers(response, ('Cookie',))

        return response
