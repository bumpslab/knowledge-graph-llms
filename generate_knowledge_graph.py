from llm_graph_transformer import LLMGraphTransformer
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pyvis.network import Network
from langchain_neo4j import Neo4jGraph
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
import os
import asyncio
import threading
from kg_config import EXTRACTION_CONFIG, BIOMEDICAL_ENTITIES, BIOMEDICAL_RELATIONSHIPS
from langchain_core.prompts import ChatPromptTemplate

# Load the .env file
load_dotenv()
# Get API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")

neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
neo4j_username = os.getenv("NEO4J_USERNAME", "neo4j")
neo4j_password = os.getenv("NEO4J_PASSWORD", "password")

def create_llm_instance():
    """Create a new LLM instance for each request to avoid connection issues."""
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=api_key
    )

# LLMGraphTransformer의 시스템 프롬프트
system_prompt = (
    "# Knowledge Graph Instructions for GPT-4\n"
    "## 1. Overview\n"
    "You are a top-tier algorithm designed for extracting information in structured "
    "formats to build a knowledge graph.\n"
    "You are also an expert in biomedical domain knowledge.\n"
    "You have the ability to understand and reason what entities and relationships are important."
    "Try to capture as much information from the text as possible without "
    "sacrificing accuracy. Do not add any information that is not explicitly "
    "mentioned in the text.\n"
    "- **Nodes** represent entities and concepts.\n"
    "- The aim is to achieve simplicity and clarity in the knowledge graph, making it\n"
    "accessible for a vast audience.\n"
    "## 2. Labeling Nodes\n"
    "- **Consistency**: Ensure you use available types for node labels.\n"
    "Ensure you use basic or elementary types for node labels.\n"
    "- For example, when you identify an entity representing a person, "
    "always label it as **'person'**. Avoid using more specific terms "
    "like 'mathematician' or 'scientist'."
    "- **Node IDs**: Never utilize integers as node IDs. Node IDs should be "
    "names or human-readable identifiers found in the text.\n"
    "- **Relationships** represent connections between entities or concepts.\n"
    "Ensure consistency and generality in relationship types when constructing "
    "knowledge graphs. Instead of using specific and momentary types "
    "such as 'BECAME_PROFESSOR', use more general and timeless relationship types "
    "like 'PROFESSOR'. Make sure to use general and timeless relationship types!\n"
    "## 3. Coreference Resolution\n"
    "- **Maintain Entity Consistency**: When extracting entities, it's vital to "
    "ensure consistency.\n"
    'If an entity, such as "John Doe", is mentioned multiple times in the text '
    'but is referred to by different names or pronouns (e.g., "Joe", "he"),'
    "always use the most complete identifier for that entity throughout the "
    'knowledge graph. In this example, use "John Doe" as the entity ID.\n'
    "Remember, the knowledge graph should be coherent and easily understandable, "
    "so maintaining consistency in entity references is crucial.\n"
    "## 4. Strict Compliance\n"
    "Adhere to the rules strictly. Non-compliance will result in termination."
)

def get_final_prompt(
    additional_instructions: str = "",
) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            (
                "human",
                additional_instructions
                + " Tip: Make sure to answer in the correct format and do "
                "not include any explanations. "
                "Use the given format to extract information from the "
                "following input: {input}",
            ),
        ]
    )

def create_graph_transformer():
    """Create a new graph transformer instance for each request."""
    llm = create_llm_instance()
    my_prompt = get_final_prompt()
    
    return LLMGraphTransformer(
        llm=llm,
        allowed_nodes=BIOMEDICAL_ENTITIES,
        allowed_relationships=BIOMEDICAL_RELATIONSHIPS,
        prompt=my_prompt,
        additional_instructions="Do NOT extract author information or references, Countries etc. Only extract biomedical entities and relationships."
    )

# Initialize text splitter for chunking long documents
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ". ", ".", " ", ""],
    chunk_size=EXTRACTION_CONFIG.get("chunk_size", 1500),
    chunk_overlap=EXTRACTION_CONFIG.get("overlap", 200),
    length_function=len,
    is_separator_regex=False,
)

neo4j_graph = None  # Global variable to hold Neo4j connection

def _run_async_in_thread(coro):
    """Run an async function in a separate thread with its own event loop."""
    result = {}
    exception = {}
    
    def thread_target():
        try:
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result['value'] = loop.run_until_complete(coro)
            finally:
                loop.close()
        except Exception as e:
            exception['error'] = e
    
    # Run in a separate thread
    thread = threading.Thread(target=thread_target)
    thread.start()
    thread.join()
    
    if 'error' in exception:
        raise exception['error']
    return result.get('value', [])

# Extract graph data from input text
def extract_graph_data(text):
    """
    Extracts graph data from input text using a graph transformer.
    Automatically chunks long text to ensure better processing.

    Args:
        text (str): Input text to be processed into graph format.

    Returns:
        list: A list of GraphDocument objects containing nodes and relationships.
    """
    # Get chunk size from config
    chunk_size = EXTRACTION_CONFIG.get("chunk_size", 1500)
    max_chunks = 10  # Gemini rate limit: 10 requests per minute
    
    # Check if text needs chunking
    if len(text) > chunk_size:
        # Split text into chunks
        chunks = text_splitter.split_text(text)
        
        # Limit chunks to respect Gemini rate limits
        if len(chunks) > max_chunks:
            st.warning(f"⚠️ **Text would create {len(chunks)} chunks, limiting to {max_chunks} due to API rate limits**")
            # Calculate new chunk size to fit within limit
            new_chunk_size = len(text) // max_chunks + 1
            temp_splitter = RecursiveCharacterTextSplitter(
                separators=["\n\n", "\n", ". ", ".", " ", ""],
                chunk_size=new_chunk_size,
                chunk_overlap=EXTRACTION_CONFIG.get("overlap", 200),
                length_function=len,
                is_separator_regex=False,
            )
            chunks = temp_splitter.split_text(text)[:max_chunks]
            st.write(f"📄 **Text split into {len(chunks)} chunks** (~{new_chunk_size} chars each)")
        elif len(chunks) > 1:
            st.write(f"📄 **Text split into {len(chunks)} chunks** (~{chunk_size} chars each)")
    else:
        chunks = [text]
    
    # Create documents from chunks
    documents = []
    for i, chunk in enumerate(chunks):
        chunk_metadata = {}
        if len(chunks) > 1:
            chunk_metadata["chunk_index"] = i
            chunk_metadata["total_chunks"] = len(chunks)
        
        documents.append(Document(
            page_content=chunk,
            metadata=chunk_metadata
        ))
    
    # Extract graph from all documents at once
    try:
        if len(chunks) > 0:
            st.write(f"🔬 **Processing {len(documents)} document chunks...**")
        
        # Create a fresh graph transformer instance for this request
        transformer = create_graph_transformer()
        
        # Run async operation in a separate thread with fresh event loop
        graph_documents = _run_async_in_thread(
            transformer.aconvert_to_graph_documents(documents)
        )
        return graph_documents
        
    except Exception as e:
        st.error(f"❌ **Error processing documents:** {e}")
        return []


def visualize_graph(graph_documents):
    """
    Visualizes a knowledge graph using PyVis based on the extracted graph documents.

    Args:
        graph_documents (list): A list of GraphDocument objects with nodes and relationships.

    Returns:
        pyvis.network.Network: The visualized network graph object.
    """
    if not graph_documents:
        st.warning("⚠️ **No graph documents to visualize**")
        return None
    
    # Create network
    net = Network(height="1200px", width="100%", directed=True,
                      notebook=False, bgcolor="#222222", font_color="white", filter_menu=True, cdn_resources='remote') 

    # Collect all nodes and relationships from all graph documents
    all_nodes = []
    all_relationships = []
    
    for doc in graph_documents:
        all_nodes.extend(doc.nodes)
        all_relationships.extend(doc.relationships)
    
    # Use combined nodes and relationships
    nodes = all_nodes
    relationships = all_relationships

    # Build lookup for valid nodes
    node_dict = {node.id: node for node in nodes}
    
    # Filter out invalid edges and collect valid node IDs
    valid_edges = []
    valid_node_ids = set()
    for rel in relationships:
        if rel.source.id in node_dict and rel.target.id in node_dict:
            valid_edges.append(rel)
            valid_node_ids.update([rel.source.id, rel.target.id])

    # Track which nodes are part of any relationship
    connected_node_ids = set()
    for rel in relationships:
        connected_node_ids.add(rel.source.id)
        connected_node_ids.add(rel.target.id)

    # Add valid nodes to the graph
    for node_id in valid_node_ids:
        node = node_dict[node_id]
        try:
            net.add_node(node.id, label=node.id, title=node.type, group=node.type)
        except:
            continue  # Skip node if error occurs

    # Add valid edges to the graph
    for rel in valid_edges:
        try:
            net.add_edge(rel.source.id, rel.target.id, label=rel.type)
        except:
            continue  # Skip edge if error occurs

    # Configure graph layout and physics
    net.set_options("""
        {
            "physics": {
                "forceAtlas2Based": {
                    "gravitationalConstant": -100,
                    "centralGravity": 0.01,
                    "springLength": 200,
                    "springConstant": 0.08
                },
                "minVelocity": 0.75,
                "solver": "forceAtlas2Based"
            }
        }
    """)

    output_file = "knowledge_graph.html"
    try:
        net.save_graph(output_file)
        print(f"Graph saved to {os.path.abspath(output_file)}")
        return net
    except Exception as e:
        print(f"Error saving graph: {e}")
        return None

def store_graph_in_neo4j(graph_documents, document_name=None):
    """Store graph documents in Neo4j database"""
    try:
        graph = get_neo4j_connection()
        
        st.write("💾 **Storing graph data in Neo4j...**")
        
        # Add document metadata to nodes if document_name is provided
        if document_name:
            for doc in graph_documents:
                for node in doc.nodes:
                    if not hasattr(node, 'properties'):
                        node.properties = {}
                    node.properties['source_document'] = document_name
                    node.properties['created_at'] = datetime.now().isoformat()
        
        # Store in Neo4j
        graph.add_graph_documents(graph_documents)
        
        st.write("✅ **Graph data stored successfully in Neo4j**")
        return True
        
    except Exception as e:
        st.error(f"❌ **Error storing graph in Neo4j:** {str(e)}")
        return False
    
def generate_knowledge_graph(text, document_name=None, store_in_neo4j=True):
    """
    Generates and visualizes a knowledge graph from input text.

    This function extracts the graph data, optionally stores
    the graph in Neo4j, and visualizes the resulting graph using PyVis.

    Args:
        text (str): Input text to convert into a knowledge graph.
        document_name (str): Optional name for the document being processed.
        store_in_neo4j (bool): Whether to store the graph in Neo4j database.

    Returns:
        pyvis.network.Network: The visualized network graph object.
    """
    graph_documents = extract_graph_data(text)
    
    # Store in Neo4j if requested
    if store_in_neo4j and graph_documents:
        store_graph_in_neo4j(graph_documents, document_name)
    
    net = visualize_graph(graph_documents)
    return net

def get_neo4j_connection():
    """Get or create Neo4j connection"""
    global neo4j_graph
    if neo4j_graph is None:
        try:
            st.write("🔗 **Connecting to Neo4j database...**")
            neo4j_graph = Neo4jGraph(
                url=neo4j_uri,
                username=neo4j_username,
                password=neo4j_password
            )
            st.write("✅ **Connected to Neo4j database**")
        except Exception as e:
            st.error(f"❌ **Failed to connect to Neo4j:** {str(e)}")
            st.write("💡 **Make sure Neo4j is running and credentials are correct**")
            raise e
    return neo4j_graph

def get_accumulated_graph_visualization():
    """
    Create a visualization of the accumulated graph from Neo4j
    """
    try:
        st.write("📊 **Fetching accumulated graph from Neo4j...**")
        graph = get_neo4j_connection()
        
        # Query all nodes and relationships using internal Neo4j ID
        nodes_query = """
        MATCH (n) 
        RETURN id(n) as internal_id, n.id as id, labels(n)[0] as type, properties(n) as properties
        """
        
        relationships_query = """
        MATCH (a)-[r]->(b) 
        RETURN id(a) as source, id(b) as target, type(r) as type
        """
        
        nodes_data = graph.query(nodes_query)
        relationships_data = graph.query(relationships_query)
        
        st.write(f"📊 **Found {len(nodes_data)} nodes and {len(relationships_data)} relationships in Neo4j**")
        
        # Create PyVis network
        net = Network(height="1200px", width="100%", directed=True,
                      notebook=False, bgcolor="#222222", font_color="white", 
                      filter_menu=True, cdn_resources='remote')
        
        # Add nodes - use internal_id as unique identifier, id as display label
        for node in nodes_data:
            net.add_node(
                node['internal_id'], 
                label=node['id'], 
                title=f"Type: {node['type']}\nID: {node['id']}\nSource: {node['properties'].get('source_document', 'Unknown')}", 
                group=node['type']
            )
        
        # Add relationships
        for rel in relationships_data:
            net.add_edge(rel['source'], rel['target'], label=rel['type'])
        
        # Configure layout
        net.set_options("""
            {
                "physics": {
                    "forceAtlas2Based": {
                        "gravitationalConstant": -100,
                        "centralGravity": 0.01,
                        "springLength": 200,
                        "springConstant": 0.08
                    },
                    "minVelocity": 0.75,
                    "solver": "forceAtlas2Based"
                }
            }
        """)
        
        # Save and return
        output_file = "accumulated_knowledge_graph.html"
        net.save_graph(output_file)
        st.write(f"✅ **Accumulated graph saved to {output_file}**")
        
        return net
        
    except Exception as e:
        st.error(f"❌ **Error creating accumulated graph visualization:** {str(e)}")
        return None