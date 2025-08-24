# 지식 그래프 구축 방법

> **참조:**
> - [https://python.langchain.com/docs/how_to/graph_constructing/](https://python.langchain.com/docs/how_to/graph_constructing/)

이 가이드는 비정형 텍스트에서 지식 그래프를 구축하는 기본적인 방법들을 다룹니다. 구축된 그래프는 RAG 애플리케이션에서 지식 베이스 역할을 합니다.

## 보안 참고사항

지식 그래프 구축에는 데이터베이스에 대한 쓰기 권한이 필요합니다. 이는 본질적인 위험을 수반합니다. 데이터를 가져오기 전에 검증하고 확인하세요. 일반적인 보안 모범 사례는 보안 문서를 참조하시기 바랍니다.

## 아키텍처

높은 수준에서, 텍스트로부터 지식 그래프를 구축하는 과정은 다음 단계들을 포함합니다:

- **텍스트에서 구조화된 정보 추출**: 모델이 텍스트에서 구조화된 그래프 정보를 추출합니다
- **그래프 데이터베이스에 저장**: 추출된 구조화된 그래프 정보를 그래프 데이터베이스에 저장하여 하위 RAG 애플리케이션을 활성화합니다

## 설정

먼저 필요한 패키지를 설치하고 환경 변수를 설정합니다. 이 예시는 Neo4j 그래프 데이터베이스를 사용합니다.

```bash
%pip install --upgrade --quiet langchain langchain-neo4j langchain-openai langchain-experimental neo4j
```

이 가이드는 기본적으로 OpenAI 모델을 사용합니다.

```python
import getpass
import os

os.environ["OPENAI_API_KEY"] = getpass.getpass()

# LangSmith를 사용하려면 아래 주석을 해제하세요. 필수는 아닙니다.
# os.environ["LANGSMITH_API_KEY"] = getpass.getpass()
# os.environ["LANGSMITH_TRACING"] = "true"
```

다음으로, Neo4j 자격 증명과 연결을 정의합니다. Neo4j 데이터베이스를 설정하려면 Neo4j 설치 단계를 따르세요.

```python
import os
from langchain_neo4j import Neo4jGraph

os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "password"

graph = Neo4jGraph(refresh_schema=False)
```

## LLM 그래프 변환기

텍스트에서 그래프 데이터를 추출하는 것은 비정형 정보를 구조화된 형식으로 변환합니다. 이는 복잡한 관계와 패턴을 통해 더 깊은 통찰력과 보다 효율적인 탐색을 가능하게 합니다. `LLMGraphTransformer`는 LLM을 사용하여 엔터티와 그들의 관계를 분석하고 분류함으로써 텍스트 문서를 구조화된 그래프 문서로 변환합니다. LLM 모델 선택은 추출된 그래프 데이터의 정확성과 뉘앙스 파악에 상당한 영향을 미칩니다.

```python
import os
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo")
llm_transformer = LLMGraphTransformer(llm=llm)
```

이제 예시 텍스트를 전달하고 결과를 살펴볼 수 있습니다.

```python
from langchain_core.documents import Document

text = """
Marie Curie, born in 1867, was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity.
She was the first woman to win a Nobel Prize, the first person to win a Nobel Prize twice, and the only person to win a Nobel Prize in two scientific fields.
Her husband, Pierre Curie, was a co-winner of her first Nobel Prize, making them the first-ever married couple to win the Nobel Prize and launching the Curie family legacy of five Nobel Prizes.
She was, in 1906, the first woman to become a professor at the University of Paris.
"""

documents = [Document(page_content=text)]
graph_documents = await llm_transformer.aconvert_to_graph_documents(documents)

print(f"노드:{graph_documents[0].nodes}")
print(f"관계:{graph_documents[0].relationships}")
```

출력:
```
노드:[Node(id='Marie Curie', type='Person', properties={}), Node(id='Pierre Curie', type='Person', properties={}), Node(id='University Of Paris', type='Organization', properties={})]
관계:[Relationship(source=Node(id='Marie Curie', type='Person', properties={}), target=Node(id='Pierre Curie', type='Person', properties={}), type='MARRIED', properties={}), Relationship(source=Node(id='Marie Curie', type='Person', properties={}), target=Node(id='University Of Paris', type='Organization', properties={}), type='PROFESSOR', properties={})]
```

LLM을 사용하므로 그래프 구축 과정은 비결정적입니다. 각 실행에서 약간 다른 결과를 얻을 수 있습니다.

요구사항에 따라 추출할 특정 노드 유형과 관계를 정의할 수 있습니다.

```python
llm_transformer_filtered = LLMGraphTransformer(
    llm=llm,
    allowed_nodes=["Person", "Country", "Organization"],
    allowed_relationships=["NATIONALITY", "LOCATED_IN", "WORKED_AT", "SPOUSE"],
)

graph_documents_filtered = await llm_transformer_filtered.aconvert_to_graph_documents(
    documents
)

print(f"노드:{graph_documents_filtered[0].nodes}")
print(f"관계:{graph_documents_filtered[0].relationships}")
```

출력:
```
노드:[Node(id='Marie Curie', type='Person', properties={}), Node(id='Pierre Curie', type='Person', properties={}), Node(id='University Of Paris', type='Organization', properties={})]
관계:[Relationship(source=Node(id='Marie Curie', type='Person', properties={}), target=Node(id='Pierre Curie', type='Person', properties={}), type='SPOUSE', properties={}), Relationship(source=Node(id='Marie Curie', type='Person', properties={}), target=Node(id='University Of Paris', type='Organization', properties={}), type='WORKED_AT', properties={})]
```

그래프 스키마를 더 정확하게 정의하려면 관계에 대해 세 개 요소 접근법을 사용하세요. 각 튜플은 소스 노드, 관계 유형, 타겟 노드의 세 가지 요소로 구성됩니다.

```python
allowed_relationships = [
    ("Person", "SPOUSE", "Person"),
    ("Person", "NATIONALITY", "Country"),
    ("Person", "WORKED_AT", "Organization"),
]

llm_transformer_tuple = LLMGraphTransformer(
    llm=llm,
    allowed_nodes=["Person", "Country", "Organization"],
    allowed_relationships=allowed_relationships,
)

graph_documents_filtered = await llm_transformer_tuple.aconvert_to_graph_documents(
    documents
)

print(f"노드:{graph_documents_filtered[0].nodes}")
print(f"관계:{graph_documents_filtered[0].relationships}")
```

출력:
```
노드:[Node(id='Marie Curie', type='Person', properties={}), Node(id='Pierre Curie', type='Person', properties={}), Node(id='University Of Paris', type='Organization', properties={})]
관계:[Relationship(source=Node(id='Marie Curie', type='Person', properties={}), target=Node(id='Pierre Curie', type='Person', properties={}), type='SPOUSE', properties={}), Relationship(source=Node(id='Marie Curie', type='Person', properties={}), target=Node(id='University Of Paris', type='Organization', properties={}), type='WORKED_AT', properties={})]
```

## 노드 속성

`node_properties` 매개변수는 노드 속성 추출을 활성화하여 더 상세한 그래프를 만듭니다. `True`로 설정하면 LLM이 자율적으로 관련 노드 속성을 식별하고 추출합니다. `node_properties`가 문자열 리스트로 정의되면 LLM은 텍스트에서 지정된 속성만을 선택적으로 검색합니다.

```python
llm_transformer_props = LLMGraphTransformer(
    llm=llm,
    allowed_nodes=["Person", "Country", "Organization"],
    allowed_relationships=["NATIONALITY", "LOCATED_IN", "WORKED_AT", "SPOUSE"],
    node_properties=["born_year"],
)

graph_documents_props = await llm_transformer_props.aconvert_to_graph_documents(
    documents
)

print(f"노드:{graph_documents_props[0].nodes}")
print(f"관계:{graph_documents_props[0].relationships}")
```

출력:
```
노드:[Node(id='Marie Curie', type='Person', properties={'born_year': '1867'}), Node(id='Pierre Curie', type='Person', properties={}), Node(id='University Of Paris', type='Organization', properties={}), Node(id='Poland', type='Country', properties={}), Node(id='France', type='Country', properties={})]
관계:[Relationship(source=Node(id='Marie Curie', type='Person', properties={}), target=Node(id='Poland', type='Country', properties={}), type='NATIONALITY', properties={}), Relationship(source=Node(id='Marie Curie', type='Person', properties={}), target=Node(id='France', type='Country', properties={}), type='NATIONALITY', properties={}), Relationship(source=Node(id='Marie Curie', type='Person', properties={}), target=Node(id='Pierre Curie', type='Person', properties={}), type='SPOUSE', properties={}), Relationship(source=Node(id='Marie Curie', type='Person', properties={}), target=Node(id='University Of Paris', type='Organization', properties={}), type='WORKED_AT', properties={})]
```

## 그래프 데이터베이스에 저장

생성된 그래프 문서는 `add_graph_documents` 메서드를 사용하여 그래프 데이터베이스에 저장할 수 있습니다.

```python
graph.add_graph_documents(graph_documents_props)
```

대부분의 그래프 데이터베이스는 데이터 가져오기와 검색을 최적화하기 위해 인덱스를 지원합니다. 모든 노드 레이블을 미리 알 수 없기 때문에 `baseEntityLabel` 매개변수를 사용하여 각 노드에 보조 기본 레이블을 추가하여 이를 처리할 수 있습니다.

```python
graph.add_graph_documents(graph_documents, baseEntityLabel=True)
```

마지막 옵션은 추출된 노드와 관계에 대한 소스 문서를 가져오는 것입니다. 이 접근법을 통해 각 엔터티가 어떤 문서에 나타났는지 추적할 수 있습니다.

```python
graph.add_graph_documents(graph_documents, include_source=True)
```

이 시각화에서 소스 문서는 파란색으로 강조 표시되며, 여기에서 추출된 모든 엔터티가 `MENTIONS` 관계로 연결됩니다.