import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the 'src' directory to the path so we can import the agents
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import your agent (Adjust the import if your class name is different)
from agents.evaluator_agent import EvaluatorAgent

class TestEvaluatorAgent(unittest.TestCase):

    def setUp(self):
        """Set up the agent before each test."""
        self.agent = EvaluatorAgent()

    @patch('agents.evaluator_agent.EvaluatorAgent.call_llm') # MOCK the LLM call
    def test_evaluate_valid_insight(self, mock_llm):
        """Test that a strong insight gets a high confidence score."""
        
        # 1. Simulate the LLM returning a "Good" JSON response
        mock_llm.return_value = """
        {
            "confidence_score": 85,
            "reasoning": "The insight is supported by the data showing a 20% drop."
        }
        """

        # 2. Define inputs
        context = "ROAS dropped by 20% last week."
        insight = "The drop in ROAS is due to creative fatigue."

        # 3. Run the method
        result = self.agent.evaluate(context, insight)

        # 4. Assertions (Check if code handles the JSON correctly)
        self.assertGreater(result['confidence_score'], 70)
        self.assertEqual(result['confidence_score'], 85)
        print("\n✅ Test High Confidence: Passed")

    @patch('agents.evaluator_agent.EvaluatorAgent.call_llm') # MOCK the LLM call
    def test_evaluate_weak_insight(self, mock_llm):
        """Test that a weak insight gets a low confidence score."""
        
        # 1. Simulate the LLM returning a "Bad" JSON response
        mock_llm.return_value = """
        {
            "confidence_score": 40,
            "reasoning": "This hypothesis is vague and lacks data proof."
        }
        """

        context = "ROAS is stable."
        insight = "Maybe the weather affected it?"

        result = self.agent.evaluate(context, insight)

        self.assertLess(result['confidence_score'], 70)
        self.assertEqual(result['confidence_score'], 40)
        print("\n✅ Test Low Confidence: Passed")

if __name__ == '__main__':
    unittest.main()