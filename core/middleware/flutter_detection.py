from django.http import JsonResponse

class FlutterRequestMiddleware:
    FLUTTER_AGENTS = ['Dart/3.6', 'Flutter']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        request.is_flutter = any(agent in user_agent for agent in self.FLUTTER_AGENTS)
        

        return self.get_response(request)