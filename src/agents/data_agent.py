import pandas as pd
import os
import yaml
from src.utils.llm_client import LLMClient

class DataAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.config = self._load_config()
        self.df = self._load_data()
        self.prompt_path = "prompts/data_agent.txt"

    def _load_config(self):
        with open("config/config.yaml", "r") as f:
            return yaml.safe_load(f)

    def _load_data(self):
        """Loads the CSV data once when the agent starts."""
        path = self.config["data"]["filepath"]
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ Data file not found at: {path}")
        print(f"📊 Data Agent loaded {path}")
        return pd.read_csv(path)

    def analyze(self, query: str):
        """
        1. Asks LLM for Python code to solve the query.
        2. Executes the code on the dataframe.
        3. Returns the result.
        """
        # 1. Prepare Prompt
        with open(self.prompt_path, "r") as f:
            template = f.read()
        prompt = template.replace("{user_query}", query)

        # 2. Get Code from LLM
        print(f"    👉 Data Agent analyzing: '{query}'")
        code_response = self.llm.generate(prompt)
        
        # Clean up code (remove markdown ` ```python ... ``` `)
        clean_code = code_response.replace("```python", "").replace("```", "").strip()

        # 3. Execute Code safely
        # We create a local scope with 'df' available
        local_scope = {"df": self.df, "pd": pd, "result": None}
        
        try:
            exec(clean_code, {}, local_scope)
            result = local_scope.get("result")
            return str(result)
        except Exception as e:
            return f"Error executing data analysis: {str(e)}"

# Test Block
if __name__ == "__main__":
    agent = DataAgent()
    
    # Test 1: Simple Aggregation
    print("\n--- Test 1: Total Spend ---")
    response = agent.analyze("What is the total spend across all campaigns?")
    print(f"Result: {response}")

    # Test 2: Complex Calculation
    print("\n--- Test 2: Best Campaign by ROAS ---")
    response = agent.analyze("Which campaign_name had the highest average ROAS?")
    print(f"Result: {response}")