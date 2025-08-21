# Neo4jGraph API Reference

## Class: langchain_community.graphs.neo4j_graph.Neo4jGraph

> **Deprecated since version 0.3.8**: Use `langchain_neo4j.Neo4jGraph` instead. It will not be removed until langchain-community==1.0.

Neo4j database wrapper for various graph operations.

### Constructor

```python
Neo4jGraph(
    url: str | None = None,
    username: str | None = None,
    password: str | None = None,
    database: str | None = None,
    timeout: float | None = None,
    sanitize: bool = False,
    refresh_schema: bool = True,
    *,
    driver_config: Dict | None = None,
    enhanced_schema: bool = False,
)
```

Create a new Neo4j graph wrapper instance.

#### Parameters

- **url** (`str | None`): The URL of the Neo4j database server
- **username** (`str | None`): The username for database authentication
- **password** (`str | None`): The password for database authentication
- **database** (`str | None`): The name of the database to connect to. Default is 'neo4j'
- **timeout** (`float | None`): The timeout for transactions in seconds. Useful for terminating long-running queries. By default, there is no timeout set
- **sanitize** (`bool`): A flag to indicate whether to remove lists with more than 128 elements from results. Useful for removing embedding-like properties from database responses. Default is False
- **refresh_schema** (`bool`): A flag whether to refresh schema information at initialization. Default is True
- **enhanced_schema** (`bool`): A flag whether to scan the database for example values and use them in the graph schema. Default is False
- **driver_config** (`Dict | None`): Configuration passed to Neo4j Driver

#### Security Note

Make sure that the database connection uses credentials that are narrowly-scoped to only include necessary permissions. Failure to do so may result in data corruption or loss, since the calling code may attempt commands that would result in deletion, mutation of data if appropriately prompted or reading sensitive data if such data is present in the database. The best way to guard against such negative outcomes is to (as appropriate) limit the permissions granted to the credentials used with this tool.

See [https://python.langchain.com/docs/security](https://python.langchain.com/docs/security) for more information.

### Attributes

- **get_schema**: Returns the schema of the Graph
- **get_structured_schema**: Returns the structured schema of the Graph

### Methods

#### add_graph_documents()

```python
add_graph_documents(
    graph_documents: List[GraphDocument],
    include_source: bool = False,
    baseEntityLabel: bool = False,
) -> None
```

This method constructs nodes and relationships in the graph based on the provided GraphDocument objects.

##### Parameters

- **graph_documents** (`List[GraphDocument]`): A list of GraphDocument objects that contain the nodes and relationships to be added to the graph. Each GraphDocument should encapsulate the structure of part of the graph, including nodes, relationships, and the source document information
- **include_source** (`bool`, optional): If True, stores the source document and links it to nodes in the graph using the MENTIONS relationship. This is useful for tracing back the origin of data. Merges source documents based on the id property from the source document metadata if available; otherwise it calculates the MD5 hash of page_content for merging process. Defaults to False
- **baseEntityLabel** (`bool`, optional): If True, each newly created node gets a secondary `__Entity__` label, which is indexed and improves import speed and performance. Defaults to False

##### Returns

None

#### query()

```python
query(
    query: str,
    params: dict = {},
) -> List[Dict[str, Any]]
```

Query Neo4j database.

##### Parameters

- **query** (`str`): The Cypher query to execute
- **params** (`dict`): The parameters to pass to the query

##### Returns

- **List[Dict[str, Any]]**: The list of dictionaries containing the query results

#### refresh_schema()

```python
refresh_schema() -> None
```

Refreshes the Neo4j graph schema information.

## Usage Example

```python
from langchain_community.graphs import Neo4jGraph

# Initialize the graph
graph = Neo4jGraph(
    url="bolt://localhost:7687",
    username="neo4j",
    password="password",
    database="neo4j"
)

# Query the database
result = graph.query("MATCH (n) RETURN n LIMIT 10")

# Add graph documents
graph.add_graph_documents(
    graph_documents=my_graph_documents,
    include_source=True,
    baseEntityLabel=True
)
```