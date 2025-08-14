#!/usr/bin/env python3
"""
Simple test script for the Patent Agent System
"""

import asyncio
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_system():
    """Test the basic system functionality"""
    try:
        print("Testing Patent Agent System...")
        
        # Test basic imports
        print("✓ Testing imports...")
        import fastmcp_config
        print("  - FastMCP config imported")
        
        import google_a2a_client
        print("  - Google A2A client imported")
        
        # Test agent imports
        print("✓ Testing agent imports...")
        from agents.base_agent import BaseAgent
        print("  - Base agent imported")
        
        from agents.planner_agent import PlannerAgent
        print("  - Planner agent imported")
        
        from agents.coordinator_agent import CoordinatorAgent
        print("  - Coordinator agent imported")
        
        # Test system import
        print("✓ Testing system import...")
        import patent_agent_system
        print("  - Patent agent system imported")
        
        print("\n🎉 All imports successful! System is ready to run.")
        
        # Test system initialization
        print("\n✓ Testing system initialization...")
        system = patent_agent_system.PatentAgentSystem()
        print("  - System instance created")
        
        print("\n✅ Patent Agent System test completed successfully!")
        print("The system is ready to use with FastMCP and Google A2A integration.")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("Patent Agent System - Simple Test")
    print("=" * 50)
    
    # Run the test
    success = asyncio.run(test_system())
    
    if success:
        print("\n🚀 Ready to run the full demo!")
        print("You can now run:")
        print("  python3 demo_simple.py")
        print("  python3 main.py --interactive")
    else:
        print("\n⚠️  Some issues were found. Please check the error messages above.")
        sys.exit(1)