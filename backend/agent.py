import os
import json
from groq import Groq
from dotenv import load_dotenv

from backend.prompts import SYSTEM_PROMPT

load_dotenv()

class FinancialAgent:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key or self.groq_api_key == "your_groq_api_key_here":
            print("⚠️ WARNING: GROQ_API_KEY not configured in .env file")
            self.client = None
        else:
            self.client = Groq(api_key=self.groq_api_key)
    
    def analyze_expense(self, expense_text: str, provider: str = "groq") -> dict:
        """Analyze expense text using Groq API"""
        if not self.client:
            raise Exception("Groq API key not configured. Please add your GROQ_API_KEY to .env file")
        
        try:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Analyze this expense text: {expense_text}"}
            ]
            
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            response_text = completion.choices[0].message.content
            
            # Try to extract JSON from response
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            return json.loads(response_text)
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse AI response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")
