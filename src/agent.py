import os
import sys
import time
from abc import ABC, abstractmethod
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

try:
    from src.llm_strategy import get_llm_provider
    from src.retrieval import retrieve_documents
    from src.structured_query import answer_structured_query
except ImportError:
    # Handle direct script executions
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.llm_strategy import get_llm_provider
    from src.retrieval import retrieve_documents
    from src.structured_query import answer_structured_query

class QueryContext:
    """Context object passed through the Chain of Responsibility pipeline."""
    def __init__(self, query: str):
        self.query = query
        self.intent = None           # 'RETRIEVAL' or 'STRUCTURED_SQL'
        self.tool_to_use = None      # name of the tool selected
        self.tool_result = None      # raw response/data from the executed tool
        self.final_response = None   # formatted natural language answer
        self.success = True
        self.error = None
        self.metadata = {
            "start_time": time.time(),
            "latencies": {},
            "tokens": {}
        }
        
    def add_latency(self, stage_name: str, duration: float):
        self.metadata["latencies"][stage_name] = duration

class QueryPipelineHandler(ABC):
    """Abstract Base Handler for Chain of Responsibility query pipeline stages."""
    def __init__(self, next_handler: 'QueryPipelineHandler' = None):
        self.next_handler = next_handler
        
    def handle(self, context: QueryContext):
        stage_name = self.__class__.__name__
        start = time.time()
        try:
            self.process(context)
        except Exception as e:
            context.success = False
            context.error = f"Error in {stage_name}: {str(e)}"
            return
            
        duration = time.time() - start
        context.add_latency(stage_name, duration)
        
        if self.next_handler and context.success:
            self.next_handler.handle(context)
            
    @abstractmethod
    def process(self, context: QueryContext):
        """Perform the actual processing for this stage."""
        pass

class IntentParserHandler(QueryPipelineHandler):
    """Stage 1: Parse the user's intent to classify the query type."""
    def process(self, context: QueryContext):
        llm = get_llm_provider()
        
        system_prompt = (
            "You are a routing agent for a financial RAG system.\n"
            "Your job is to classify user queries into one of two categories:\n"
            "1. 'STRUCTURED_SQL': Use this for quantitative, mathematical, computational, aggregate, "
            "or statistical queries. Examples: summing spending, finding averages, counts, listing top categories, "
            "fetching exact amounts (like a salary amount) from tables.\n"
            "2. 'RETRIEVAL': Use this for semantic search, looking for textual descriptions, details, "
            "clarifications, or specific transactional occurrences that don't need calculation. "
            "Examples: 'Who did I buy flowers for?', 'Find any transactions related to Spotify', 'What company did I rent from?'.\n\n"
            "Respond with ONLY one word: either 'STRUCTURED_SQL' or 'RETRIEVAL'."
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Classify this query: {query}")
        ])
        
        chain = prompt | llm | StrOutputParser()
        intent = chain.invoke({"query": context.query}).strip().upper()
        
        # Sanitize output (e.g. if LLM returned markdown code blocks or extra words)
        if "STRUCTURED_SQL" in intent:
            context.intent = "STRUCTURED_SQL"
        else:
            context.intent = "RETRIEVAL"

class ToolPickerHandler(QueryPipelineHandler):
    """Stage 2: Select the correct tool based on parsed intent."""
    def process(self, context: QueryContext):
        if context.intent == "STRUCTURED_SQL":
            context.tool_to_use = "structured_database_tool"
        else:
            context.tool_to_use = "semantic_retrieval_tool"

class ToolExecutorHandler(QueryPipelineHandler):
    """Stage 3: Execute the selected tool and capture raw output."""
    def process(self, context: QueryContext):
        if context.tool_to_use == "structured_database_tool":
            res = answer_structured_query(context.query)
            if res["success"]:
                context.tool_result = {
                    "source": "SQLite DB",
                    "sql_query": res["sql"],
                    "columns": res["columns"],
                    "data": res["results"]
                }
            else:
                raise Exception(f"SQLite text-to-SQL execution failed: {res.get('error', 'Unknown error')}")
                
        elif context.tool_to_use == "semantic_retrieval_tool":
            docs = retrieve_documents(context.query, k=5)
            formatted_docs = []
            for doc in docs:
                formatted_docs.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata
                })
            context.tool_result = {
                "source": "FAISS Vector Store",
                "documents": formatted_docs
            }
        else:
            raise ValueError(f"Unknown tool name: {context.tool_to_use}")

class ResponseFormatterHandler(QueryPipelineHandler):
    """Stage 4: Format raw tool output into a friendly natural language response."""
    def process(self, context: QueryContext):
        llm = get_llm_provider()
        
        system_prompt = (
            "You are a primary Checking Account Query Assistant for Jane Doe. "
            "You help users query their bank statements and expense reports.\n\n"
            "Use the provided tool execution output to formulate a natural language, precise, and professional response. "
            "Do not invent or hallucinate transactions or amounts that are not in the tool output. "
            "Negative transaction amounts indicate expenses/spending, and positive amounts indicate income/deposits.\n\n"
            "TOOL OUTPUT:\n"
            "{tool_result}\n\n"
            "Format the numbers nicely (e.g. $1,500.00). If the output contains SQL rows or matching document text, "
            "summarize or list them clearly. If no information is found, explain that politely."
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Answer this question: {query}")
        ])
        
        chain = prompt | llm | StrOutputParser()
        context.final_response = chain.invoke({
            "query": context.query,
            "tool_result": str(context.tool_result)
        }).strip()

def run_agent(query: str) -> QueryContext:
    """Build and execute the Chain of Responsibility pipeline for a query."""
    # Build the chain
    formatter = ResponseFormatterHandler()
    executor = ToolExecutorHandler(next_handler=formatter)
    picker = ToolPickerHandler(next_handler=executor)
    parser = IntentParserHandler(next_handler=picker)
    
    # Initialize and execute context
    context = QueryContext(query)
    parser.handle(context)
    
    # Calculate overall latency
    context.metadata["total_latency"] = time.time() - context.metadata["start_time"]
    return context

def main():
    if len(sys.argv) < 2:
        queries = [
            "What was my total spend in March?",
            "Find my transaction for Spotify Premium",
            "Show total spend grouped by category for January 2026",
            "How much did I make from Freelance Design Client?",
            "What company did I pay rent to?"
        ]
    else:
        queries = [" ".join(sys.argv[1:])]
        
    print("Running Agent Query Pipeline (Chain of Responsibility) Tests...\n")
    for q in queries:
        print(f"User Query: '{q}'")
        ctx = run_agent(q)
        if ctx.success:
            print(f"  Parsed Intent: {ctx.intent}")
            print(f"  Selected Tool: {ctx.tool_to_use}")
            print(f"  Final Response: {ctx.final_response}")
            print(f"  Latencies: {ctx.metadata['latencies']}")
            print(f"  Total Latency: {ctx.metadata['total_latency']:.4f}s")
        else:
            print(f"  Pipeline Error: {ctx.error}")
        print("-" * 70)

if __name__ == "__main__":
    main()
