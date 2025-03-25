from django.conf import settings

class FlutterAwareCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if getattr(request, 'is_flutter', False):
            # اعمال تنظیمات CORS مخصوص Flutter
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = ', '.join(
                settings.CORS_FLUTTER_SETTINGS['ALLOWED_METHODS']
            )
            response['Access-Control-Allow-Headers'] = ', '.join(
                settings.CORS_FLUTTER_SETTINGS['ALLOWED_HEADERS']
            )
            response['Access-Control-Max-Age'] = str(
                settings.CORS_FLUTTER_SETTINGS['MAX_AGE']
            )
            
        return response