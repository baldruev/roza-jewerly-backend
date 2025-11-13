"""
Custom Language Middleware.
Extracts language from Accept-Language header and sets it for the request.
"""
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class LanguageMiddleware(MiddlewareMixin):
    """
    Middleware to handle multi-language requests.
    Follows Single Responsibility Principle (SOLID).
    """
    
    def process_request(self, request):
        """
        Process incoming request and set language from Accept-Language header.
        Falls back to default language if header is not present.
        """
        language = self._get_language_from_request(request)
        
        # Validate language is supported
        supported_languages = [lang[0] for lang in settings.LANGUAGES]
        if language not in supported_languages:
            language = settings.LANGUAGE_CODE
        
        # Set language for this request
        translation.activate(language)
        request.LANGUAGE_CODE = language
    
    def process_response(self, request, response):
        """
        Add Content-Language header to response.
        """
        if hasattr(request, 'LANGUAGE_CODE'):
            response['Content-Language'] = request.LANGUAGE_CODE
        return response
    
    @staticmethod
    def _get_language_from_request(request):
        """
        Extract language from Accept-Language header.
        Returns default language if not found.
        """
        # Check for explicit language parameter first
        lang_param = request.GET.get('lang') or request.POST.get('lang')
        if lang_param:
            return lang_param.lower()
        
        # Check Accept-Language header
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        if accept_language:
            # Parse Accept-Language header (e.g., "en-US,en;q=0.9,de;q=0.8")
            languages = []
            for item in accept_language.split(','):
                lang = item.split(';')[0].strip().lower()
                # Handle language codes like 'en-US' -> 'en'
                if '-' in lang:
                    lang = lang.split('-')[0]
                languages.append(lang)
            
            if languages:
                return languages[0]
        
        # Fallback to default
        return settings.LANGUAGE_CODE