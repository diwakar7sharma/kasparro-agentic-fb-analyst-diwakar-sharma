import os
import json
from src.utils.llm_client import LLMClient

class PlannerAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.prompt_path = "prompts/planner.txt"

    def _load_prompt(self, user_query: str) -> str:
        if not os.path.exists(self.prompt_path):
            raise FileNotFoundError(f"Prompt file not found at {self.prompt_path}") 
        with open(self.prompt_path, "r") as f:
            template = f.read()
        return template.replace("{user_query}", user_query)

    def create_plan(self, user_query: str):
        print(f"🧠 Planner is thinking about: '{user_query}'...")
        prompt = self._load_prompt(user_query)
        response = self.llm.generate(prompt)
        
        # Cleanup JSON
        cleaned = response.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(cleaned)
        except:
            return {"steps": [cleaned]}

if __name__ == "__main__":
    agent = PlannerAgent()
    print(agent.create_plan("Why is my ROAS down?"))