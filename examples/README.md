# CoScientist Examples

This directory contains example scripts demonstrating how to use the CoScientist framework for AI-driven scientific research.

## 📁 Examples

### `simple_example.py` - Complete Research Pipeline

A fully documented example showing the entire research workflow from start to finish.

**What it demonstrates:**
- Setting up a research question
- Configuring the multi-agent system
- Running the full research pipeline
- Viewing and interpreting results

**How to run:**
```bash
# Make sure you have API keys set up
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
export GOOGLE_API_KEY="your-key"
export TAVILY_API_KEY="your-key"

# Run the example
python examples/simple_example.py
```

**Expected runtime:** 15-30 minutes

**Output:**
- Literature review reports
- Generated and ranked hypotheses
- Tournament results with ELO ratings
- Meta-review synthesizing insights
- Final comprehensive report

---

## 🎯 Understanding the Workflow

### Phase 1: Literature Review (2-5 minutes)
The system breaks down your research question into subtopics and conducts comprehensive literature searches using GPT Researcher.

**Example output:**
- 3-5 subtopic areas identified
- Detailed reports for each subtopic
- Synthesized literature overview

### Phase 2: Hypothesis Generation (3-8 minutes)
Multiple AI models generate scientific hypotheses using different reasoning approaches:
- **Independent Generation**: Single model creates hypothesis using specific reasoning strategy
- **Collaborative Generation**: Two models debate and refine hypothesis together

**Reasoning strategies:**
- Causal reasoning (cause → effect)
- Observational reasoning (patterns in data)
- Assumption decomposition (breaking down complex ideas)
- Out-of-the-box thinking (novel approaches)

### Phase 3: Reflection & Verification (2-5 minutes)
Each hypothesis undergoes deep verification:
- Logical consistency checks
- Scientific validity assessment
- Identification of testable predictions
- Quality filtering

**Example verification:**
```
Hypothesis: "Vitamin D modulates T-cell function through VDR receptor binding"

Verification checks:
✓ Mechanism is biologically plausible
✓ Testable predictions are specific
✓ Evidence from literature is cited
✓ Logical chain is sound
```

### Phase 4: Tournament Ranking (3-10 minutes)
Hypotheses compete head-to-head using an ELO rating system:

**How it works:**
1. Two hypotheses are compared by an AI judge
2. Judge explains which is more promising and why
3. ELO ratings are updated based on outcomes
4. Multiple rounds ensure robust rankings

**Example tournament:**
```
Match 1: Hypothesis A vs Hypothesis B
Winner: Hypothesis A
Reasoning: "A provides a more specific mechanism with testable predictions..."

Updated ELO:
- Hypothesis A: 1400 → 1425
- Hypothesis B: 1400 → 1375
```

### Phase 5: Meta-Review (2-4 minutes)
The system synthesizes insights across top hypotheses:
- Identifies common themes
- Highlights complementary mechanisms
- Suggests research directions
- Evaluates evidence strength

### Phase 6: Evolution & Iteration (5-15 minutes)
A supervisor agent decides what to do next:
- Generate more hypotheses in under-explored areas
- Evolve top hypotheses based on feedback
- Expand literature review if needed
- Run additional tournament rounds
- Complete research when sufficient

**Supervisor decision-making:**
```
Current state:
- 8 hypotheses generated
- 16 tournament matches played
- Top ELO: 1450
- 2 semantic communities identified

Decision: evolve_hypotheses
Reasoning: "Top hypotheses show promise but need refinement based on tournament feedback..."
```

### Phase 7: Final Report (1-3 minutes)
Comprehensive report including:
- Executive summary
- Top 3 hypotheses with detailed analysis
- Evidence synthesis
- Future research recommendations

---

## 🔧 Customization Options

### Custom Configuration

```python
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

# Use specific models for different agents
config = CoscientistConfig(
    # Use GPT-4 for generation
    generation_agent_llms={
        "gpt-4": ChatOpenAI(model="gpt-4", max_tokens=50_000)
    },
    
    # Claude for supervision
    supervisor_agent_llm=ChatAnthropic(
        model="claude-sonnet-4-20250514", 
        max_tokens=50_000
    ),
    
    # Custom specialist fields
    specialist_fields=["immunology", "nutrition", "molecular biology"]
)
```

### Step-by-Step Execution

Instead of running the full pipeline, you can control each phase:

```python
import asyncio
from coscientist.framework import CoscientistConfig, CoscientistFramework
from coscientist.global_state import CoscientistState, CoscientistStateManager

async def manual_research():
    # Initialize
    goal = "Your research question here"
    state = CoscientistState(goal=goal)
    config = CoscientistConfig()
    state_manager = CoscientistStateManager(state)
    cosci = CoscientistFramework(config, state_manager)
    
    # Step 1: Start with initial hypotheses and tournament
    await cosci.start(n_hypotheses=6)
    print("Initial tournament complete!")
    
    # Step 2: Generate more hypotheses
    await cosci.generate_new_hypotheses(n_hypotheses=4)
    print("New hypotheses generated!")
    
    # Step 3: Run tournament with new hypotheses
    await cosci.run_tournament(k_bracket=8)
    print("Tournament updated!")
    
    # Step 4: Get meta-review
    await cosci.run_meta_review(k_bracket=8)
    print("Meta-review complete!")
    
    # Step 5: Evolve top hypotheses
    await cosci.evolve_hypotheses(n_hypotheses=4)
    print("Hypotheses evolved!")
    
    # Step 6: Final tournament and report
    await cosci.run_tournament(k_bracket=8)
    await cosci.finish()
    print("Research complete!")
    
    return state_manager.final_report, state_manager.meta_review

asyncio.run(manual_research())
```

### Resuming Research

If your research is interrupted, you can resume from the last checkpoint:

```python
from coscientist.global_state import CoscientistState

# Load the most recent state
goal = "Your original research question"
loaded_state = CoscientistState.load_latest(goal=goal)

if loaded_state:
    print(f"Resumed from iteration {loaded_state._iteration}")
    state_manager = CoscientistStateManager(loaded_state)
    cosci = CoscientistFramework(config, state_manager)
    
    # Continue research
    final_report, meta_review = await cosci.run()
else:
    print("No saved state found - starting fresh")
```

---

## 📊 Viewing Results

### Option 1: Streamlit Dashboard (Recommended)

```bash
cd app
pip install -r viewer_requirements.txt
streamlit run tournament_viewer.py
```

**Features:**
- Interactive tournament rankings
- Hypothesis comparison
- Semantic proximity graphs
- Meta-review visualization
- Supervisor decision logs

### Option 2: Python Analysis

```python
from coscientist.global_state import CoscientistState

# Load your results
state = CoscientistState.load_latest(goal="Your research question")

# Access different components
print("Literature Review:", state.literature_review)
print("Total Hypotheses:", len(state.tournament.hypotheses))
print("Top Hypothesis:", state.tournament.get_sorted_hypotheses()[0])

# Analyze tournament
for uid, rating in state.tournament.get_sorted_hypotheses()[:5]:
    hypothesis = state.tournament.hypotheses[uid]
    print(f"\nELO {rating:.0f}: {hypothesis.prediction}")
    print(f"Reasoning: {hypothesis.reasoning}")

# View match history
matches = state.tournament.matches
print(f"\nTotal matches played: {len(matches)}")
```

### Option 3: Direct File Access

Results are saved as pickle files in `~/.coscientist/<goal_hash>/`

```python
import pickle

# Load the latest checkpoint
with open('path/to/checkpoint.pkl', 'rb') as f:
    state = pickle.load(f)

# Access any component
print(state.final_report)
print(state.meta_reviews[-1])
```

---

## 💡 Tips for Best Results

### Crafting Good Research Questions

**✅ Good examples:**
- "How does sleep deprivation affect cognitive function in adults?"
- "What mechanisms link the gut microbiome to depression?"
- "Can CRISPR gene therapy treat sickle cell disease safely?"

**❌ Avoid:**
- Too broad: "What causes cancer?" (too general)
- Non-scientific: "Is astrology real?" (not scientifically answerable)
- Opinion-based: "What's the best diet?" (subjective)

### Optimizing Performance

1. **API Rate Limits**: The system makes many API calls. If you hit rate limits:
   - Use the step-by-step approach with delays
   - Consider upgrading API tier
   - Use fewer models in configuration

2. **Cost Management**: Full research can cost $5-20 depending on models used:
   - Use Gemini Flash for cheaper runs
   - Reduce number of hypotheses
   - Use simpler reasoning strategies

3. **Quality vs Speed**:
   - More hypotheses = better coverage but slower
   - More tournament rounds = better rankings but more expensive
   - Balance based on your needs

### Interpreting Results

- **ELO ratings > 1400**: Strong hypotheses worth pursuing
- **ELO ratings 1200-1400**: Decent hypotheses, need refinement
- **ELO ratings < 1200**: Weaker hypotheses, less promising

- **Semantic communities**: Show different research directions
- **Debate transcripts**: Explain why hypotheses are ranked as they are
- **Meta-reviews**: Provide the big picture synthesis

---

## 🐛 Troubleshooting

### Common Issues

**"API key not found"**
```bash
# Make sure all keys are set
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."
export TAVILY_API_KEY="tvly-..."
```

**"Directory already exists"**
```python
# Clear old results for the same question
CoscientistState.clear_goal_directory("Your research question")

# Or load existing results
state = CoscientistState.load_latest(goal="Your research question")
```

**"Rate limit exceeded"**
- Wait a few minutes and resume
- Upgrade API tier
- Use fewer concurrent operations

**"Out of memory"**
- The system can handle 20-30 hypotheses
- For larger research, results will be truncated
- Consider running on a machine with more RAM

---

## 📚 Further Reading

- [Main README](../README.md) - Project overview
- [Framework Documentation](../coscientist/framework.py) - Core system details
- [Tournament Viewer Guide](../app/README_tournament_viewer.md) - Web interface
- [DeepMind Paper](https://arxiv.org/abs/2502.18864) - Original research inspiration

---

## 🤝 Contributing

Have ideas for better examples? Found issues? Contributions welcome!

1. Fork the repository
2. Create your example
3. Submit a pull request

**Example ideas we'd love:**
- Domain-specific examples (chemistry, physics, etc.)
- Integration with experimental data
- Custom visualization scripts
- Optimization strategies
