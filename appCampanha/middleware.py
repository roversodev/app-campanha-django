from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger('user')

class LogUnauthorizedAccessMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 403:
            user = request.user
            url = request.path
            extra = {
                'user_id': user.id,
                'username': user.username,
                'ip_address': request.META.get('REMOTE_ADDR'),
            }
            logger.warning('TENTOU ACESSAR %s SEM PERMISSÃO/ACESSO NEGADO', url, extra=extra)
        if response.status_code == 404:
            user = request.user
            url = request.path
            extra = {
                'user_id': user.id if user != 'Anônimo' else None,
                'username': user.username if user != 'Anônimo' else 'Anônimo',
                'ip_address': request.META.get('REMOTE_ADDR'),
            }
            logger.warning('TENTOU ACESSAR %s URL QUE NÃO EXISTE', url, extra=extra)
        return response
