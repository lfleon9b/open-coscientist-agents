"""
Simple Example: Using CoScientist for Scientific Research
===========================================================

This example demonstrates how to use the CoScientist framework to explore
a scientific research question. We'll use a straightforward question about
vitamin D and immunity to illustrate the system's capabilities.

The system will:
1. Conduct a literature review
2. Generate multiple hypotheses using different AI models
3. Rank hypotheses through competitive tournaments
4. Evolve and refine the best ideas
5. Produce a comprehensive research report
"""

import asyncio
from coscientist.framework import CoscientistConfig, CoscientistFramework
from coscientist.global_state import CoscientistState, CoscientistStateManager


async def simple_research_example():
    """
    Run a simple research question through the CoScientist system.
    
    This example uses a clear, manageable research question to demonstrate
    the full capabilities of the multi-agent system.
    """
    
    # =========================================================================
    # STEP 1: Define Your Research Question
    # =========================================================================
    # The research goal should be specific, scientific, and answerable through
    # literature review and hypothesis generation.
    
    research_goal = (
        "Does vitamin D supplementation enhance immune system function in adults? "
        "What are the mechanisms, and what dosage is most effective?"
    )
    
    print("=" * 80)
    print("CoScientist Framework - Simple Example")
    print("=" * 80)
    print(f"\nResearch Goal: {research_goal}\n")
    
    # =========================================================================
    # STEP 2: Initialize the State
    # =========================================================================
    # The CoscientistState manages all data throughout the research process:
    # - Literature reviews
    # - Generated hypotheses
    # - Tournament results
    # - Evolution history
    # - Final reports
    #
    # The state is automatically saved to disk at: ~/.coscientist/<goal_hash>/
    
    print("Initializing research state...")
    initial_state = CoscientistState(goal=research_goal)
    print(f"✓ State directory created: {initial_state._output_dir}\n")
    
    # =========================================================================
    # STEP 3: Configure the Framework
    # =========================================================================
    # The CoscientistConfig allows you to customize:
    # - Which LLMs to use for each agent type
    # - Specialist fields for hypothesis generation
    # - Embedding models for semantic similarity
    #
    # Default configuration uses:
    # - Gemini 2.5 Pro, Claude Sonnet 4, and o3 for generation
    # - Claude Sonnet 4 for supervision and final reports
    # - Gemini Flash for meta-reviews (handles long context well)
    
    print("Configuring multi-agent system...")
    config = CoscientistConfig()
    print(f"✓ Generation LLMs: {list(config.generation_agent_llms.keys())}")
    print(f"✓ Specialist fields: {config.specialist_fields}\n")
    
    # =========================================================================
    # STEP 4: Create the Framework and State Manager
    # =========================================================================
    # The StateManager handles state transitions between agents
    # The Framework orchestrates the entire research workflow
    
    state_manager = CoscientistStateManager(initial_state)
    cosci = CoscientistFramework(config, state_manager)
    
    print("Framework initialized. Available actions:")
    for action in cosci.available_actions():
        print(f"  - {action}")
    print()
    
    # =========================================================================
    # STEP 5: Run the Research Process
    # =========================================================================
    # The run() method executes the full research pipeline:
    #
    # Phase 1 - Literature Review:
    #   - Decomposes research goal into subtopics
    #   - Uses GPT Researcher to gather and synthesize information
    #
    # Phase 2 - Hypothesis Generation:
    #   - Creates initial hypotheses using multiple LLMs
    #   - Uses different reasoning strategies (causal, observational, etc.)
    #   - Can generate independently or collaboratively
    #
    # Phase 3 - Reflection & Verification:
    #   - Deep verification of each hypothesis
    #   - Checks for logical consistency and scientific validity
    #   - Filters out low-quality hypotheses
    #
    # Phase 4 - Tournament Ranking:
    #   - Pits hypotheses against each other head-to-head
    #   - Uses ELO rating system (like chess rankings)
    #   - Records debate transcripts explaining rankings
    #
    # Phase 5 - Meta-Review:
    #   - Synthesizes insights across top hypotheses
    #   - Identifies patterns and research directions
    #
    # Phase 6 - Evolution (Iterative):
    #   - Supervisor decides next actions based on progress
    #   - Top hypotheses are refined based on feedback
    #   - New hypotheses can be generated
    #   - Process repeats until research is complete
    #
    # Phase 7 - Final Report:
    #   - Comprehensive summary of findings
    #   - Top 3 hypotheses with detailed analysis
    #   - Recommendations for future research
    
    print("=" * 80)
    print("Starting Research Process")
    print("=" * 80)
    print("\nThis will take 15-30 minutes depending on API response times...")
    print("Progress is automatically saved to disk after each major step.\n")
    
    try:
        final_report, final_meta_review = await cosci.run()
        
        # =====================================================================
        # STEP 6: Review the Results
        # =====================================================================
        
        print("\n" + "=" * 80)
        print("Research Complete!")
        print("=" * 80)
        
        print("\n" + "-" * 80)
        print("FINAL META-REVIEW")
        print("-" * 80)
        print(final_meta_review)
        
        print("\n" + "-" * 80)
        print("FINAL REPORT")
        print("-" * 80)
        print(final_report)
        
        # =====================================================================
        # STEP 7: Explore Additional Insights
        # =====================================================================
        
        print("\n" + "=" * 80)
        print("Additional Insights")
        print("=" * 80)
        
        # View hypothesis tournament rankings
        print("\nTop 5 Hypotheses by ELO Rating:")
        top_hypotheses = state_manager._state.tournament.get_sorted_hypotheses()[:5]
        for i, (uid, rating) in enumerate(top_hypotheses, 1):
            hypothesis = state_manager._state.tournament.hypotheses[uid]
            print(f"\n{i}. [ELO: {rating:.0f}] {hypothesis.prediction}")
        
        # View semantic communities
        print("\n\nSemantic Communities:")
        communities = cosci.get_semantic_communities(resolution=1.0, min_weight=0.85)
        print(f"Found {len(communities)} distinct research directions")
        
        # View supervisor decision history
        print(f"\n\nSupervisor Actions Taken: {len(state_manager._state.actions)}")
        for i, action in enumerate(state_manager._state.actions, 1):
            print(f"  {i}. {action}")
        
        print("\n" + "=" * 80)
        print("Results saved to:", initial_state._output_dir)
        print("=" * 80)
        print("\nYou can:")
        print("1. Load the state later with: CoscientistState.load_latest(goal='...')")
        print("2. View results in the web interface: streamlit run app/tournament_viewer.py")
        print("3. Access the state file directly for custom analysis")
        
    except Exception as e:
        print(f"\n❌ Error during research process: {e}")
        print(f"Partial results saved to: {initial_state._output_dir}")
        raise


# =============================================================================
# HELPER FUNCTION: Monitor Progress During Long Runs
# =============================================================================

async def monitor_research_progress(cosci: CoscientistFramework):
    """
    Optional: Monitor the research process in real-time.
    
    You can run this in a separate task to track progress while
    the main research process is running.
    """
    state_manager = cosci.state_manager
    
    while not state_manager.is_finished:
        print("\n--- Progress Update ---")
        print(f"Total Hypotheses: {state_manager.total_hypotheses}")
        print(f"Tournament Hypotheses: {state_manager.num_tournament_hypotheses}")
        print(f"Unranked Hypotheses: {state_manager.num_unranked_hypotheses}")
        print(f"Actions Taken: {len(state_manager._state.actions)}")
        
        if state_manager._state.actions:
            print(f"Last Action: {state_manager._state.actions[-1]}")
        
        # Wait before checking again
        await asyncio.sleep(60)  # Check every minute


# =============================================================================
# RUN THE EXAMPLE
# =============================================================================

if __name__ == "__main__":
    # Run the simple research example
    asyncio.run(simple_research_example())
    
    # Alternative: Run with progress monitoring
    # async def main():
    #     # Create the framework
    #     goal = "Does vitamin D supplementation enhance immune function?"
    #     state = CoscientistState(goal=goal)
    #     config = CoscientistConfig()
    #     state_manager = CoscientistStateManager(state)
    #     cosci = CoscientistFramework(config, state_manager)
    #     
    #     # Run research with monitoring
    #     research_task = asyncio.create_task(cosci.run())
    #     monitor_task = asyncio.create_task(monitor_research_progress(cosci))
    #     
    #     # Wait for research to complete
    #     final_report, final_meta_review = await research_task
    #     monitor_task.cancel()
    #     
    #     return final_report, final_meta_review
    # 
    # asyncio.run(main())
