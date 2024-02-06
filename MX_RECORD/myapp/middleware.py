from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

class DisableClientSideCachingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @method_decorator(never_cache, name='dispatch')
    def __call__(self, request):
        response = self.get_response(request)
        if request.resolver_match is not None and request.resolver_match.url_name == 'logout':
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response
