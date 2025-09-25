"""
Rate limiting to prevent abuse and DoS attacks
"""

from collections import defaultdict, deque
from typing import Dict, Optional
import time


class RateLimiter:
    """Rate limiting implementation"""

    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, deque] = defaultdict(deque)

    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed for identifier"""
        current_time = time.time()
        user_requests = self.requests[identifier]

        # Remove old requests outside the window
        while user_requests and user_requests[0] <= current_time - self.window_seconds:
            user_requests.popleft()

        # Check if under limit
        if len(user_requests) < self.max_requests:
            user_requests.append(current_time)
            return True

        return False

    def get_remaining_requests(self, identifier: str) -> int:
        """Get remaining requests for identifier"""
        current_time = time.time()
        user_requests = self.requests[identifier]

        # Remove old requests
        while user_requests and user_requests[0] <= current_time - self.window_seconds:
            user_requests.popleft()

        return max(0, self.max_requests - len(user_requests))

    def get_reset_time(self, identifier: str) -> Optional[float]:
        """Get time when rate limit resets"""
        user_requests = self.requests[identifier]
        if not user_requests:
            return None

        return user_requests[0] + self.window_seconds


# Global rate limiter instances
api_limiter = RateLimiter(max_requests=60, window_seconds=60)  # 60 requests per minute
form_limiter = RateLimiter(
    max_requests=10, window_seconds=60
)  # 10 form submissions per minute
