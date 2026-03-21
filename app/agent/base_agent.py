import os
import httpx
import asyncio
from typing import List, TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from openai import AsyncOpenAI
from tavily import TavilyClient

from app.core.config import get_settings
from app.utils.pdf_parser import parse_pdf
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)

# 1. Define AgentState (TypedDict)
class AgentState(TypedDict):
    topic: str
    search_results: List[dict]
    pdf_texts: List[str]
    summaries: List[str]
    newsletter: str

# Helper for LLM calls using the openai library (compatible with Ollama)
async def call_llm(prompt: str) -> str:
    """Makes an async call to the LLM (OpenAI or Local via Ollama)."""
    api_key = settings.openai_api_key or "ollama"
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=settings.llm_base_url
    )
    
    logger.debug(f"Calling LLM with model: {settings.llm_model} at {settings.llm_base_url}")
    try:
        response = await client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=settings.news_letter_max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"LLM Call failed: {e}")
        return f"Error generating content: {e}"

# 2. Node Implementations

async def search_node(state: AgentState) -> dict:
    """Calls Tavily API to fetch web results."""
    logger.info(f"--- NODE: search_node | Topic: {state['topic']} ---")
    
    try:
        tavily = TavilyClient(api_key=settings.tavily_api_key)
        # Search for the topic with advanced depth for better quality
        results = tavily.search(
            query=state['topic'], 
            search_depth="advanced", 
            max_results=settings.tavily_max_results
        )
        
        found_results = results.get('results', [])
        logger.info(f"Found {len(found_results)} search results.")
        return {"search_results": found_results}
    except Exception as e:
        logger.error(f"Search node failed: {e}")
        return {"search_results": []}

async def pdf_reader_node(state: AgentState) -> dict:
    """Downloads and reads up to 5 PDFs from search results or local files."""
    logger.info("--- NODE: pdf_reader_node ---")
    
    pdf_urls = []
    for res in state['search_results']:
        url = res.get('url', '')
        if url.lower().endswith('.pdf'):
            pdf_urls.append(url)
    
    # Limit url downloads to max settings
    pdf_urls = pdf_urls[:settings.pdf_max_count]
    logger.info(f"Identified {len(pdf_urls)} potential PDFs to download.")
    
    pdf_texts = []
    async with httpx.AsyncClient() as client:
        for url in pdf_urls:
            try:
                logger.info(f"Downloading PDF: {url}")
                response = await client.get(url, timeout=30.0)
                if response.status_code == 200:
                    temp_name = f"temp_{abs(hash(url))}.pdf"
                    with open(temp_name, "wb") as f:
                        f.write(response.content)
                    
                    try:
                        text = parse_pdf(temp_name)
                        if len(text) > settings.pdf_max_chars:
                            text = text[:settings.pdf_max_chars] + "... [truncated]"
                        pdf_texts.append(text)
                        logger.info(f"Successfully parsed PDF: {url} ({len(text)} chars)")
                    finally:
                        if os.path.exists(temp_name):
                            os.remove(temp_name)
                else:
                    logger.warning(f"Failed to download PDF {url}: {response.status_code}")
            except Exception as e:
                logger.error(f"Error processing PDF from URL {url}: {e}")

    # Also read from local files if they exist in data/pdfs
    local_pdf_dir = os.path.join(os.getcwd(), "data", "pdfs")
    if os.path.exists(local_pdf_dir):
        logger.info(f"Checking for local PDFs in {local_pdf_dir}...")
        for filename in os.listdir(local_pdf_dir):
            if filename.lower().endswith(".pdf"):
                file_path = os.path.join(local_pdf_dir, filename)
                try:
                    logger.info(f"Reading local PDF: {filename}")
                    text = parse_pdf(file_path)
                    if len(text) > settings.pdf_max_chars:
                        text = text[:settings.pdf_max_chars] + "... [truncated]"
                    pdf_texts.append(text)
                except Exception as e:
                    logger.error(f"Error reading local PDF {filename}: {e}")

    # Limit total PDFs to settings
    pdf_texts = pdf_texts[:settings.pdf_max_count]
    return {"pdf_texts": pdf_texts}

async def summarizer_node(state: AgentState) -> dict:
    """Uses LLM to summarize each PDF/document."""
    logger.info("--- NODE: summarizer_node ---")
    
    summaries = []
    
    # Prioritize PDF content if available
    if state['pdf_texts']:
        for i, text in enumerate(state['pdf_texts']):
            logger.info(f"Summarizing PDF content block {i+1}...")
            prompt = (
                f"Please provide a concise but comprehensive summary of the following document text. "
                f"Focus on key findings, data, and insights related to the research topic: '{state['topic']}'.\n\n"
                f"Document Text:\n{text}"
            )
            summary = await call_llm(prompt)
            summaries.append(summary)
    
    # If no PDFs were found or to supplement, summarize search snippets
    if not summaries:
        logger.info("No PDF content available. Summarizing search snippets instead.")
        combined_snippets = "\n\n".join([
            f"Source: {res.get('url')}\nContent: {res.get('content')}" 
            for res in state['search_results']
        ])
        prompt = (
            f"Please provide a comprehensive summary of the following search results related to '{state['topic']}'. "
            f"Synthesize the information into key themes and findings.\n\n"
            f"Search Snippets:\n{combined_snippets}"
        )
        summary = await call_llm(prompt)
        summaries.append(summary)

    return {"summaries": summaries}

async def composer_node(state: AgentState) -> dict:
    """Writes the final newsletter from all summaries."""
    logger.info("--- NODE: composer_node ---")
    
    combined_summaries = "\n\n---\n\n".join(state['summaries'])
    prompt = (
        f"You are an expert research curator. Using the following research summaries about '{state['topic']}', "
        f"compose a high-quality, professional research newsletter.\n\n"
        f"Requirements:\n"
        f"1. Catchy and relevant title\n"
        f"2. Executive summary/Introduction\n"
        f"3. Detailed sections based on the research findings\n"
        f"4. Conclusion and future outlook\n"
        f"5. Professional tone but engaging for a general tech-savvy audience\n\n"
        f"Research Summaries:\n{combined_summaries}"
    )
    
    newsletter = await call_llm(prompt)
    logger.info("Newsletter composition complete.")
    return {"newsletter": newsletter}

# 3. Connect nodes into a StateGraph
workflow = StateGraph(AgentState)

# Add nodes to the graph
workflow.add_node("search_node", search_node)
workflow.add_node("pdf_reader_node", pdf_reader_node)
workflow.add_node("summarizer_node", summarizer_node)
workflow.add_node("composer_node", composer_node)

# Define the flow (edges)
workflow.add_edge(START, "search_node")
workflow.add_edge("search_node", "pdf_reader_node")
workflow.add_edge("pdf_reader_node", "summarizer_node")
workflow.add_edge("summarizer_node", "composer_node")
workflow.add_edge("composer_node", END)

# 4. Compile the graph
graph = workflow.compile()

async def run_agent(topic: str) -> str:
    """
    Public entry point to run the LangGraph research agent.
    
    Args:
        topic: The research topic to investigate.
        
    Returns:
        The generated newsletter text.
    """
    logger.info(f"Starting research agent for topic: {topic}")
    
    initial_state: AgentState = {
        "topic": topic,
        "search_results": [],
        "pdf_texts": [],
        "summaries": [],
        "newsletter": ""
    }
    
    try:
        final_state = await graph.ainvoke(initial_state)
        return final_state.get("newsletter", "Agent failed to produce a newsletter.")
    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        return f"Agent error: {e}"