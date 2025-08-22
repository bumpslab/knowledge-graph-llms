# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit-based knowledge graph application that extracts entities and relationships from text using LangChain and stores them in Neo4j. The application uses OpenRouter API for LLM access instead of direct OpenAI integration, providing flexibility to use various models including free tiers.

## Key Architecture Components

- **app.py**: Main Streamlit application with sidebar controls for input methods, Neo4j storage options, and accumulated graph visualization
- **generate_knowledge_graph.py**: Core logic containing:
  - `extract_graph_data()`: Async function using LLMGraphTransformer to convert text to graph documents
  - `visualize_graph()`: PyVis network visualization with physics-based layout
  - `store_graph_in_neo4j()`: Neo4j storage with metadata enhancement
  - `get_accumulated_graph_visualization()`: Retrieves and visualizes all stored knowledge across documents
- **OpenRouter Integration**: Uses ChatOpenAI with custom base URL pointing to OpenRouter API (`https://openrouter.ai/api/v1`)

## Development Commands

### Environment Setup
```bash
# Install dependencies using uv (recommended)
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt

# Set up environment variables (copy and modify .env.example)
cp .env.example .env
```

### Running the Application
```bash
# Start Streamlit development server
streamlit run app.py

# The app will be available at http://localhost:8501
```

### Environment Configuration
Required environment variables in `.env`:
- `OPENROUTER_API_KEY`: API key for OpenRouter service
- `NEO4J_URI`: Neo4j database connection string (e.g., bolt://localhost:7687)
- `NEO4J_USERNAME`: Neo4j username
- `NEO4J_PASSWORD`: Neo4j password

## Key Technical Details

### LLM Model Configuration
- Currently uses `microsoft/mai-ds-r1:free` model through OpenRouter
- Temperature set to 0 for consistent extraction results
- Model can be changed by modifying the `model_name` parameter in `generate_knowledge_graph.py`

### Data Flow
1. Text input (file upload or manual entry) → 
2. LLMGraphTransformer extracts entities/relationships → 
3. Optional storage in Neo4j with metadata (source document, timestamp) → 
4. PyVis visualization with interactive features

### Neo4j Integration
- Global connection pooling with lazy initialization
- Metadata enhancement: adds `source_document` and `created_at` to nodes
- Accumulated graph feature: combines knowledge from multiple documents
- Error handling for connection failures

### Visualization Features
- Dark theme with customizable physics parameters
- Node filtering and edge validation
- Interactive controls (drag, zoom, hover tooltips)
- Filter menu for exploring large graphs
- Export to standalone HTML files

## File Structure Notes

- `assets/`: Screenshots and images for documentation
- `*.html`: Generated graph visualizations (created at runtime)
- `knowledge_graph.md`: LangChain documentation for graph construction patterns
- `neo4jgraph.md`: Additional Neo4j-specific documentation
- Korean README.md with comprehensive setup instructions

## Testing the Application

To verify the application works:
1. Ensure Neo4j is running and accessible
2. Set valid environment variables
3. Run `streamlit run app.py`
4. Test with sample text input to generate a basic graph
5. Verify Neo4j storage by checking the "Show Accumulated Graph" feature