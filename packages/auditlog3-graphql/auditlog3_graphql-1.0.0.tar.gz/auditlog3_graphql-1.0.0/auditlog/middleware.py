from __future__ import unicode_literals

import threading
import time

from django.conf import settings
from django.db.models.signals import pre_save
from auditlog.utils import curry
from django.apps import apps
from auditlog.models import LogEntry
from auditlog.compat import is_authenticated
from django.conf import settings
from django.contrib import auth
from graphql_jwt.utils import jwt_decode
import jwt

# Use MiddlewareMixin when present (Django >= 1.10)
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


threadlocal = threading.local()


class AuditlogMiddleware(MiddlewareMixin):
    """
    Middleware to couple the request's user to log items. This is accomplished by currying the signal receiver with the
    user from the request (or None if the user is not authenticated).
    """

    def process_request(self, request):
        """
        Gets the current user from the request and prepares and connects a signal receiver with the user already
        attached to it.
        """
        self._check_authenticated_user(request)
        # Initialize thread local storage
        threadlocal.auditlog = {
            'signal_duid': (self.__class__, time.time()),
            'remote_addr': request.META.get('REMOTE_ADDR'),
        }

        # In case of proxy, set 'original' address
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            threadlocal.auditlog['remote_addr'] = request.META.get(
                'HTTP_X_FORWARDED_FOR').split(',')[0]

        # Connect signal for automatic logging
        if hasattr(request, 'user') and is_authenticated(request.user):
            set_actor = curry(self.set_actor, user=request.user,
                              signal_duid=threadlocal.auditlog['signal_duid'])
            pre_save.connect(set_actor, sender=LogEntry,
                             dispatch_uid=threadlocal.auditlog['signal_duid'], weak=False)

    def process_response(self, request, response):
        """
        Disconnects the signal receiver to prevent it from staying active.
        """
        if hasattr(threadlocal, 'auditlog'):
            pre_save.disconnect(
                sender=LogEntry, dispatch_uid=threadlocal.auditlog['signal_duid'])

        return response

    def process_exception(self, request, exception):
        """
        Disconnects the signal receiver to prevent it from staying active in case of an exception.
        """
        if hasattr(threadlocal, 'auditlog'):
            pre_save.disconnect(
                sender=LogEntry, dispatch_uid=threadlocal.auditlog['signal_duid'])

        return None

    @staticmethod
    def set_actor(user, sender, instance, signal_duid, **kwargs):
        """
        Signal receiver with an extra, required 'user' kwarg. This method becomes a real (valid) signal receiver when
        it is curried with the actor.
        """
        if hasattr(threadlocal, 'auditlog'):
            if signal_duid != threadlocal.auditlog['signal_duid']:
                return
            try:
                app_label, model_name = settings.AUTH_USER_MODEL.split('.')
                auth_user_model = apps.get_model(app_label, model_name)
            except ValueError:
                auth_user_model = apps.get_model('auth', 'user')
            if sender == LogEntry and isinstance(user, auth_user_model) and instance.actor is None:
                instance.actor = user

            instance.remote_addr = threadlocal.auditlog['remote_addr']

    def _check_authenticated_user(self, request):
        if not request.user.is_authenticated:
            self._authenticate_graphql(request)

    def _authenticate_graphql(self, request):
        token_header_key = getattr(
            settings, 'AUDITLOG_GRAPHQL_TOKEN_KEY', 'HTTP_AUTHORIZATION')
        token = request.META.get(token_header_key, None)
        if token is not None:
            try:
                token = token.strip()
                if token:
                    token = token.replace("JWT ", "")
                    decoded_token = jwt_decode(token)
                    if 'email' in decoded_token:
                        email = decoded_token.get('email', None)
                        user = auth.authenticate(request, remote_user=email)
                        if user:
                            # set request.user and persist user in the session
                            # by logging the user in.
                            request.user = user
                            auth.login(request, user)
            except jwt.ExpiredSignatureError:
                # Signature has expired
                pass
            except jwt.exceptions.DecodeError:
                # Invalid JWT token
                pass
