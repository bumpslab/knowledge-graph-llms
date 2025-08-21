# Import necessary modules
import streamlit as st
import streamlit.components.v1 as components  # For embedding custom HTML
from generate_knowledge_graph import generate_knowledge_graph, get_accumulated_graph_visualization, store_graph_in_neo4j

# Set up Streamlit page configuration
st.set_page_config(
    page_icon=None, 
    layout="wide",  # Use wide layout for better graph display
    initial_sidebar_state="auto", 
    menu_items=None
)

# Set the title of the app
st.title("Knowledge Graph From Text")

# Sidebar section for user input method
st.sidebar.title("Input document")
input_method = st.sidebar.radio(
    "Choose an input method:",
    ["Upload txt", "Input text"],  # Options for uploading a file or manually inputting text
)

# Neo4j storage options
st.sidebar.markdown("---")
st.sidebar.title("Storage Options")
store_in_neo4j = st.sidebar.checkbox("Store in Neo4j database", value=True)

# Sidebar section for accumulated graph visualization
st.sidebar.markdown("---")
st.sidebar.title("Accumulated Graph")
if st.sidebar.button("Show Accumulated Graph"):
    with st.spinner("Loading accumulated graph from Neo4j..."):
        net = get_accumulated_graph_visualization()
        if net is not None:
            st.success("Accumulated graph loaded successfully!")
            
            # Save and display the accumulated graph
            output_file = "accumulated_knowledge_graph.html"
            net.save_graph(output_file)
            
            # Open the HTML file and display it within the Streamlit app
            HtmlFile = open(output_file, 'r', encoding='utf-8')
            components.html(HtmlFile.read(), height=1000)

# Case 1: User chooses to upload a .txt file
if input_method == "Upload txt":
    # File uploader widget in the sidebar
    uploaded_file = st.sidebar.file_uploader(label="Upload file", type=["txt"])
    
    if uploaded_file is not None:
        # Read the uploaded file content and decode it as UTF-8 text
        text = uploaded_file.read().decode("utf-8")
 
        # Button to generate the knowledge graph
        if st.sidebar.button("Generate Knowledge Graph"):
            with st.spinner("Generating knowledge graph..."):
                # Call the function to generate the graph from the text
                document_name = uploaded_file.name
                net = generate_knowledge_graph(text, document_name=document_name, store_in_neo4j=store_in_neo4j)
                st.success("Knowledge graph generated successfully!")
                
                # Save the graph to an HTML file
                output_file = "knowledge_graph.html"
                net.save_graph(output_file) 

                # Open the HTML file and display it within the Streamlit app
                HtmlFile = open(output_file, 'r', encoding='utf-8')
                components.html(HtmlFile.read(), height=1000)

# Case 2: User chooses to directly input text
else:
    # Text area for manual input
    text = st.sidebar.text_area("Input text", height=300)

    if text:  # Check if the text area is not empty
        if st.sidebar.button("Generate Knowledge Graph"):
            with st.spinner("Generating knowledge graph..."):
                # Call the function to generate the graph from the input text
                document_name = "Manual Input"
                net = generate_knowledge_graph(text, document_name=document_name, store_in_neo4j=store_in_neo4j)
                st.success("Knowledge graph generated successfully!")
                
                # Save the graph to an HTML file
                output_file = "knowledge_graph.html"
                net.save_graph(output_file) 

                # Open the HTML file and display it within the Streamlit app
                HtmlFile = open(output_file, 'r', encoding='utf-8')
                components.html(HtmlFile.read(), height=1000)