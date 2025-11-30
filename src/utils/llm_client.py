import os
import google.generativeai as genai
from dotenv import load_dotenv
import yaml
from src.utils.logger import setup_logger

# Load environment variables
load_dotenv()

class LLMClient:
    def __init__(self):
        # Setup Logger
        self.logger = setup_logger()

        # Load config
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
        """Sends a prompt to Gemini and logs the interaction."""
        try:
            # Set generation config
            generation_config = genai.types.GenerationConfig(
                temperature=self.config["llm"]["temperature"],
                max_output_tokens=self.config["llm"]["max_tokens"]
            )

            # Log the Input
            self.logger.info(f"🔵 INPUT PROMPT:\n{prompt[:500]}...") # Log first 500 chars to avoid clutter

            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            result_text = response.text

            # Log the Output
            self.logger.info(f"🟢 MODEL RESPONSE:\n{result_text}")

            return result_text
            
        except Exception as e:
            error_msg = f"❌ Error calling Gemini: {e}"
            print(error_msg)
            self.logger.error(error_msg)
            return ""