import os
import json
import google.generativeai as genai

class EvaluatorAgent:
    def __init__(self):
        # Load API key from environment
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None

    def call_llm(self, prompt):
        """
        Separate method for the actual API call. 
        This is what the test will 'mock' (intercept).
        """
        if not self.model:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        response = self.model.generate_content(prompt)
        return response.text

    def evaluate(self, context, insight):
        """
        Main method to validate an insight.
        """
        prompt = f"""
        You are a Senior Data Analyst Evaluator.
        
        CONTEXT:
        {context}
        
        HYPOTHESIS TO VALIDATE:
        {insight}
        
        TASK:
        Rate the confidence of this hypothesis (0-100) based on the context.
        If the data supports it, give a high score (>70).
        If it is vague or unsupported, give a low score (<50).
        
        OUTPUT FORMAT (JSON ONLY):
        {{
            "confidence_score": <int>,
            "reasoning": "<string>"
        }}
        """
        
        try:
            # Call the helper method (which gets mocked in tests)
            raw_response = self.call_llm(prompt)
            
            # Clean up potential markdown formatting (```json ... ```)
            cleaned_response = raw_response.replace("```json", "").replace("```", "").strip()
            
            return json.loads(cleaned_response)
            
        except Exception as e:
            # Fallback for errors
            return {
                "confidence_score": 0,
                "reasoning": f"Evaluation failed: {str(e)}"
            }