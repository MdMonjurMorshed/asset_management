# your_project/middleware.py

from django.core.cache import cache
from django.http import HttpResponseForbidden,JsonResponse
from rest_framework.response import Response
from rest_framework import status

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of API endpoints that should be rate-limited
        rate_limited_endpoints = ['/get-all','change-pass']

        # Check if the current endpoint should be rate-limited
        if request.path in rate_limited_endpoints:
            # Apply rate limiting logic for specific endpoints
            return self.apply_rate_limit(request)

        # For other endpoints, proceed without rate limiting
        response = self.get_response(request)
        return response

    def apply_rate_limit(self, request):
        # Your rate limiting logic here
        # ...

        # Example: Rate limiting logic for demonstration
        user_identifier = "unknown_user"
        user=request.user
        rate_limit=5 if user.is_authenticated else 2
        # print("user id is:",user.email)
        if user.is_authenticated:
            user_identifier = str(user.id)
            



        user_cache_key = f"user:{user_identifier}"
        user_requests_key = f"user_requests:{user_identifier}"

        if not cache.get(user_cache_key):
            cache.set(user_cache_key, True, timeout=60)  
            cache.set(user_requests_key, 0, timeout=60)

        user_requests = cache.get(user_requests_key)
        if user_requests >= rate_limit:
            time_counter=cache.ttl(user_cache_key)
            return JsonResponse({"message":f"Too many requests, please try after {time_counter} seconds"},status=429)

        cache.incr(user_requests_key)

        response = self.get_response(request)
        return response
