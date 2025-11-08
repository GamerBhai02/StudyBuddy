from openai import OpenAI
from app.config.settings import settings
import json

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def extract_topics(self, text: str, subject: str) -> list:
        """Extract topics from text using GPT-4"""
        system_prompt = """
        You are an expert at analyzing academic content and extracting study topics.
        Analyze the provided text and extract all distinct topics.
        Assign each topic an importance weight from 1-10 based on frequency, emphasis, and apparent significance.
        Return ONLY valid JSON in this exact format:
        {"topics": [{"name": "Topic Name", "weight": 8}, {"name": "Another Topic", "weight": 6}]}
        """
        
        user_prompt = f"""
        Subject: {subject}
        
        Content to analyze:
        {text[:4000]}  # Limit to first 4000 chars to avoid token limits
        
        Extract all major topics and subtopics with their importance weights.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            return result.get("topics", [])
        except Exception as e:
            # Fallback to basic topic extraction
            return [
                {"name": "Introduction", "weight": 5},
                {"name": "Core Concepts", "weight": 8},
                {"name": "Advanced Topics", "weight": 7}
            ]
    
    async def generate_lesson_content(self, topic_name: str, subject: str) -> dict:
        """Generate lesson content for a topic"""
        system_prompt = """
        You are an expert educator creating concise, clear study materials.
        Create a structured lesson with:
        1. Brief concept explanation (3-4 sentences)
        2. 2-3 key formulas, definitions, or principles
        3. One worked example
        4. Common mistakes to avoid
        
        Return ONLY valid JSON in this format:
        {
            "explanation": "...",
            "key_points": ["point 1", "point 2", "point 3"],
            "example": "...",
            "common_mistakes": ["mistake 1", "mistake 2"]
        }
        """
        
        user_prompt = f"Create a lesson for: {topic_name} in {subject}"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            return {
                "explanation": f"This is an introduction to {topic_name}.",
                "key_points": ["Core concept 1", "Core concept 2"],
                "example": "Example will be generated",
                "common_mistakes": ["Common error to avoid"]
            }
