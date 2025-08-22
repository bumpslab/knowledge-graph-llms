# Knowledge Graph Generator

A Streamlit application that extract graph data (entities and relationships) from text input using LangChain and OpenRouter API, stores the graph information in Neo4j graph database and visualizes interactive graphs.
![CleanShot 2025-05-28 at 13 11 46](https://github.com/user-attachments/assets/4fef9158-8dd8-432d-bb8a-b53953a82c6c)

👉 This repo is part of Thu Vu's tutorial on Youtube:
[![](https://img.youtube.com/vi/O-T_6KOXML4/0.jpg)](https://www.youtube.com/watch?v=O-T_6KOXML4)

## Features

- Two input methods: text upload (.txt files) or direct text input
- Interactive knowledge graph visualization
- Customizable graph display with physics-based layout
- Entity relationship extraction powered by LLMs provided by OpenRouter API

## Installation
We recommend using uv to install the dependencies. Install uv and activate your virtual environment.
Installing uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Creating and activating virtual environment:
```
uv venv 
source .venv/bin/activate
```

### Prerequisites

- Python 3.8 or higher (Done by Github Codespaces)
- Neo4j setup
- OpenRouter API key

### Setting up 

### Setting up Neo4j
1. Go to [https://neo4j.com/product/auradb/](https://neo4j.com/product/auradb/) and hit 'Start Free'
2. Hit 'Continue with Google', sign
3. Go through each step and fill in information needed
4. Hit 'Create instance'
5. Hit 'Download to Continue'
![Alt text](./assets/neo4j_setup.png)
6. Check if .txt file is in your 'Downloads' directory

### Getting OpenRouter API key

1. Sign in via github at [https://openrouter.ai/](https://openrouter.ai/)
2. Click Authorize OpenRouterTeam
3. Click on the top right corner icon, and click on 'Keys'
![Alt text](./assets/openrouter_1.png)
4. Click on 'Create API Key'
![Alt text](./assets/CreateAPIKey.png)
5. Fill in Name, set credit limit to 0 and hit 'Create'
![Alt text](./assets/createapikey_2.png)
6. Copy the API Key and save it somewhere easily accessible. Do not share with other people
![Alt text](./assets/saveapikey.png)

### Dependencies

The application requires the following Python packages:

- langchain (>= 0.1.0): Core LLM framework
- langchain-experimental (>= 0.0.45): Experimental LangChain features
- langchain-openai (>= 0.1.0): OpenAI integration for LangChain
- langchain-neo4j: Neo4j integration for LangChain
- python-dotenv (>= 1.0.0): Environment variable support
- pyvis (>= 0.3.2): Graph visualization
- streamlit (>= 1.32.0): Web UI framework

Install all required dependencies using the provided requirements.txt file:

```bash
uv pip install -r requirements.txt
```

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/bumpslab/knowledge-graph-llms.git
   ```

   Note: Replace `[repository-url]` with the actual URL of this repository.

2. Create a `.env` file in the root directory with your OpenRouter API key, Neo4j uri and credentials:
   ```
   OPENROUTER_API_KEY=your_openai_api_key_here
   NEO4J_URI=your_neo4j_url_here
   NEO4J_USERNAME=your_neo4j_username_here
   NEO4J_PASSWORD=your_neo4j_password_here
   ```

## Running the Application

To run the Streamlit app:

```bash
streamlit run app.py
```

This will start the application and open it in your default web browser (typically at http://localhost:8501).

## Usage

1. Choose your input method from the sidebar (Upload txt or Input text)
2. If uploading a file, select a .txt file from your computer
3. If using direct input, type or paste your text into the text area
4. Click the "Generate Knowledge Graph" button
5. Wait for the graph to be generated (this may take a few moments depending on the length of the text)
6. Explore the interactive knowledge graph:
   - Drag nodes to rearrange the graph
   - Hover over nodes and edges to see additional information
   - Zoom in/out using the mouse wheel
   - Filter the graph for specific nodes and edges.

## How It Works

The application uses LangChain's experimental graph transformers with OpenAI's GPT-4o model to:
1. Extract entities from the input text
2. Identify relationships between these entities
3. Generate a graph structure representing this information
4. Visualize the graph using PyVis, a Python interface for the vis.js visualization library

## License

This project is licensed under the MIT License - a permissive open source license that allows for free use, modification, and distribution of the software.

For more details, see the [MIT License](https://opensource.org/licenses/MIT) documentation.
