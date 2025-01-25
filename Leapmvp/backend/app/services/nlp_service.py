from transformers import pipeline
from datetime import datetime, timedelta
import spacy
from dateutil import parser
import logging

class NLPService:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.classifier = pipeline("text-classification")
        except Exception as e:
            logging.error(f"Failed to initialize NLP models: {str(e)}")
            raise

    def parse_task(self, text: str) -> dict:
        """
        Parse natural language input into structured task data
        """
        try:
            doc = self.nlp(text)
            
            task_data = {
                "title": "",
                "due_date": None,
                "priority": 0,
                "category": "general",
                "estimated_duration": 30  # default duration in minutes
            }

            # Extract date and time information
            for ent in doc.ents:
                if ent.label_ in ["DATE", "TIME"]:
                    task_data["due_date"] = self._parse_datetime(ent.text)

            # Extract task title
            task_data["title"] = self._extract_title(doc)
            task_data["priority"] = self._determine_priority(text)

            return task_data
        except Exception as e:
            logging.error(f"Error parsing task: {str(e)}")
            raise

    def _parse_datetime(self, text: str) -> datetime:
        try:
            # Handle relative dates
            relative_terms = {
                "today": datetime.now(),
                "tomorrow": datetime.now() + timedelta(days=1),
                "next week": datetime.now() + timedelta(weeks=1)
            }
            
            if text.lower() in relative_terms:
                return relative_terms[text.lower()]
            
            # Use dateutil parser for other date formats
            return parser.parse(text)
        except Exception:
            return datetime.now() + timedelta(days=1)  # Default to tomorrow

    def _extract_title(self, doc) -> str:
        # Remove date/time entities and return remaining text
        title = " ".join([token.text for token in doc 
                         if not token.ent_type_ in ["DATE", "TIME"]])
        return title.strip() or "Untitled Task"

    def _determine_priority(self, text: str) -> int:
        urgent_words = {"urgent", "asap", "important", "critical"}
        text_lower = text.lower()
        
        if any(word in text_lower for word in urgent_words):
            return 1  # High priority
        return 2  # Normal priority 