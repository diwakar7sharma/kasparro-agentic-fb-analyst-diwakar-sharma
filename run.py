import json
import os
from src.agents.planner import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.creative_agent import CreativeAgent
from src.agents.evaluator_agent import EvaluatorAgent

def save_to_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)
    print(f"📁 Saved output to {filename}")

def main():
    print("🤖 Kasparro Agentic Analyst Starting...")
    
    # 1. Initialize Agents
    planner = PlannerAgent()
    data_agent = DataAgent()
    insight_agent = InsightAgent()
    creative_agent = CreativeAgent()
    evaluator_agent = EvaluatorAgent() # <--- NEW: Initialized Evaluator

    # 2. Define the Big Question
    user_query = "Analyze the decline in ROAS over the last 30 days and suggest new creatives."
    print(f"\n🎯 Goal: {user_query}")

    # 3. Generate Plan
    plan = planner.create_plan(user_query)
    print("\n📋 Plan of Action:")
    for i, step in enumerate(plan["steps"]):
        print(f"  {i+1}. {step}")

    # 4. Execute Steps
    context = "Initial Query: " + user_query
    final_insights = []
    final_creatives = []

    print("\n🚀 Executing Plan...")
    
    for step in plan["steps"]:
        print(f"\n--- Executing: {step} ---")
        
        # Route to Data Agent
        if "Data Agent" in step:
            result = data_agent.analyze(step)
            context += f"\n\n[DATA FINDINGS]:\n{result}"
            print(f"📊 Data Result: {result[:200]}...") 
            
        # Route to Insight Agent (WITH VALIDATION)
        elif "Insight Agent" in step:
            # 1. Generate Insight
            raw_insight = insight_agent.generate_insight(context, step)
            print(f"💡 Raw Insight Generated: {raw_insight[:100]}...")
            
            # 2. Validate it!
            evaluation = evaluator_agent.evaluate(context, raw_insight)
            
            if evaluation["confidence_score"] > 70:
                print(f"✅ Insight Validated (Score: {evaluation['confidence_score']})")
                context += f"\n\n[VALIDATED INSIGHT]:\n{raw_insight}"
                final_insights.append(raw_insight)
            else:
                print(f"❌ Insight Rejected (Score: {evaluation['confidence_score']}): {evaluation['reasoning']}")
                # Note: Rejected insights are NOT added to context or final_insights
            
        # Route to Creative Agent
        elif "Creative Agent" in step:
            result = creative_agent.generate_copy(context, step)
            final_creatives.append(result)
            print(f"🎨 Creative Generated: {len(result.get('variations', []))} variations")

    # 5. Generate Final Report
    print("\n📝 Generating Final Report...")
    
    report_content = f"# Facebook Ads Performance Report\n\n## 1. Executive Summary\n{user_query}\n\n"
    
    report_content += "## 2. Key Insights (Validated)\n"
    if not final_insights:
        report_content += "No insights met the confidence threshold.\n"
    else:
        for insight in final_insights:
            report_content += f"{insight}\n\n"
        
    report_content += "## 3. Recommended Creatives\n"
    for creative_batch in final_creatives:
        for ad in creative_batch.get("variations", []):
            report_content += f"### {ad.get('headline')}\n"
            report_content += f"**Copy:** {ad.get('primary_text')}\n"
            report_content += f"**Why:** {ad.get('reasoning')}\n\n"

    # Save files
    save_to_file("report.md", report_content)
    save_to_file("insights.json", json.dumps(final_insights, indent=2))
    save_to_file("creatives.json", json.dumps(final_creatives, indent=2))

    print("\n✅ Mission Complete! Check report.md for the results.")

if __name__ == "__main__":
    main()