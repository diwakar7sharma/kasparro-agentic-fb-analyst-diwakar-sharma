import os
import json
from src.utils.llm_client import LLMClient

class EvaluatorAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.prompt_path = "prompts/evaluator.txt"

    def _load_prompt(self, data_context: str, hypothesis: str) -> str:
        if not os.path.exists(self.prompt_path):
            raise FileNotFoundError(f"Prompt file not found at {self.prompt_path}")
            
        with open(self.prompt_path, "r") as f:
            template = f.read()
            
        return template.replace("{data_context}", data_context).replace("{hypothesis}", hypothesis)

    def evaluate(self, data_context: str, hypothesis: str):
        print(f"⚖️ Evaluator is judging the insight...")
        
        prompt = self._load_prompt(data_context, hypothesis)
        response = self.llm.generate(prompt)
        
        cleaned = response.replace("```json", "").replace("```", "").strip()
        
        try:
            return json.loads(cleaned)
        except:
            return {
                "is_valid": False, 
                "confidence_score": 0, 
                "reasoning": "Failed to parse validation output."
            }

if __name__ == "__main__":
    # Test
    agent = EvaluatorAgent()
    data = "Spend: $500, ROAS: 1.2, CTR: 0.5%"
    hypo = "ROAS is low because CTR is very high."
    print(agent.evaluate(data, hypo))