# Neo4jGraph API 레퍼런스

> **참조:**
> - [https://python.langchain.com/api_reference/community/graphs/langchain_community.graphs.neo4j_graph.Neo4jGraph.html](https://python.langchain.com/api_reference/community/graphs/langchain_community.graphs.neo4j_graph.Neo4jGraph.html)

## 클래스: langchain_community.graphs.neo4j_graph.Neo4jGraph

> **버전 0.3.8부터 더 이상 사용되지 않음**: `langchain_neo4j.Neo4jGraph`를 대신 사용하세요. langchain-community==1.0까지는 제거되지 않습니다.

다양한 그래프 작업을 위한 Neo4j 데이터베이스 래퍼입니다.

### 생성자

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

새로운 Neo4j 그래프 래퍼 인스턴스를 생성합니다.

#### 매개변수

- **url** (`str | None`): Neo4j 데이터베이스 서버의 URL
- **username** (`str | None`): 데이터베이스 인증을 위한 사용자명
- **password** (`str | None`): 데이터베이스 인증을 위한 비밀번호
- **database** (`str | None`): 연결할 데이터베이스의 이름. 기본값은 'neo4j'
- **timeout** (`float | None`): 초 단위 트랜잭션 타임아웃. 장시간 실행되는 쿼리를 종료하는 데 유용합니다. 기본적으로는 타임아웃이 설정되지 않습니다
- **sanitize** (`bool`): 결과에서 128개 이상의 요소를 가진 리스트를 제거할지 여부를 나타내는 플래그. 데이터베이스 응답에서 임베딩과 같은 속성을 제거하는 데 유용합니다. 기본값은 False
- **refresh_schema** (`bool`): 초기화 시 스키마 정보를 새로 고칠지 여부를 나타내는 플래그. 기본값은 True
- **enhanced_schema** (`bool`): 데이터베이스에서 예시 값을 스캔하여 그래프 스키마에 사용할지 여부를 나타내는 플래그. 기본값은 False
- **driver_config** (`Dict | None`): Neo4j 드라이버에 전달되는 구성

#### 보안 참고사항

데이터베이스 연결이 필요한 권한만을 포함하도록 좁게 범위가 제한된 자격 증명을 사용하는지 확인하세요. 그렇지 않으면 호출 코드가 적절히 프롬프트를 받을 경우 데이터의 삭제, 변경을 초래하거나 데이터베이스에 민감한 데이터가 있는 경우 이를 읽는 명령을 시도할 수 있어 데이터 손상이나 손실이 발생할 수 있습니다. 이러한 부정적인 결과를 방지하는 가장 좋은 방법은 (적절히) 이 도구와 함께 사용되는 자격 증명에 부여된 권한을 제한하는 것입니다.

자세한 정보는 [https://python.langchain.com/docs/security](https://python.langchain.com/docs/security)를 참조하세요.

### 속성

- **get_schema**: 그래프의 스키마를 반환합니다
- **get_structured_schema**: 그래프의 구조화된 스키마를 반환합니다

### 메서드

#### add_graph_documents()

```python
add_graph_documents(
    graph_documents: List[GraphDocument],
    include_source: bool = False,
    baseEntityLabel: bool = False,
) -> None
```

이 메서드는 제공된 GraphDocument 객체를 기반으로 그래프에서 노드와 관계를 구성합니다.

##### 매개변수

- **graph_documents** (`List[GraphDocument]`): 그래프에 추가할 노드와 관계를 포함하는 GraphDocument 객체의 리스트. 각 GraphDocument는 노드, 관계, 소스 문서 정보를 포함한 그래프의 일부 구조를 캡슐화해야 합니다
- **include_source** (`bool`, 선택사항): True로 설정하면 소스 문서를 저장하고 MENTIONS 관계를 사용하여 그래프의 노드에 연결합니다. 이는 데이터의 출처를 역추적하는 데 유용합니다. 소스 문서 메타데이터에서 id 속성이 있으면 이를 기반으로 소스 문서를 병합하고, 그렇지 않으면 병합 과정을 위해 page_content의 MD5 해시를 계산합니다. 기본값은 False
- **baseEntityLabel** (`bool`, 선택사항): True로 설정하면 새로 생성된 각 노드는 인덱싱되고 가져오기 속도와 성능을 향상시키는 보조 `__Entity__` 레이블을 얻습니다. 기본값은 False

##### 반환값

None

#### query()

```python
query(
    query: str,
    params: dict = {},
) -> List[Dict[str, Any]]
```

Neo4j 데이터베이스에 쿼리를 실행합니다.

##### 매개변수

- **query** (`str`): 실행할 Cypher 쿼리
- **params** (`dict`): 쿼리에 전달할 매개변수

##### 반환값

- **List[Dict[str, Any]]**: 쿼리 결과를 포함하는 딕셔너리의 리스트

#### refresh_schema()

```python
refresh_schema() -> None
```

Neo4j 그래프 스키마 정보를 새로 고칩니다.

## 사용 예시

```python
from langchain_community.graphs import Neo4jGraph

# 그래프 초기화
graph = Neo4jGraph(
    url="bolt://localhost:7687",
    username="neo4j",
    password="password",
    database="neo4j"
)

# 데이터베이스 쿼리
result = graph.query("MATCH (n) RETURN n LIMIT 10")

# 그래프 문서 추가
graph.add_graph_documents(
    graph_documents=my_graph_documents,
    include_source=True,
    baseEntityLabel=True
)
```