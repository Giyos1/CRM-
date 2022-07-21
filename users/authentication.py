from rest_framework.authentication import SessionAuthentication, BaseAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return
