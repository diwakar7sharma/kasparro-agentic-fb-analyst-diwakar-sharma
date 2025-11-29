import os
import json
from src.utils.llm_client import LLMClient

class CreativeAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.prompt_path = "prompts/creative_agent.txt"

    def _load_prompt(self, data_context: str, user_query: str) -> str:
        if not os.path.exists(self.prompt_path):
            raise FileNotFoundError(f"Prompt file not found at {self.prompt_path}")
            
        with open(self.prompt_path, "r") as f:
            template = f.read()
            
        return template.replace("{data_context}", data_context).replace("{user_query}", user_query)

    def generate_copy(self, data_context: str, query: str):
        print(f"🎨 Creative Agent writing copy for: '{query}'...")
        
        prompt = self._load_prompt(data_context, query)
        response = self.llm.generate(prompt)
        
        # Clean JSON
        cleaned = response.replace("```json", "").replace("```", "").strip()
        
        try:
            return json.loads(cleaned)
        except:
            return {"variations": [], "raw_text": cleaned}

# Test Block
if __name__ == "__main__":
    agent = CreativeAgent()
    
    # 1. Simulate insight context
    context = """
    Product: Noise Cancelling Headphones ($200)
    Problem: Current ads have low CTR (0.5%).
    Insight: People think they are too expensive.
    Current Ad: "Buy our headphones now."
    """
    
    # 2. Ask for improvements
    query = "Write 3 new ads that justify the price by focusing on 'Peace of Mind' and 'Focus'."
    
    result = agent.generate_copy(context, query)
    print("\n✨ NEW AD VARIATIONS:")
    print(json.dumps(result, indent=2))