"""
Minimal Example: Quick Start with CoScientist
==============================================

This is the absolute minimal code needed to run CoScientist.
For a detailed, educational example, see simple_example.py
"""

import asyncio
from coscientist.framework import CoscientistConfig, CoscientistFramework
from coscientist.global_state import CoscientistState, CoscientistStateManager


async def main():
    # 1. Define your research question
    goal = "Does vitamin D supplementation enhance immune function in adults?"
    
    # 2. Initialize state and framework
    initial_state = CoscientistState(goal=goal)
    config = CoscientistConfig()
    state_manager = CoscientistStateManager(initial_state)
    cosci = CoscientistFramework(config, state_manager)
    
    # 3. Run the research pipeline
    final_report, meta_review = await cosci.run()
    
    # 4. Print results
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    print(f"\n{final_report}\n")
    
    return final_report, meta_review


if __name__ == "__main__":
    # Run the research
    asyncio.run(main())
