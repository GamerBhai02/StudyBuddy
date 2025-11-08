from google import genai
from app.config.settings import settings
import json
import re
from typing import List, Dict
from app.models.models import Question, MCQOption, WrittenAnswer, Topic
from sqlalchemy.orm import Session

class QuestionService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-2.5-pro-preview-03-25"
    
    def _clean_json_response(self, content: str) -> str:
        """Remove markdown formatting"""
        if not content:
            return "{}"
        # remove any triple-backtick fences (``` or longer) left in the model output
        content = re.sub(r'`{3,}', '', content)
        return content.strip()
    
    async def generate_mcqs(
        self, 
        topic: Topic, 
        difficulty: str, 
        count: int = 10,
        db: Session = None
    ) -> List[Question]:
        """Generate MCQ questions for a topic"""
        
        system_instruction = """
        You are an expert exam question generator.
        Generate multiple-choice questions that test student understanding.
        
        Requirements:
        - 4 options (A, B, C, D)
        - Only 1 correct answer
        - Plausible distractors (wrong options)
        - Clear, unambiguous wording
        - Mix of conceptual and application questions
        
        Return ONLY valid JSON in this format:
        {
          "questions": [
            {
              "question": "Question text here?",
              "options": [
                {"label": "A", "text": "Option A", "is_correct": false},
                {"label": "B", "text": "Option B", "is_correct": true},
                {"label": "C", "text": "Option C", "is_correct": false},
                {"label": "D", "text": "Option D", "is_correct": false}
              ],
              "explanation": "Why B is correct..."
            }
          ]
        }
        """
        
        prompt = f"""
        Generate {count} multiple-choice questions for:
        Topic: {topic.name}
        Subject: {topic.study_plan.subject}
        Difficulty: {difficulty}
        
        Focus on testing understanding of key concepts.
        Difficulty guide:
        - Easy: Direct recall, basic definitions
        - Medium: Application of concepts, multi-step reasoning
        - Hard: Complex problem solving, analysis, synthesis
        
        Return {count} questions as JSON.
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "system_instruction": system_instruction,
                    "temperature": 0.7,
                    "max_output_tokens": 3000,
                }
            )
            
            if not response or not response.text:
                print("Warning: Empty response from Gemini")
                return []
            
            content = self._clean_json_response(response.text)
            result = json.loads(content)
            questions_data = result.get("questions", [])
            
            # Save to database
            saved_questions = []
            for q_data in questions_data:
                question = Question(
                    topic_id=topic.id,
                    question_type="mcq",
                    difficulty=difficulty,
                    question_text=q_data["question"],
                    marks=1,
                    time_limit=60
                )
                db.add(question)
                db.flush()
                
                # Add options
                for opt in q_data["options"]:
                    option = MCQOption(
                        question_id=question.id,
                        option_label=opt["label"],
                        option_text=opt["text"],
                        is_correct=opt["is_correct"],
                        explanation=q_data.get("explanation") if opt["is_correct"] else None
                    )
                    db.add(option)
                
                saved_questions.append(question)
            
            db.commit()
            print(f"✓ Generated {len(saved_questions)} MCQs for {topic.name}")
            return saved_questions
            
        except Exception as e:
            print(f"Error generating MCQs: {e}")
            return []
    
    async def generate_written_questions(
        self,
        topic: Topic,
        difficulty: str,
        count: int = 5,
        db: Session = None
    ) -> List[Question]:
        """Generate written questions with model answers"""
        
        system_instruction = """
        You are an expert exam question creator.
        Generate exam-style written questions with detailed model answers.
        
        Return ONLY valid JSON:
        {
          "questions": [
            {
              "question": "Question text",
              "marks": 10,
              "time_minutes": 12,
              "model_answer": {
                "introduction": "Brief intro...",
                "main_body": "Detailed explanation...",
                "conclusion": "Summary..."
              },
              "marking_scheme": {
                "introduction": 2,
                "main_body": 6,
                "conclusion": 2
              },
              "keywords": [
                {"word": "key concept", "importance": "high"},
                {"word": "supporting idea", "importance": "medium"}
              ],
              "expected_length": "200-250 words"
            }
          ]
        }
        """
        
        marks_by_difficulty = {
            "easy": 5,
            "medium": 10,
            "hard": 15
        }
        
        prompt = f"""
        Generate {count} written exam questions for:
        Topic: {topic.name}
        Subject: {topic.study_plan.subject}
        Difficulty: {difficulty}
        Marks: {marks_by_difficulty.get(difficulty, 10)}
        
        Question types:
        - Explain/Describe (conceptual understanding)
        - Analyze/Compare (critical thinking)
        - Apply/Solve (problem solving)
        
        Each question should have:
        - Clear marking scheme
        - Model answer with structure
        - Keywords for evaluation
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "system_instruction": system_instruction,
                    "temperature": 0.6,
                    "max_output_tokens": 4000,
                }
            )
            
            if not response or not response.text:
                return []
            
            content = self._clean_json_response(response.text)
            result = json.loads(content)
            questions_data = result.get("questions", [])
            
            saved_questions = []
            for q_data in questions_data:
                question = Question(
                    topic_id=topic.id,
                    question_type="written",
                    difficulty=difficulty,
                    question_text=q_data["question"],
                    marks=q_data.get("marks", 10),
                    time_limit=q_data.get("time_minutes", 15) * 60
                )
                db.add(question)
                db.flush()
                
                # Combine model answer parts
                model_answer_parts = q_data.get("model_answer", {})
                full_answer = f"{model_answer_parts.get('introduction', '')}\n\n{model_answer_parts.get('main_body', '')}\n\n{model_answer_parts.get('conclusion', '')}"
                
                written_answer = WrittenAnswer(
                    question_id=question.id,
                    model_answer=full_answer,
                    marking_scheme=q_data.get("marking_scheme", {}),
                    keywords=q_data.get("keywords", []),
                    expected_length=q_data.get("expected_length", "200-300 words")
                )
                db.add(written_answer)
                saved_questions.append(question)
            
            db.commit()
            print(f"✓ Generated {len(saved_questions)} written questions for {topic.name}")
            return saved_questions
            
        except Exception as e:
            print(f"Error generating written questions: {e}")
            return []
    
    async def evaluate_written_answer(
        self,
        question: Question,
        student_answer: str,
        model_answer: str,
        marking_scheme: Dict,
        keywords: List[Dict]
    ) -> Dict:
        """Evaluate student's written answer using AI"""
        
        system_instruction = """
        You are an expert exam evaluator.
        Grade the student's answer based on the model answer and marking scheme.
        
        Return JSON:
        {
          "score": 7.5,
          "max_score": 10,
          "feedback": "Your answer covered...",
          "strengths": ["point 1", "point 2"],
          "improvements": ["missing concept X", "expand on Y"],
          "keyword_coverage": 6,
          "keyword_total": 10
        }
        """
        
        prompt = f"""
        Grade this answer:
        
        Question: {question.question_text}
        Marks: {question.marks}
        
        Model Answer:
        {model_answer}
        
        Marking Scheme:
        {json.dumps(marking_scheme, indent=2)}
        
        Keywords to check:
        {json.dumps(keywords, indent=2)}
        
        Student's Answer:
        {student_answer}
        
        Provide detailed evaluation.
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "system_instruction": system_instruction,
                    "temperature": 0.3,
                }
            )
            
            if not response or not response.text:
                return {"score": 0, "feedback": "Could not evaluate"}
            
            content = self._clean_json_response(response.text)
            return json.loads(content)
            
        except Exception as e:
            print(f"Error evaluating answer: {e}")
            return {"score": 0, "feedback": "Evaluation failed"}
