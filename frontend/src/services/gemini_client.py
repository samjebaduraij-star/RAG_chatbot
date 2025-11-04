# gemini_client.py
# Description: Google Gemini API client for AI response generation
# Dependencies: google-generativeai, logging, typing, os
# Author: AI Generated Code
# Created: August 09, 2025

import os
import logging
from typing import Dict, Any, Optional, List
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
import time
from ..utils.rate_limiter import RateLimiter

class GeminiClient:
    """Client for Google Gemini API integration."""
    
    def __init__(self):
        """Initialize Gemini API client."""
        self.logger = logging.getLogger(__name__)
        # Strip whitespace to avoid subtle env formatting issues (e.g., trailing spaces in .env)
        self.api_key = (os.getenv("GEMINI_API_KEY", "") or "").strip()
        self.model_name = (os.getenv("GEMINI_MODEL", "gemini-2.5-pro") or "gemini-2.5-pro").strip()
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Configure API
        genai.configure(api_key=self.api_key)
        
        # Initialize model
        self.model = genai.GenerativeModel(self.model_name)
        
        # Initialize rate limiter (15 requests per minute for free tier)
        self.rate_limiter = RateLimiter(max_requests=15, time_window=60)
        
        # Generation config (lower temperature to reduce randomness and enforce grounding)
        self.generation_config = {
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        # Safety settings
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    
    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=2, min=10, max=60)
    )
    def generate_response(self, prompt: str) -> Dict[str, Any]:
        """Generate response using Gemini API.
        
        Args:
            prompt: Input prompt for generation
        
        Returns:
            Response dictionary with content and metadata
        """
        try:
            # Check rate limit
            if not self.rate_limiter.can_make_request():
                wait_time = self.rate_limiter.time_until_next_request()
                return {
                    "content": f"⏳ Rate limit reached. Please wait {wait_time} seconds before making another request.",
                    "model": self.model_name,
                    "tokens": 0,
                    "confidence": 0.0,
                    "finish_reason": "rate_limited",
                    "response_time": 0.0
                }
            
            start_time = time.time()
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            # Check if response was blocked
            if response.candidates and response.candidates[0].finish_reason == "SAFETY":
                return {
                    "content": "I apologize, but I cannot provide a response to that request due to safety guidelines.",
                    "model": self.model_name,
                    "tokens": 0,
                    "confidence": 0.0,
                    "finish_reason": "safety_block",
                    "response_time": time.time() - start_time
                }
            
            # Extract response content
            content = response.text if response.text else "I apologize, but I couldn't generate a response."
            
            # Extract usage metadata
            usage_metadata = response.usage_metadata if hasattr(response, 'usage_metadata') else None
            tokens_used = usage_metadata.total_token_count if usage_metadata else 0
            
            return {
                "content": content,
                "model": self.model_name,
                "tokens": tokens_used,
                "confidence": self._calculate_confidence(response),
                "finish_reason": response.candidates[0].finish_reason if response.candidates else "unknown",
                "response_time": time.time() - start_time
            }
            
        except Exception as e:
            self.logger.error(f"Gemini API error: {e}")
            raise
    
    def _calculate_confidence(self, response) -> float:
        """Calculate confidence score for response.
        
        Args:
            response: Gemini API response object
        
        Returns:
            Confidence score between 0 and 1
        """
        try:
            if not response.candidates:
                return 0.0
            
            candidate = response.candidates[0]
            
            # Use safety ratings as confidence indicator
            if hasattr(candidate, 'safety_ratings'):
                blocked_count = sum(1 for rating in candidate.safety_ratings 
                                  if rating.blocked)
                if blocked_count > 0:
                    return 0.5  # Lower confidence if any safety blocks
            
            # Default confidence based on finish reason
            finish_reason = candidate.finish_reason
            if finish_reason == "STOP":
                return 0.9
            elif finish_reason == "MAX_TOKENS":
                return 0.7
            else:
                return 0.5
                
        except Exception:
            return 0.5
    
    def test_connection(self) -> Dict[str, Any]:
        """Test API connection and configuration.
        
        Returns:
            Test result dictionary
        """
        try:
            test_prompt = "Hello, this is a test message. Please respond with 'API connection successful.'"
            response = self.generate_response(test_prompt)
            
            return {
                "success": True,
                "model": self.model_name,
                "response": response.get("content", ""),
                "tokens": response.get("tokens", 0),
                "response_time": response.get("response_time", 0.0)
            }
            
        except Exception as e:
            self.logger.error(f"API connection test failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "model": self.model_name
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model.
        
        Returns:
            Model information dictionary
        """
        try:
            models = genai.list_models()
            current_model = None
            
            for model in models:
                if self.model_name in model.name:
                    current_model = model
                    break
            
            if current_model:
                return {
                    "name": current_model.name,
                    "display_name": current_model.display_name,
                    "description": current_model.description,
                    "input_token_limit": current_model.input_token_limit,
                    "output_token_limit": current_model.output_token_limit,
                    "supported_generation_methods": current_model.supported_generation_methods
                }
            else:
                return {
                    "name": self.model_name,
                    "status": "Model info not available"
                }
                
        except Exception as e:
            self.logger.error(f"Error getting model info: {e}")
            return {
                "name": self.model_name,
                "error": str(e)
            }