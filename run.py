import json
import os
from src.agents.planner import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.creative_agent import CreativeAgent

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
            print(f"📊 Data Result: {result[:200]}...") # Print preview
            
        # Route to Insight Agent
        elif "Insight Agent" in step:
            result = insight_agent.generate_insight(context, step)
            context += f"\n\n[ANALYSIS]:\n{result}"
            final_insights.append(result)
            print(f"💡 Insight: {result[:200]}...")
            
        # Route to Creative Agent
        elif "Creative Agent" in step:
            result = creative_agent.generate_copy(context, step)
            final_creatives.append(result)
            print(f"🎨 Creative Generated: {len(result.get('variations', []))} variations")

    # 5. Generate Final Report
    print("\n📝 Generating Final Report...")
    
    report_content = f"# Facebook Ads Performance Report\n\n## 1. Executive Summary\n{user_query}\n\n"
    
    report_content += "## 2. Key Insights\n"
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