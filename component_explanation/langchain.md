# LangChain: LLM 파이프라인 구축(오케스트레이션) 프레임워크

> **참조:**
> - [https://python.langchain.com/docs/concepts/why_langchain/](https://python.langchain.com/docs/concepts/why_langchain/)
> - [https://python.langchain.com/docs/introduction/](https://python.langchain.com/docs/introduction/)

## LangChain이란 무엇인가?

**LangChain**은 대규모 언어 모델(LLM) 애플리케이션 개발을 위한 포괄적인 오픈소스 프레임워크입니다. LangChain의 핵심 목표는 "개발자가 추론 능력을 가진 애플리케이션을 최대한 쉽게 구축할 수 있도록 지원하는 것"입니다.

## LangChain의 핵심 가치

### 1. 표준화된 컴포넌트 인터페이스
- 다양한 AI 모델과 구성 요소를 위한 일관된 인터페이스 제공
- 모델 제공자(OpenAI, Anthropic, Google 등) 간 쉬운 전환 가능
- 도구 호출(tool calling)과 구조화된 출력 등 고급 기능 지원

### 2. 복잡한 애플리케이션 오케스트레이션
- LLM의 **제어 흐름 관리**
- 멀티스텝 워크플로우 구축에 용이

### 3. 관찰 가능성 및 평가
- **LangSmith**를 통해 AI 애플리케이션의 성능 모니터링 및 평가
- 프롬프트 엔지니어링과 모델 선택에 대한 통찰 제공
- 실제 운영 환경에서의 성능 추적

## 이 코드베이스에서의 LangChain 활용

### 1. 핵심 LangChain 컴포넌트 사용

```python
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_neo4j import Neo4jGraph
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llm_graph_transformer import LLMGraphTransformer
from kg_config import BIOMEDICAL_ENTITIES, BIOMEDICAL_RELATIONSHIPS
```

### 2. LLM 통합 - ChatGoogleGenerativeAI
```python
from langchain_google_genai import ChatGoogleGenerativeAI

def create_llm_instance():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=API_KEY
    )
```

**활용 방식:**
- **ChatGoogleGenerativeAI** 클래스를 사용하여 Google Gemini API 통합
- gemini-2.5-flash 모델을 사용하여 빠르고 정확한 그래프 변환
- 새로운 인스턴스를 생성하여 연결 문제 방지

### 3. 그래프 변환 - LLMGraphTransformer (커스텀)
```python
from llm_graph_transformer import LLMGraphTransformer

def create_graph_transformer():
    llm = create_llm_instance()
    prompt = get_final_prompt(additional_instructions=additional_prompt)
    
    return LLMGraphTransformer(
        llm=llm,
        allowed_nodes=BIOMEDICAL_ENTITIES,
        allowed_relationships=BIOMEDICAL_RELATIONSHIPS,
        prompt=prompt
    )

def extract_graph_data(text):
    # 텍스트 청킹 및 처리
    chunks = TEXT_SPLITTER.split_text(text) if len(text) > chunk_size else [text]
    documents = [Document(page_content=chunk) for chunk in chunks]
    
    transformer = create_graph_transformer()
    return _run_async_in_thread(transformer.aconvert_to_graph_documents(documents))
```

**활용 방식:**
- **커스텀 LLMGraphTransformer**를 사용하여 생명의학 도메인에 특화된 그래프 변환
- **사전 정의된 엔티티 및 관계 타입**으로 일관성 있는 그래프 구조 보장
- **텍스트 청킹**으로 긴 문서 처리 및 API 제한 대응
- **스레드 기반 비동기 처리**로 Streamlit과의 호환성 확보

### 4. 그래프 데이터베이스 통합 - Neo4jGraph
```python
def get_neo4j_connection():
    global neo4j_graph
    if neo4j_graph is None:
        neo4j_graph = Neo4jGraph(
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD
        )
    return neo4j_graph

def store_graph_in_neo4j(graph_documents, document_name=None):
    graph = get_neo4j_connection()
    
    # 문서 메타데이터 추가
    if document_name:
        for doc in graph_documents:
            for node in doc.nodes:
                node.properties = node.properties or {}
                node.properties['source_document'] = document_name
                node.properties['created_at'] = datetime.now().isoformat()
    
    graph.add_graph_documents(graph_documents)
```

**활용 방식:**
- **Neo4jGraph**로 Neo4j 데이터베이스와 통합
- **메타데이터 강화**: 소스 문서 및 생성 시간 정보 추가
- **전역 연결 풀링**으로 효율적인 연결 관리
- **누적 그래프 기능**: 여러 문서의 지식을 통합하여 저장

## LangChain 장점

### 1. 개발 생산성 향상
- 복잡한 LLM-그래프 변환 로직을 간단한 API로 추상화
- 다양한 데이터베이스와 모델 간 호환성 제공

### 2. 확장성과 유연성
- 새로운 LLM 모델로 쉽게 교체 가능
- 다른 그래프 데이터베이스로 마이그레이션 용이
- 추가 기능(에이전트, 체인 등) 통합 가능

## 생명의학 도메인 특화

### 1. 도메인 특화 그래프 구조
```python
# kg_config.py에서 정의된 생명의학 엔티티 및 관계
BIOMEDICAL_ENTITIES = ["Gene", "Protein", "Disease", "Drug", "Pathway", ...]
BIOMEDICAL_RELATIONSHIPS = ["REGULATES", "INTERACTS_WITH", "CAUSES", ...]
```

### 2. 맞춤형 시스템 프롬프트
```python
SYSTEM_PROMPT = (
    "You are a top-tier algorithm designed for extracting information in structured "
    "formats to build a knowledge graph.\n"
    "You are also an expert in biomedical domain knowledge.\n"
    "DO NOT use generic terms like 'Gene', 'Protein' for Node IDs.\n"
    "Use specific names or identifiers from the text, such as 'BRCA1', 'Diabetes', etc."
)
```

### 3. 청킹 전략
```python
TEXT_SPLITTER = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ". ", ".", " ", ""],
    chunk_size=1500,
    chunk_overlap=200
)
```

이 프로젝트에서 LangChain은 **생명의학 도메인에 특화된 지식 그래프 구축 플랫폼**을 제공합니다. Google Gemini의 강력한 언어 이해 능력과 결합하여 복잡한 생명의학 텍스트에서 정확한 엔티티와 관계를 추출하며, 대용량 문서 처리를 위한 청킹 및 비동기 처리를 통해 실용적인 성능을 보장합니다.

LangChain의 모듈화된 아키텍처 덕분에 다른 LLM 모델로의 전환이나 추가 기능 통합이 용이하며, 지속적으로 발전하는 생명의학 연구 분야의 요구사항에 유연하게 대응할 수 있습니다.