"""
Test script to verify Gemini API configuration
"""
import os
from dotenv import load_dotenv

def test_gemini_config():
    """Test if Gemini API is properly configured"""
    
    print("=" * 70)
    print("Testing Gemini API Configuration")
    print("=" * 70)
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    
    if not gemini_api_key:
        print("\n❌ GEMINI_API_KEY not found in environment")
        print("\nPlease set your API key in .env file:")
        print("1. Get key from: https://aistudio.google.com/app/apikey")
        print("2. Edit .env and set: GEMINI_API_KEY=your-key")
        return False
    
    if gemini_api_key == 'your-gemini-api-key-here':
        print("\n⚠️  GEMINI_API_KEY is set to default placeholder")
        print("\nPlease replace with your actual API key:")
        print("1. Get key from: https://aistudio.google.com/app/apikey")
        print("2. Edit .env and replace the placeholder")
        return False
    
    print(f"\n✅ GEMINI_API_KEY found: {gemini_api_key[:20]}...")
    
    # Test OpenAI client configuration
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=gemini_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        
        print("✅ OpenAI client configured with Gemini endpoint")
        print(f"   Base URL: {client.base_url}")
        
    except Exception as e:
        print(f"\n❌ Error configuring OpenAI client: {e}")
        return False
    
    # Test Swarm initialization
    try:
        from swarm import Swarm
        
        swarm_client = Swarm(client=client)
        print("✅ Swarm client initialized successfully")
        
    except Exception as e:
        print(f"\n❌ Error initializing Swarm: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("✅ All configuration tests passed!")
    print("=" * 70)
    print("\nYou can now run the agent:")
    print("  uv run python image_preprocessing_agent.py")
    print("\n")
    
    return True

if __name__ == "__main__":
    test_gemini_config()
