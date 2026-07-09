# Evals Report - FinDocs AI

**Date Generated**: 2026-07-09 16:20:40

## Evaluation Summary

- **Total Test Cases**: 32
- **Tool Selection Accuracy**: 18.75%
- **Answer Correctness Rate**: 9.38%
- **Hallucinations Detected**: 0
- **Average Latency**: 3.16 seconds

## Category Summary

| Category | Total | Tool Match | Correct | Avg Latency |
| --- | --- | --- | --- | --- |
| Retrieval | 10 | 2/10 | 2/10 | 1.98s |
| Computation | 12 | 2/12 | 0/12 | 0.87s |
| Edge Case - Ambiguous | 5 | 1/5 | 1/5 | 6.55s |
| Edge Case - No Answer | 5 | 1/5 | 0/5 | 7.61s |

## Detailed Results

| # | Category | Query | Expected Tool | Actual Tool | Tool Match | Correct? | Hallucinated? | Latency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Computation | What was my total spend in March? | `structured_database_tool` | `structured_database_tool` | ✅ | ❌ | ✅ No | 3.30s |
| 2 | Computation | How much did I spend in January? | `structured_database_tool` | `structured_database_tool` | ✅ | ❌ | ✅ No | 1.39s |
| 3 | Computation | What was my total spending in February 2026? | `structured_database_tool` | `None` | ❌ | ❌ | ✅ No | 0.47s |
| 4 | Computation | What was my total spend in April? | `structured_database_tool` | `None` | ❌ | ❌ | ✅ No | 0.55s |
| 5 | Computation | What is my total TechCorp salary from January to April? | `structured_database_tool` | `None` | ❌ | ❌ | ✅ No | 0.65s |
| 6 | Computation | How much money did I earn from Freelance Design Client in March? | `structured_database_tool` | `None` | ❌ | ❌ | ✅ No | 0.73s |
| 7 | Computation | What was the total rent paid? | `structured_database_tool` | `None` | ❌ | ❌ | ✅ No | 0.54s |
| 8 | Computation | How much was spent at Whole Foods Market in February? | `structured_database_tool` | `None` | ❌ | ❌ | ✅ No | 0.55s |
| 9 | Computation | What is the average transaction amount for Groceries? | `structured_database_tool` | `None` | ❌ | ❌ | ✅ No | 0.62s |
| 10 | Computation | How many transactions occurred in January? | `structured_database_tool` | `None` | ❌ | ❌ | ✅ No | 0.52s |
| 11 | Computation | What was my maximum single expense amount? | `structured_database_tool` | `None` | ❌ | ❌ | ✅ No | 0.66s |
| 12 | Computation | What is my total freelance design client income? | `structured_database_tool` | `None` | ❌ | ❌ | ✅ No | 0.50s |
| 13 | Retrieval | Find my transactions for Netflix Subscription | `semantic_retrieval_tool` | `semantic_retrieval_tool` | ✅ | ✅ | ✅ No | 7.62s |
| 14 | Retrieval | What gas station did I visit in January? | `semantic_retrieval_tool` | `semantic_retrieval_tool` | ✅ | ✅ | ✅ No | 6.21s |
| 15 | Retrieval | Who paid me salary? | `semantic_retrieval_tool` | `None` | ❌ | ❌ | ✅ No | 0.44s |
| 16 | Retrieval | What company did I pay rent to? | `semantic_retrieval_tool` | `None` | ❌ | ❌ | ✅ No | 0.58s |
| 17 | Retrieval | Find my Spotify Premium payments | `semantic_retrieval_tool` | `None` | ❌ | ❌ | ✅ No | 0.48s |
| 18 | Retrieval | What did I buy at Best Buy? | `semantic_retrieval_tool` | `None` | ❌ | ❌ | ✅ No | 0.57s |
| 19 | Retrieval | Where did I buy groceries in March? | `semantic_retrieval_tool` | `None` | ❌ | ❌ | ✅ No | 0.67s |
| 20 | Retrieval | Find design freelance client payments | `semantic_retrieval_tool` | `None` | ❌ | ❌ | ✅ No | 0.52s |
| 21 | Retrieval | What did I purchase from the Apple Store? | `semantic_retrieval_tool` | `None` | ❌ | ❌ | ✅ No | 1.27s |
| 22 | Retrieval | What city utility bills did I pay in February? | `semantic_retrieval_tool` | `None` | ❌ | ❌ | ✅ No | 1.45s |
| 23 | Edge Case - No Answer | How much did I spend on Tesla stock? | `semantic_retrieval_tool` | `None` | ❌ | ❌ | ✅ No | 0.70s |
| 24 | Edge Case - No Answer | Find any transactions for gym membership | `semantic_retrieval_tool` | `semantic_retrieval_tool` | ✅ | ❌ | ✅ No | 12.75s |
| 25 | Edge Case - No Answer | How much did I spend on Uber rides? | `semantic_retrieval_tool` | `structured_database_tool` | ❌ | ❌ | ✅ No | 23.37s |
| 26 | Edge Case - No Answer | What was my bonus in January? | `semantic_retrieval_tool` | `None` | ❌ | ❌ | ✅ No | 0.66s |
| 27 | Edge Case - No Answer | Show transactions for Walmart | `semantic_retrieval_tool` | `None` | ❌ | ❌ | ✅ No | 0.58s |
| 28 | Edge Case - Ambiguous | What about Target? | `semantic_retrieval_tool` | `None` | ❌ | ❌ | ✅ No | 0.63s |
| 29 | Edge Case - Ambiguous | Tell me about gas expenses | `semantic_retrieval_tool` | `None` | ❌ | ❌ | ✅ No | 0.51s |
| 30 | Edge Case - Ambiguous | What is salary? | `semantic_retrieval_tool` | `None` | ❌ | ❌ | ✅ No | 0.42s |
| 31 | Edge Case - Ambiguous | How much did I spend on food? | `structured_database_tool` | `structured_database_tool` | ✅ | ✅ | ✅ No | 18.89s |
| 32 | Edge Case - Ambiguous | Show my utilities | `semantic_retrieval_tool` | `structured_database_tool` | ❌ | ❌ | ✅ No | 12.30s |
