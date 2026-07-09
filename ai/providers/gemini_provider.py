from google import genai
from google.genai import types
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)

class GeminiProvider:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = "gemini-3-flash-preview"

    def generate_response(self, prompt, history=None):
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="You are Yiyara, a supportive AI life coach."
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            return "I'm having trouble thinking right now."

    def generate_structured_response(self, prompt):
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini Structured Error: {e}")
            raise e
        
    def classify_intent(self, user_input):
        """
        Determines if the user wants to create a goal, ask a question, or just chat.
        """
        prompt = f"""
        Analyze the following user input and classify it into ONE of these categories:
        - DECOMPOSE: User wants to start a new goal, project, or task list.
        - QUERY: User is asking for information about their existing goals or progress.
        - CHAT: General conversation, greetings, or follow-up questions.

        Input: "{user_input}"
        
        Return ONLY the word: DECOMPOSE, QUERY, or CHAT.
        """
        try:
            # Use self.client.models.generate_content (New SDK style)
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1, # Low temperature for strict classification
                )
            )
            
            intent = response.text.strip().upper()
            
            # Clean up the response in case it returned "Category: DECOMPOSE" or similar
            for valid_intent in ['DECOMPOSE', 'QUERY', 'CHAT']:
                if valid_intent in intent:
                    return valid_intent
                    
            return 'CHAT' # Final fallback
            
        except Exception as e:
            logger.error(f"Classification Error: {e}")
            return 'CHAT' # Fallback to chat so the user isn't stuck
    