import os
import google.generativeai as genai
from dotenv import load_dotenv
import yaml

# Load environment variables
load_dotenv()

class LLMClient:
    def __init__(self):
        # Load config to get model name
        with open("config/config.yaml", "r") as f:
            self.config = yaml.safe_load(f)
            
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in .env file")

        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model_name = self.config["llm"]["model"]
        self.model = genai.GenerativeModel(self.model_name)

    def generate(self, prompt: str) -> str:
        """Sends a prompt to Gemini and returns the text response."""
        try:
            # Set generation config
            generation_config = genai.types.GenerationConfig(
                temperature=self.config["llm"]["temperature"],
                max_output_tokens=self.config["llm"]["max_tokens"]
            )

            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            return response.text
            
        except Exception as e:
            print(f"❌ Error calling Gemini: {e}")
            return ""