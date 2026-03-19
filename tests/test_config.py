from app.core.config import get_settings

def test_loading_settings():
    settings = get_settings()
    print(f"OPENAI_API_KEY: {settings.openai_api_key}")
    print(f"TAVILY_API_KEY: {settings.tavily_api_key}")
    print(f"LLM_BASE_URL: {settings.llm_base_url}")
    print(f"LLM_MODEL: {settings.llm_model}")
    print(f"LOG_LEVEL: {settings.log_level}")
    print(f"ENVIRONMENT: {settings.environment}")

    assert settings.openai_api_key == "sk-test-openai-key"
    assert settings.tavily_api_key == "tvly-test-tavily-key"
    print("Test passed!")

if __name__ == "__main__":
    test_loading_settings()
