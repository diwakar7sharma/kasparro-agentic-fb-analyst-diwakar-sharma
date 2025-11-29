import os
from src.utils.llm_client import LLMClient

class InsightAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.prompt_path = "prompts/insight_agent.txt"

    def _load_prompt(self, data_context: str, user_query: str) -> str:
        if not os.path.exists(self.prompt_path):
            raise FileNotFoundError(f"Prompt file not found at {self.prompt_path}")
            
        with open(self.prompt_path, "r") as f:
            template = f.read()
            
        return template.replace("{data_context}", data_context).replace("{user_query}", user_query)

    def generate_insight(self, data_context: str, query: str):
        """
        data_context: A string summary of data (e.g., "Spend: $500, ROAS: 1.2")
        query: The specific question (e.g., "Why is ROAS low?")
        """
        print(f"💡 Insight Agent thinking about: '{query}'...")
        
        prompt = self._load_prompt(data_context, query)
        response = self.llm.generate(prompt)
        
        return response

# Test Block
if __name__ == "__main__":
    agent = InsightAgent()
    
    # 1. Simulate some data coming from the Data Agent
    dummy_data = """
    Campaign: Winter_Sale
    - Spend increased by 50% yesterday.
    - CPC increased from $1.00 to $2.50.
    - CTR dropped from 2.0% to 0.8%.
    - ROAS dropped from 3.0 to 1.1.
    """
    
    # 2. Ask for an insight
    query = "Why did performance tank yesterday?"
    insight = agent.generate_insight(dummy_data, query)
    
    print("\n📝 ANALYSIS:")
    print(insight)