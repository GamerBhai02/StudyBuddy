from google import genai
from app.config.settings import settings
import json
import re

class AIService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-2.5-pro"  # Using latest Gemini 2.5 Pro
    
    async def extract_topics(self, text: str, subject: str) -> list:
        """Extract topics from text using Gemini 2.5 Pro"""
        
        system_instruction = """
        You are an expert at analyzing academic content and extracting study topics.
        Analyze the provided text and extract all distinct topics.
        Assign each topic an importance weight from 1-10 based on frequency, emphasis, and apparent significance.
        Return ONLY valid JSON in this exact format:
        {"topics": [{"name": "Topic Name", "weight": 8}, {"name": "Another Topic", "weight": 6}]}
        
        Do not include any markdown formatting, code blocks, or additional text.
        """
        
        prompt = f"""
        Subject: {subject}
        
        Content to analyze:
        {text[:4000]}  # Limit to first 4000 chars to avoid token limits
        
        Extract all major topics and subtopics with their importance weights (1-10).
        Return only the JSON object, no additional text or formatting.
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "system_instruction": system_instruction,
                    "temperature": 0.3,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )
            
            content = response.text.strip()
            
            # Clean up response - remove markdown code blocks if present
            # Remove any leading ``` or ```<lang> and remove any trailing ```
            content = re.sub(r'^```(?:\w+)?\s*', '', content)
            content = re.sub(r'\s*```$', '', content)
            content = content.strip()
            
            result = json.loads(content)
            return result.get("topics", [])
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response content: {content}")
            # Fallback to basic topic extraction
            return [
                {"name": "Introduction", "weight": 5},
                {"name": "Core Concepts", "weight": 8},
                {"name": "Advanced Topics", "weight": 7}
            ]
        except Exception as e:
            print(f"Gemini API error: {e}")
            return [
                {"name": "Introduction", "weight": 5},
                {"name": "Core Concepts", "weight": 8},
                {"name": "Advanced Topics", "weight": 7}
            ]
    
    async def generate_lesson_content(self, topic_name: str, subject: str) -> dict:
        """Generate lesson content for a topic using Gemini 2.5 Pro"""
        
        system_instruction = """
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
        
        Do not include any markdown formatting, code blocks, or additional text.
        """
        
        prompt = f"Create a comprehensive lesson for: {topic_name} in {subject}"
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "system_instruction": system_instruction,
                    "temperature": 0.5,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )
            
            content = response.text.strip()
            
            # Clean up response - remove markdown code blocks if present
            # Normalize removal of opening triple backticks (including optional language) and closing backticks
            content = re.sub(r'^```(?:\w+)?\s*', '', content)
            content = re.sub(r'\s*```$', '', content)
            content = content.strip()
            
            return json.loads(content)
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response content: {content}")
            return {
                "explanation": f"This is an introduction to {topic_name} in {subject}. This topic covers fundamental concepts that are essential for understanding the broader subject area.",
                "key_points": [
                    f"Core concept 1 of {topic_name}",
                    f"Core concept 2 of {topic_name}",
                    f"Key principle related to {topic_name}"
                ],
                "example": f"Example application of {topic_name} will be demonstrated here.",
                "common_mistakes": [
                    "Common error to avoid when studying this topic",
                    "Another frequent misconception"
                ]
            }
        except Exception as e:
            print(f"Gemini API error: {e}")
            return {
                "explanation": f"This is an introduction to {topic_name}.",
                "key_points": ["Core concept 1", "Core concept 2"],
                "example": "Example will be generated",
                "common_mistakes": ["Common error to avoid"]
            }
    
    async def generate_streaming_content(self, prompt: str):
        """Generate streaming response from Gemini (optional for real-time responses)"""
        try:
            response = self.client.models.generate_content_stream(
                model=self.model,
                contents=prompt,
                config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_output_tokens": 2048,
                }
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            print(f"Streaming error: {e}")
            yield "Error generating streaming response"
    
    async def analyze_study_materials(self, text: str, material_type: str) -> dict:
        """Analyze uploaded study materials and provide insights"""
        
        system_instruction = f"""
        You are analyzing {material_type} for a student.
        Provide insights about:
        1. Main themes covered
        2. Difficulty level (Easy/Medium/Hard)
        3. Estimated study time needed (in hours)
        4. Key areas of focus
        
        Return JSON format:
        {{
            "themes": ["theme1", "theme2"],
            "difficulty": "Medium",
            "estimated_hours": 10,
            "focus_areas": ["area1", "area2"]
        }}
        """
        
        prompt = f"Analyze this {material_type}:\n\n{text[:3000]}"
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "system_instruction": system_instruction,
                    "temperature": 0.3,
                    "max_output_tokens": 1024,
                }
            )
            
            content = response.text.strip()
            # Remove any leading ``` or ```<lang> and remove any trailing ```
            content = re.sub(r'^```(?:\w+)?\s*', '', content)
            content = re.sub(r'\s*```$', '', content)
            content = content.strip()
            
            return json.loads(content)
            
        except Exception as e:
            print(f"Analysis error: {e}")
            return {
                "themes": ["General topics"],
                "difficulty": "Medium",
                "estimated_hours": 8,
                "focus_areas": ["Core concepts"]
            }
