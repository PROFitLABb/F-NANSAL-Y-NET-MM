import os
import json
from groq import Groq
import streamlit as st

SYSTEM_PROMPT = """
You are an expert personal finance assistant specialized in analyzing expense descriptions and providing actionable financial advice.
Your task is to extract structured information from natural language expense descriptions and provide detailed insights.

EXPENSE CATEGORIES (Use Turkish names):
1. Yemek & İçecek (restaurants, cafes, groceries, food delivery)
2. Ulaşım (fuel, public transport, taxi, car maintenance)
3. Alışveriş (clothing, electronics, household items)
4. Eğlence (movies, concerts, games, subscriptions)
5. Konut (rent, utilities, maintenance)
6. Sağlık (medications, doctor visits, insurance)
7. Eğitim (courses, books, tuition)
8. Kişisel Bakım (haircut, cosmetics, gym)
9. Seyahat (flights, hotels, vacation expenses)
10. Diğer (other expenses)

INSTRUCTIONS:
1. Extract ALL expenses mentioned in the text with accurate categorization
2. For each expense, identify:
   - Category (use Turkish category names from the list above)
   - Amount (numeric value)
   - Description (in Turkish, brief but clear summary)
   - Date (if mentioned, format as YYYY-MM-DD)
   - Tags (in Turkish, relevant keywords like "temel", "lüks", "tekrarlayan", "tek seferlik")

3. SUMMARY (in Turkish): Provide a comprehensive 2-3 sentence summary that includes:
   - Total spending amount
   - Main spending categories
   - Spending pattern observation

4. SUGGESTIONS (in Turkish): Provide 4-6 SPECIFIC and ACTIONABLE saving tips based on the actual expenses

OUTPUT FORMAT (JSON):
{
  "expenses": [
    {
      "category": "Turkish category name",
      "amount": float,
      "description": "Turkish description",
      "date": "string (optional)",
      "tags": ["Turkish tag", ...]
    }
  ],
  "summary": "Detailed 2-3 sentence summary in Turkish",
  "suggestions": [
    "Specific actionable tip 1 in Turkish",
    "Specific actionable tip 2 in Turkish",
    "..."
  ]
}

IMPORTANT:
- Return ONLY valid JSON, no additional text or markdown
- ALL text content must be in TURKISH
"""

def analyze_expense_with_ai(expense_text: str) -> dict:
    """Analyze expense text using Groq AI"""
    try:
        api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
        
        if not api_key:
            return {
                "error": "GROQ_API_KEY bulunamadı. Lütfen Streamlit secrets'a ekleyin.",
                "expenses": [],
                "summary": "API anahtarı eksik",
                "suggestions": ["Streamlit Cloud'da Settings → Secrets bölümünden GROQ_API_KEY ekleyin"]
            }
        
        client = Groq(api_key=api_key)
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Analyze this expense text: {expense_text}"}
        ]
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        response_text = completion.choices[0].message.content
        
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(response_text)
        return result
        
    except json.JSONDecodeError as e:
        return {
            "error": f"AI yanıtı JSON formatında değil: {str(e)}",
            "expenses": [],
            "summary": "Analiz başarısız",
            "suggestions": ["Lütfen tekrar deneyin"]
        }
    except Exception as e:
        return {
            "error": f"Hata: {str(e)}",
            "expenses": [],
            "summary": "Analiz başarısız",
            "suggestions": ["Lütfen tekrar deneyin"]
        }
