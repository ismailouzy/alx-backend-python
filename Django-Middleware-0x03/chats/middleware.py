from django.http import HttpResponseForbidden
from collections import defaultdict
from datetime import datetime, time
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        
        # Write to file
        with open('requests.log', 'a') as f:
            f.write(log_message + '\n')
            
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start_time = time(21, 0)  # 9 PM
        end_time = time(18, 0)    # 6 PM
        
        # Check if current time is between 9 PM and 6 AM (next day)
        if (current_time >= start_time) or (current_time <= end_time):
            return HttpResponseForbidden("Chat access is restricted between 9 PM and 6 AM")
            
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_counts = defaultdict(list)
        self.limit = 5  # 5 messages
        self.time_window = 60  # 60 seconds

    def __call__(self, request):
        if request.method == 'POST':
            ip = request.META.get('REMOTE_ADDR')
            current_time = time.time()
            
            # Remove old timestamps
            self.message_counts[ip] = [
                t for t in self.message_counts[ip] 
                if current_time - t < self.time_window
            ]
            
            # Check if limit exceeded
            if len(self.message_counts[ip]) >= self.limit:
                return HttpResponseForbidden("Message rate limit exceeded. Please wait before sending more messages.")
            
            # Add current timestamp
            self.message_counts[ip].append(current_time)
            
        return self.get_response(request)


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Paths that require admin/mod permissions
        restricted_paths = ['/admin/', '/moderate/']  # Add your restricted paths
        
        if any(request.path.startswith(path) for path in restricted_paths):
            user = request.user
            if not (user.is_authenticated and (user.is_staff or user.is_superuser)):
                return HttpResponseForbidden("You don't have permission to access this resource")
                
        return self.get_response(request)
