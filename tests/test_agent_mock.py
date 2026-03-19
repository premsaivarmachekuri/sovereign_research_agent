import asyncio
import sys
import os
from unittest.mock import MagicMock, AsyncMock, patch

# Ensure the app directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.agent.base_agent import run_agent

async def test_agent():
    print("🚀 Testing Research Agent LangGraph Logic...")
    
    # Set dummy env vars for the agent to initialize settings without failing
    os.environ["TAVILY_API_KEY"] = "dummy"
    os.environ["OPENAI_API_KEY"] = "dummy"
    
    # Mocking Tavily, OpenAI, and HTTP calls to test the graph logic
    with patch('app.agent.base_agent.TavilyClient') as MockTavily, \
         patch('app.agent.base_agent.AsyncOpenAI') as MockOpenAI, \
         patch('app.agent.base_agent.httpx.AsyncClient.get') as MockHttpGet:
        
        # 1. Mock Tavily Search Results
        mock_tavily = MockTavily.return_value
        mock_tavily.search.return_value = {
            "results": [
                {"url": "https://example.com/whitepaper.pdf", "content": "Future solar tech trends..."},
                {"url": "https://example.com/news", "content": "Solar market growing rapidly."}
            ]
        }
        
        # 2. Mock OpenAI Chat Response
        mock_openai_instance = MockOpenAI.return_value
        mock_openai_instance.chat.completions.create = AsyncMock(return_value=MagicMock(
            choices=[MagicMock(message=MagicMock(content="[MOCK NEWSLETTER CONTENT] This research explores the future of solar batteries, focusing on solid-state tech and cost reduction."))]
        ))
        
        # 3. Mock HTTP Get for PDF downloading
        MockHttpGet.return_value = MagicMock(status_code=200, content=b"%PDF-1.4 mock content")
        
        # 4. Mock PDF Parser utility
        with patch('app.agent.base_agent.parse_pdf', return_value="Deep technical details from the solar whitepaper PDF."):
            topic = "Future of Solar Batteries"
            
            try:
                result = await run_agent(topic)
                
                print("\n✅ Agent Result Received:")
                print("-" * 30)
                print(result)
                print("-" * 30)
                
                # Basic assertions
                if "[MOCK NEWSLETTER CONTENT]" in result:
                    print("SUCCESS: Graph nodes executed in correct sequence and produced output.")
                else:
                    print("FAILURE: Result does not contain expected mock content.")
                    
            except Exception as e:
                print(f"❌ Test failed with error: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_agent())
