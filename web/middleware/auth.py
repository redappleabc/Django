from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    def process_request(self, request):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')

        if not request.user.is_authenticated:
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL)

        elif path == settings.LOGOUT_URL.lstrip("/"):
            try:
                del request.session[settings.AUTH_TOKEN]
            except KeyError:
                print("already deleted or no exist")
            logout(request)