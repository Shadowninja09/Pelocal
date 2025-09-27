"""
Custom middleware for exception handling and logging
"""
import logging
import traceback
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class ExceptionHandlingMiddleware(MiddlewareMixin):
    """Middleware to handle exceptions and provide consistent error responses"""
    
    def process_exception(self, request, exception):
        """Process exceptions and return appropriate responses"""
        logger.error(f"Unhandled exception: {str(exception)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Check if it's an API request
        if request.path.startswith('/api/'):
            return JsonResponse({
                'status': 'error',
                'message': 'Internal server error',
                'error': 'INTERNAL_ERROR'
            }, status=500)
        
        # For non-API requests, let Django handle the exception
        return None

class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware to log all requests"""
    
    def process_request(self, request):
        """Log incoming requests"""
        logger.info(f"Request: {request.method} {request.path} from {request.META.get('REMOTE_ADDR', 'unknown')}")
        
        # Log request body for POST/PUT requests (excluding sensitive data)
        if request.method in ['POST', 'PUT', 'PATCH'] and request.path.startswith('/api/'):
            try:
                body = request.body.decode('utf-8')
                # Don't log if it contains sensitive information
                if 'password' not in body.lower() and 'token' not in body.lower():
                    logger.debug(f"Request body: {body[:500]}...")  # Limit to 500 chars
            except Exception:
                logger.debug("Could not decode request body")
    
    def process_response(self, request, response):
        """Log outgoing responses"""
        logger.info(f"Response: {response.status_code} for {request.method} {request.path}")
        return response
