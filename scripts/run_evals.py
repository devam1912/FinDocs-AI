import os
import sys
import time
import datetime

try:
    from src.agent import run_agent
except ImportError:
    # Handle direct script executions
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.agent import run_agent

EVAL_DATASET = [
    # --- COMPUTATION (12 Questions) ---
    {
        "query": "What was my total spend in March?",
        "expected_tool": "structured_database_tool",
        "expected_values": ["2,243.83", "2243.83"],
        "is_no_answer": False,
        "category": "Computation"
    },
    {
        "query": "How much did I spend in January?",
        "expected_tool": "structured_database_tool",
        "expected_values": ["2,105.23", "2105.23"],
        "is_no_answer": False,
        "category": "Computation"
    },
    {
        "query": "What was my total spending in February 2026?",
        "expected_tool": "structured_database_tool",
        "expected_values": ["2,110.16", "2110.16"],
        "is_no_answer": False,
        "category": "Computation"
    },
    {
        "query": "What was my total spend in April?",
        "expected_tool": "structured_database_tool",
        "expected_values": ["3,272.78", "3272.78"],
        "is_no_answer": False,
        "category": "Computation"
    },
    {
        "query": "What is my total TechCorp salary from January to April?",
        "expected_tool": "structured_database_tool",
        "expected_values": ["20,000", "20000"],
        "is_no_answer": False,
        "category": "Computation"
    },
    {
        "query": "How much money did I earn from Freelance Design Client in March?",
        "expected_tool": "structured_database_tool",
        "expected_values": ["850.00", "850"],
        "is_no_answer": False,
        "category": "Computation"
    },
    {
        "query": "What was the total rent paid?",
        "expected_tool": "structured_database_tool",
        "expected_values": ["6,000", "6000"],
        "is_no_answer": False,
        "category": "Computation"
    },
    {
        "query": "How much was spent at Whole Foods Market in February?",
        "expected_tool": "structured_database_tool",
        "expected_values": ["135.20", "135.2"],
        "is_no_answer": False,
        "category": "Computation"
    },
    {
        "query": "What is the average transaction amount for Groceries?",
        "expected_tool": "structured_database_tool",
        "expected_values": ["113.88", "113.9"],
        "is_no_answer": False,
        "category": "Computation"
    },
    {
        "query": "How many transactions occurred in January?",
        "expected_tool": "structured_database_tool",
        "expected_values": ["14"],
        "is_no_answer": False,
        "category": "Computation"
    },
    {
        "query": "What was my maximum single expense amount?",
        "expected_tool": "structured_database_tool",
        "expected_values": ["1,500", "1500"],
        "is_no_answer": False,
        "category": "Computation"
    },
    {
        "query": "What is my total freelance design client income?",
        "expected_tool": "structured_database_tool",
        "expected_values": ["1,450.00", "1450"],
        "is_no_answer": False,
        "category": "Computation"
    },
    
    # --- RETRIEVAL (10 Questions) ---
    {
        "query": "Find my transactions for Netflix Subscription",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": ["Netflix", "15.49"],
        "is_no_answer": False,
        "category": "Retrieval"
    },
    {
        "query": "What gas station did I visit in January?",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": ["Shell", "42"],
        "is_no_answer": False,
        "category": "Retrieval"
    },
    {
        "query": "Who paid me salary?",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": ["TechCorp"],
        "is_no_answer": False,
        "category": "Retrieval"
    },
    {
        "query": "What company did I pay rent to?",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": ["Apex Properties", "Rent"],
        "is_no_answer": False,
        "category": "Retrieval"
    },
    {
        "query": "Find my Spotify Premium payments",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": ["Spotify", "10.99"],
        "is_no_answer": False,
        "category": "Retrieval"
    },
    {
        "query": "What did I buy at Best Buy?",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": ["Best Buy", "250"],
        "is_no_answer": False,
        "category": "Retrieval"
    },
    {
        "query": "Where did I buy groceries in March?",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": ["Whole Foods"],
        "is_no_answer": False,
        "category": "Retrieval"
    },
    {
        "query": "Find design freelance client payments",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": ["Design", "600", "850"],
        "is_no_answer": False,
        "category": "Retrieval"
    },
    {
        "query": "What did I purchase from the Apple Store?",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": ["Apple", "999"],
        "is_no_answer": False,
        "category": "Retrieval"
    },
    {
        "query": "What city utility bills did I pay in February?",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": ["Water", "45.5"],
        "is_no_answer": False,
        "category": "Retrieval"
    },
    
    # --- EDGE CASES: NO ANSWER (5 Questions) ---
    {
        "query": "How much did I spend on Tesla stock?",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": [],
        "is_no_answer": True,
        "category": "Edge Case - No Answer"
    },
    {
        "query": "Find any transactions for gym membership",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": [],
        "is_no_answer": True,
        "category": "Edge Case - No Answer"
    },
    {
        "query": "How much did I spend on Uber rides?",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": [],
        "is_no_answer": True,
        "category": "Edge Case - No Answer"
    },
    {
        "query": "What was my bonus in January?",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": [],
        "is_no_answer": True,
        "category": "Edge Case - No Answer"
    },
    {
        "query": "Show transactions for Walmart",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": [],
        "is_no_answer": True,
        "category": "Edge Case - No Answer"
    },
    
    # --- EDGE CASES: AMBIGUOUS (5 Questions) ---
    {
        "query": "What about Target?",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": ["Target", "98.50"],
        "is_no_answer": False,
        "category": "Edge Case - Ambiguous"
    },
    {
        "query": "Tell me about gas expenses",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": ["Shell", "Gas"],
        "is_no_answer": False,
        "category": "Edge Case - Ambiguous"
    },
    {
        "query": "What is salary?",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": ["TechCorp", "Salary"],
        "is_no_answer": False,
        "category": "Edge Case - Ambiguous"
    },
    {
        "query": "How much did I spend on food?",
        "expected_tool": "structured_database_tool",
        "expected_values": ["Groceries", "Dining"],
        "is_no_answer": False,
        "category": "Edge Case - Ambiguous"
    },
    {
        "query": "Show my utilities",
        "expected_tool": "semantic_retrieval_tool",
        "expected_values": ["Power", "Water", "Comcast"],
        "is_no_answer": False,
        "category": "Edge Case - Ambiguous"
    }
]

def run_evaluations() -> dict:
    print(f"Starting evaluations over {len(EVAL_DATASET)} Q&A pairs...")
    print("WARNING: Delay of 3.5 seconds applied between queries to respect Mistral API rate limits.\n")
    
    results = []
    
    correct_tool_count = 0
    correct_answer_count = 0
    hallucination_count = 0
    total_latency = 0.0
    
    for idx, item in enumerate(EVAL_DATASET):
        query = item["query"]
        expected_tool = item["expected_tool"]
        expected_values = item["expected_values"]
        is_no_answer = item["is_no_answer"]
        category = item["category"]
        
        print(f"[{idx+1}/{len(EVAL_DATASET)}] Evaluated Query: '{query}' (Cat: {category})")
        
        # Run agent
        ctx = run_agent(query)
        
        # Calculate scores
        tool_match = (ctx.tool_to_use == expected_tool)
        latency = ctx.metadata.get("total_latency", 0.0)
        total_latency += latency
        
        # Fallbacks for checking answers
        correct = True
        hallucination = False
        
        if ctx.success and ctx.final_response:
            response_lower = ctx.final_response.lower()
            
            if is_no_answer:
                # Expect denial keywords
                no_answer_keywords = ["no record", "no transaction", "not found", "unable to find", "no data", "does not show", "no payment", "not show"]
                found_denial = any(kw in response_lower for kw in no_answer_keywords)
                
                # Check for hallucinated numbers
                if not found_denial and "$" in response_lower:
                    hallucination = True
                    correct = False
                elif not found_denial:
                    correct = False
            else:
                # Check expected keywords/numbers
                for val in expected_values:
                    if val.lower() not in response_lower:
                        correct = False
                        break
        else:
            correct = False
            
        if tool_match:
            correct_tool_count += 1
        if correct:
            correct_answer_count += 1
        if hallucination:
            hallucination_count += 1
            
        results.append({
            "query": query,
            "category": category,
            "expected_tool": expected_tool,
            "actual_tool": ctx.tool_to_use,
            "tool_match": tool_match,
            "correct": correct,
            "hallucination": hallucination,
            "latency": latency,
            "response": ctx.final_response,
            "error": ctx.error
        })
        
        print(f"    Tool Match: {tool_match} | Correct: {correct} | Latency: {latency:.2f}s\n")
        
        # Sleep to avoid rate limiting
        time.sleep(3.5)
        
    avg_latency = total_latency / len(EVAL_DATASET)
    tool_accuracy = (correct_tool_count / len(EVAL_DATASET)) * 100
    answer_accuracy = (correct_answer_count / len(EVAL_DATASET)) * 100
    
    summary = {
        "total": len(EVAL_DATASET),
        "tool_accuracy": tool_accuracy,
        "answer_accuracy": answer_accuracy,
        "hallucinations": hallucination_count,
        "avg_latency": avg_latency,
        "results": results
    }
    
    return summary

def generate_report(summary: dict, filepath: str = "evals_report.md"):
    print(f"Writing evaluation report to {filepath}...")
    
    report = []
    report.append("# Evals Report - FinDocs AI\n")
    report.append(f"**Date Generated**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    report.append("## Evaluation Summary\n")
    report.append(f"- **Total Test Cases**: {summary['total']}")
    report.append(f"- **Tool Selection Accuracy**: {summary['tool_accuracy']:.2f}%")
    report.append(f"- **Answer Correctness Rate**: {summary['answer_accuracy']:.2f}%")
    report.append(f"- **Hallucinations Detected**: {summary['hallucinations']}")
    report.append(f"- **Average Latency**: {summary['avg_latency']:.2f} seconds\n")
    
    report.append("## Category Summary\n")
    categories = list(set(r["category"] for r in summary["results"]))
    report.append("| Category | Total | Tool Match | Correct | Avg Latency |")
    report.append("| --- | --- | --- | --- | --- |")
    
    for cat in categories:
        cat_results = [r for r in summary["results"] if r["category"] == cat]
        c_total = len(cat_results)
        c_tool = sum(1 for r in cat_results if r["tool_match"])
        c_correct = sum(1 for r in cat_results if r["correct"])
        c_latency = sum(r["latency"] for r in cat_results) / c_total
        report.append(f"| {cat} | {c_total} | {c_tool}/{c_total} | {c_correct}/{c_total} | {c_latency:.2f}s |")
    
    report.append("\n## Detailed Results\n")
    report.append("| # | Category | Query | Expected Tool | Actual Tool | Tool Match | Correct? | Hallucinated? | Latency |")
    report.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    
    for idx, r in enumerate(summary["results"]):
        tool_status = "✅" if r["tool_match"] else "❌"
        correct_status = "✅" if r["correct"] else "❌"
        hallucination_status = "⚠️ Yes" if r["hallucination"] else "✅ No"
        report.append(
            f"| {idx+1} | {r['category']} | {r['query']} | `{r['expected_tool']}` | "
            f"`{r['actual_tool']}` | {tool_status} | {correct_status} | {hallucination_status} | {r['latency']:.2f}s |"
        )
        
    with open(filepath, mode="w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")
        
    print("Report written successfully.")

def main():
    start_time = time.time()
    summary = run_evaluations()
    generate_report(summary)
    print(f"\nAll evaluations complete in {(time.time() - start_time)/60:.2f} minutes!")
    
if __name__ == "__main__":
    main()
