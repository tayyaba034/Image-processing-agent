"""
Image Preprocessing Agent - Main Entry Point
Auto-detects available API keys and routes to appropriate processor
Supports both OpenAI API and Google Gemini API
"""

import os
import sys
from dotenv import load_dotenv


def detect_api_provider():
    """
    Detect which API provider is configured
    
    Returns:
        str: Either 'openai', 'gemini', or None if neither is configured
    """
    # Load environment variables
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    # Check OpenAI first (takes precedence)
    if openai_key and not openai_key.startswith('sk-') == False:
        return 'openai'
    
    # Check Gemini
    if gemini_key and gemini_key != 'your-gemini-api-key-here':
        return 'gemini'
    
    return None


def run_with_openai():
    """Run agent with OpenAI API"""
    from image_preprocessing_openai import main as openai_main
    
    print("\n✅ OpenAI API key detected!")
    print("🚀 Launching Image Preprocessing Agent with OpenAI API...\n")
    openai_main()


def run_with_gemini():
    """Run agent with Gemini API"""
    from image_preprocessing_gemini import main as gemini_main
    
    print("\n✅ Gemini API key detected!")
    print("🚀 Launching Image Preprocessing Agent with Gemini API...\n")
    gemini_main()


def main():
    """Main entry point with auto-detection"""
    
    print("=" * 70)
    print("Image Preprocessing Agent - Auto-Detecting API Provider")
    print("=" * 70)
    
    # Load environment variables
    load_dotenv()
    
    # Detect which API is available
    provider = detect_api_provider()
    
    if provider == 'openai':
        run_with_openai()
    elif provider == 'gemini':
        run_with_gemini()
    else:
        print("\n❌ ERROR: No API key configured!")
        print("\n" + "=" * 70)
        print("Please configure one of the following:")
        print("=" * 70)
        print("\n📍 OPTION 1: OpenAI API (Recommended for Production)")
        print("   1. Get your OpenAI API key from: https://platform.openai.com/api-keys")
        print("   2. Edit the .env file and add:")
        print("      OPENAI_API_KEY=sk-...your-actual-key")
        print("\n📍 OPTION 2: Google Gemini API (Free Alternative)")
        print("   1. Get your Gemini API key from: https://aistudio.google.com/app/apikey")
        print("   2. Edit the .env file and add:")
        print("      GEMINI_API_KEY=AIzaSy...your-actual-key")
        print("\n" + "=" * 70)
        print("\nAfter configuring, run this script again:")
        print("   python image_preprocessing_agent.py")
        print("\n" + "=" * 70)
        sys.exit(1)


def show_usage():
    """Show usage information"""
    print("\n" + "=" * 70)
    print("Image Preprocessing Agent - Usage")
    print("=" * 70)
    print("\n🎯 Quick Start:\n")
    print("1. Auto-detect API (Recommended):")
    print("   python image_preprocessing_agent.py\n")
    print("2. Force OpenAI API:")
    print("   python image_preprocessing_openai.py\n")
    print("3. Force Gemini API:")
    print("   python image_preprocessing_gemini.py\n")
    print("=" * 70)


if __name__ == "__main__":
    # Show usage if --help flag is provided
    if '--help' in sys.argv or '-h' in sys.argv:
        show_usage()
        sys.exit(0)
    
    # Run main with auto-detection
    main()
