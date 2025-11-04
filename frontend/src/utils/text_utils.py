# text_utils.py
# Description: Text processing and manipulation utilities
# Dependencies: re, typing, unicodedata
# Author: AI Generated Code
# Created: August 12, 2025

import re
import logging
import unicodedata
from typing import List, Set, Dict, Any
import string

class TextUtils:
    """Utility class for text processing operations."""
    
    def __init__(self):
        """Initialize text utilities."""
        self.logger = logging.getLogger(__name__)
        
        # Compile regex patterns for better performance
        self.whitespace_pattern = re.compile(r'\s+')
        self.sentence_pattern = re.compile(r'(?<=[.!?])\s+')
        self.word_pattern = re.compile(r'\b\w+\b')
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        
        # Stop words for text processing
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'were', 'will', 'with', 'the', 'this', 'but', 'they',
            'have', 'had', 'what', 'said', 'each', 'which', 'their', 'time',
            'if', 'up', 'out', 'many', 'then', 'them', 'these', 'so', 'some',
            'her', 'would', 'make', 'like', 'into', 'him', 'has', 'two',
            'more', 'very', 'what', 'know', 'just', 'first', 'get', 'over',
            'think', 'also', 'your', 'work', 'life', 'only', 'can', 'still',
            'should', 'after', 'being', 'now', 'made', 'before', 'here',
            'through', 'when', 'where', 'how', 'all', 'much', 'well', 'way',
            'down', 'may', 'new', 'want', 'even', 'give', 'most', 'good',
            'long', 'own', 'under', 'never', 'day', 'same', 'another', 'know',
            'while', 'come', 'could', 'there', 'see', 'back', 'call', 'came',
            'each', 'need', 'take', 'year', 'find', 'right', 'look', 'end',
            'why', 'again', 'turn', 'every', 'start', 'might', 'move'
        }
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content.
        
        Args:
            text: Raw text to clean
        
        Returns:
            Cleaned text string
        """
        try:
            if not text:
                return ""
            
            # Normalize unicode characters
            text = unicodedata.normalize('NFKD', text)
            
            # Remove control characters
            text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C')
            
            # Fix common encoding issues
            text = text.replace('\ufeff', '')  # Remove BOM
            text = text.replace('\u2019', "'")  # Smart apostrophe
            text = text.replace('\u2018', "'")  # Smart apostrophe
            text = text.replace('\u201c', '"')  # Smart quote
            text = text.replace('\u201d', '"')  # Smart quote
            text = text.replace('\u2013', '-')  # En dash
            text = text.replace('\u2014', '--')  # Em dash
            
            # Normalize whitespace
            text = self.whitespace_pattern.sub(' ', text)
            
            # Remove excessive line breaks
            text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
            
            # Trim whitespace
            text = text.strip()
            
            return text
            
        except Exception as e:
            self.logger.error(f"Text cleaning error: {e}")
            return text if text else ""
    
    def split_sentences(self, text: str) -> List[str]:
        """Split text into sentences.
        
        Args:
            text: Text to split
        
        Returns:
            List of sentences
        """
        try:
            if not text:
                return []
            
            # Clean text first
            text = self.clean_text(text)
            
            # Split on sentence boundaries
            sentences = self.sentence_pattern.split(text)
            
            # Clean and filter sentences
            cleaned_sentences = []
            for sentence in sentences:
                sentence = sentence.strip()
                
                # Filter out very short sentences
                if len(sentence) > 10:
                    cleaned_sentences.append(sentence)
            
            return cleaned_sentences
            
        except Exception as e:
            self.logger.error(f"Sentence splitting error: {e}")
            return [text] if text else []
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """Extract keywords from text.
        
        Args:
            text: Text to extract keywords from
            max_keywords: Maximum number of keywords to return
        
        Returns:
            List of keywords
        """
        try:
            if not text:
                return []
            
            # Clean text
            text = self.clean_text(text.lower())
            
            # Extract words
            words = self.word_pattern.findall(text)
            
            # Filter stop words and short words
            keywords = []
            for word in words:
                if (len(word) > 3 and 
                    word not in self.stop_words and 
                    not word.isdigit()):
                    keywords.append(word)
            
            # Count word frequency
            word_freq = {}
            for word in keywords:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Sort by frequency and return top keywords
            sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            
            return [word for word, freq in sorted_keywords[:max_keywords]]
            
        except Exception as e:
            self.logger.error(f"Keyword extraction error: {e}")
            return []
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Similarity score between 0 and 1
        """
        try:
            if not text1 or not text2:
                return 0.0
            
            # Extract keywords from both texts
            keywords1 = set(self.extract_keywords(text1, max_keywords=20))
            keywords2 = set(self.extract_keywords(text2, max_keywords=20))
            
            if not keywords1 or not keywords2:
                return 0.0
            
            # Calculate Jaccard similarity
            intersection = len(keywords1.intersection(keywords2))
            union = len(keywords1.union(keywords2))
            
            similarity = intersection / union if union > 0 else 0.0
            
            return similarity
            
        except Exception as e:
            self.logger.error(f"Similarity calculation error: {e}")
            return 0.0
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text.
        
        Args:
            text: Text to extract entities from
        
        Returns:
            Dictionary of entity types and their values
        """
        try:
            entities = {
                "emails": [],
                "urls": [],
                "phone_numbers": [],
                "dates": [],
                "numbers": []
            }
            
            if not text:
                return entities
            
            # Extract emails
            entities["emails"] = self.email_pattern.findall(text)
            
            # Extract URLs
            entities["urls"] = self.url_pattern.findall(text)
            
            # Extract phone numbers (simple pattern)
            phone_pattern = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
            entities["phone_numbers"] = phone_pattern.findall(text)
            
            # Extract dates (simple patterns)
            date_patterns = [
                r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
                r'\d{4}-\d{1,2}-\d{1,2}',  # YYYY-MM-DD
                r'\b\w+\s+\d{1,2},?\s+\d{4}\b'  # Month DD, YYYY
            ]
            
            for pattern in date_patterns:
                entities["dates"].extend(re.findall(pattern, text))
            
            # Extract numbers
            number_pattern = re.compile(r'\b\d+(?:,\d{3})*(?:\.\d+)?\b')
            entities["numbers"] = number_pattern.findall(text)
            
            return entities
            
        except Exception as e:
            self.logger.error(f"Entity extraction error: {e}")
            return {"emails": [], "urls": [], "phone_numbers": [], "dates": [], "numbers": []}
    
    def truncate_text(self, text: str, max_length: int, add_ellipsis: bool = True) -> str:
        """Truncate text to specified length.
        
        Args:
            text: Text to truncate
            max_length: Maximum length
            add_ellipsis: Whether to add ellipsis
        
        Returns:
            Truncated text
        """
        try:
            if not text or len(text) <= max_length:
                return text
            
            if add_ellipsis and max_length > 3:
                return text[:max_length-3] + "..."
            else:
                return text[:max_length]
                
        except Exception as e:
            self.logger.error(f"Text truncation error: {e}")
            return text if text else ""
    
    def remove_html_tags(self, text: str) -> str:
        """Remove HTML tags from text.
        
        Args:
            text: Text containing HTML tags
        
        Returns:
            Text with HTML tags removed
        """
        try:
            if not text:
                return ""
            
            # Remove HTML tags
            html_pattern = re.compile(r'<[^>]+>')
            text = html_pattern.sub('', text)
            
            # Decode HTML entities
            html_entities = {
                '&amp;': '&',
                '&lt;': '<',
                '&gt;': '>',
                '&quot;': '"',
                '&#39;': "'",
                '&nbsp;': ' '
            }
            
            for entity, char in html_entities.items():
                text = text.replace(entity, char)
            
            return text
            
        except Exception as e:
            self.logger.error(f"HTML tag removal error: {e}")
            return text if text else ""
    
    def format_text_for_display(self, text: str, line_length: int = 80) -> str:
        """Format text for better display.
        
        Args:
            text: Text to format
            line_length: Maximum line length
        
        Returns:
            Formatted text
        """
        try:
            if not text:
                return ""
            
            # Clean text
            text = self.clean_text(text)
            
            # Split into paragraphs
            paragraphs = text.split('\n\n')
            formatted_paragraphs = []
            
            for paragraph in paragraphs:
                if paragraph.strip():
                    # Wrap lines
                    words = paragraph.split()
                    lines = []
                    current_line = []
                    current_length = 0
                    
                    for word in words:
                        if current_length + len(word) + 1 <= line_length:
                            current_line.append(word)
                            current_length += len(word) + 1
                        else:
                            if current_line:
                                lines.append(' '.join(current_line))
                            current_line = [word]
                            current_length = len(word)
                    
                    if current_line:
                        lines.append(' '.join(current_line))
                    
                    formatted_paragraphs.append('\n'.join(lines))
            
            return '\n\n'.join(formatted_paragraphs)
            
        except Exception as e:
            self.logger.error(f"Text formatting error: {e}")
            return text if text else ""
    
    def get_text_statistics(self, text: str) -> Dict[str, Any]:
        """Get statistics about text content.
        
        Args:
            text: Text to analyze
        
        Returns:
            Dictionary of text statistics
        """
        try:
            if not text:
                return {
                    "character_count": 0,
                    "word_count": 0,
                    "sentence_count": 0,
                    "paragraph_count": 0,
                    "avg_words_per_sentence": 0,
                    "reading_time_minutes": 0
                }
            
            # Clean text
            cleaned_text = self.clean_text(text)
            
            # Count characters
            char_count = len(cleaned_text)
            
            # Count words
            words = self.word_pattern.findall(cleaned_text)
            word_count = len(words)
            
            # Count sentences
            sentences = self.split_sentences(cleaned_text)
            sentence_count = len(sentences)
            
            # Count paragraphs
            paragraphs = [p.strip() for p in cleaned_text.split('\n\n') if p.strip()]
            paragraph_count = len(paragraphs)
            
            # Calculate averages
            avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
            
            # Estimate reading time (average 200 words per minute)
            reading_time = word_count / 200 if word_count > 0 else 0
            
            return {
                "character_count": char_count,
                "word_count": word_count,
                "sentence_count": sentence_count,
                "paragraph_count": paragraph_count,
                "avg_words_per_sentence": round(avg_words_per_sentence, 1),
                "reading_time_minutes": round(reading_time, 1)
            }
            
        except Exception as e:
            self.logger.error(f"Text statistics error: {e}")
            return {
                "character_count": 0,
                "word_count": 0,
                "sentence_count": 0,
                "paragraph_count": 0,
                "avg_words_per_sentence": 0,
                "reading_time_minutes": 0
            }