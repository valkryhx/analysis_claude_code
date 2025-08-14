#!/usr/bin/env python3
"""
Test script for GLM-4.5-flash client
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from glm_client import get_glm_client

async def test_glm_client():
    """Test the GLM client functionality"""
    try:
        print("🧪 Testing GLM-4.5-flash client...")
        
        # Check if API key is set
        api_key = os.getenv("GLM_API_KEY")
        if not api_key:
            print("❌ GLM_API_KEY not found in environment variables")
            print("Please set GLM_API_KEY in your .env file")
            return False
            
        print(f"✅ GLM API key found: {api_key[:10]}...")
        
        # Initialize client
        client = await get_glm_client()
        print("✅ GLM client initialized successfully")
        
        # Test basic functionality
        test_topic = "AI-powered patent analysis system"
        test_description = "A system that uses artificial intelligence to analyze patent applications and provide recommendations"
        
        print(f"\n🔍 Testing patent topic analysis...")
        analysis = await client.analyze_patent_topic(test_topic, test_description)
        print(f"✅ Analysis completed: Novelty score {analysis.novelty_score}/10")
        
        print(f"\n🔎 Testing prior art search...")
        keywords = ["AI", "patent", "analysis", "system"]
        search_results = await client.search_prior_art(test_topic, keywords)
        print(f"✅ Search completed: Found {len(search_results)} results")
        
        print(f"\n✍️ Testing patent draft generation...")
        draft = await client.generate_patent_draft(test_topic, test_description, analysis)
        print(f"✅ Draft generated: Title: {draft.title}")
        
        print(f"\n📋 Testing patent review...")
        review = await client.review_patent_draft(draft, analysis)
        print(f"✅ Review completed: Quality score {review['quality_score']}/10")
        
        print(f"\n🎯 All tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Starting GLM client tests...")
    
    success = await test_glm_client()
    
    if success:
        print("\n🎉 All tests completed successfully!")
        print("Your GLM-4.5-flash client is working correctly.")
    else:
        print("\n💥 Some tests failed. Please check your configuration.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())