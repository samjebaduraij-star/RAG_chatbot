# rate_limiter.py
# Description: Rate limiting utility for API calls
# Dependencies: time, logging
# Author: AI Generated Code
# Created: August 31, 2025

import time
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta

class RateLimiter:
    """Simple rate limiter for API calls."""
    
    def __init__(self, max_requests: int = 15, time_window: int = 60):
        """Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed in time window
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self.logger = logging.getLogger(__name__)
    
    def can_make_request(self) -> bool:
        """Check if a request can be made within rate limits.
        
        Returns:
            True if request is allowed, False otherwise
        """
        now = time.time()
        
        # Remove old requests outside time window
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time < self.time_window]
        
        # Check if we're under the limit
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        
        return False
    
    def time_until_next_request(self) -> Optional[int]:
        """Get seconds until next request is allowed.
        
        Returns:
            Seconds to wait, or None if request can be made now
        """
        if self.can_make_request():
            # Remove the request we just added for checking
            self.requests.pop()
            return None
        
        if not self.requests:
            return None
        
        # Time until oldest request expires
        oldest_request = min(self.requests)
        wait_time = int(self.time_window - (time.time() - oldest_request))
        return max(0, wait_time)
    
    def get_status(self) -> Dict[str, any]:
        """Get current rate limiter status.
        
        Returns:
            Dictionary with current status
        """
        now = time.time()
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time < self.time_window]
        
        return {
            "requests_made": len(self.requests),
            "max_requests": self.max_requests,
            "time_window": self.time_window,
            "requests_remaining": self.max_requests - len(self.requests),
            "can_make_request": len(self.requests) < self.max_requests
        }
