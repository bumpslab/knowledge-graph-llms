# 프로젝트 구조

## 디렉토리 트리 구조

```
knowledge-graph-llms/
├── .github/
│   └── copilot-instructions.md       # GitHub Copilot 지침
├── component_explanation/           # 컴포넌트 설명 문서
│   ├── langchain.md                # LangChain 설명
│   ├── neo4j.md                   # Neo4j 설명
│   ├── openrouter.md              # OpenRouter 설명
│   └── streamlit.md               # Streamlit 설명
├── .env                              # 환경 변수 (실제 API 키)
├── .env.example                      # 환경 변수 템플릿
├── .gitignore                        # Git 무시 파일 설정
├── CLAUDE.md                         # Claude Code 작업 지침서
├── LICENSE                           # 라이센스 파일
├── README.md                         # 프로젝트 설명서 (한국어)
├── app.py                           # Streamlit 메인 웹 애플리케이션
├── generate_knowledge_graph.py      # 지식 그래프 생성 핵심 로직
├── knowledge_graph.ipynb           # Jupyter 노트북 (프로토타입)
├── knowledge_graph.md              # LangChain 그래프 변환 문서
├── neo4jgraph.md                   # Neo4j 그래프 관련 문서
├── requirements.txt                  # Python 의존성 패키지 목록
└── assets/                         # 스크린샷 및 이미지 자산 (11개 파일)
```

## 파일별 상세 설명

### 핵심 실행 파일

#### `app.py`
- **역할**: Streamlit 기반 웹 애플리케이션의 메인 엔트리포인트
- **기능**:
  - 사용자 인터페이스 구성 (파일 업로드, 텍스트 입력)
  - 사이드바를 통한 설정 제어 (Neo4j 저장 옵션)
  - 그래프 시각화 임베딩
  - 누적 그래프 조회 기능
- **실행**: `streamlit run app.py`

#### `generate_knowledge_graph.py`
- **역할**: 지식 그래프 생성 및 관리의 핵심 로직
- **주요 함수**:
  - `extract_graph_data()`: LLM을 통한 비동기 그래프 데이터 추출
  - `visualize_graph()`: PyVis를 사용한 인터랙티브 시각화
  - `store_graph_in_neo4j()`: Neo4j 데이터베이스 저장
  - `get_accumulated_graph_visualization()`: 누적 그래프 조회
- **외부 API 통합**: OpenRouter를 통한 LLM 접근

### 설정 및 환경 파일

#### `.env` / `.env.example`
- **역할**: 환경 변수 관리 (API 키, 데이터베이스 연결 정보)
- **포함 변수**:
  - `OPENROUTER_API_KEY`: OpenRouter API 키
  - `NEO4J_URI`: Neo4j 연결 URL
  - `NEO4J_USERNAME`, `NEO4J_PASSWORD`: Neo4j 인증 정보

#### `requirements.txt`
- **역할**: Python 의존성 패키지 목록
- **주요 패키지**:
  - `streamlit`: 웹 애플리케이션 프레임워크
  - `langchain`: LLM 통합 프레임워크
  - `langchain-openai`: OpenAI API 통합
  - `langchain-experimental`: 실험적 기능 (그래프 변환)
  - `langchain-neo4j`: Neo4j 통합
  - `pyvis`: 네트워크 시각화 라이브러리
  - `python-dotenv`: 환경 변수 관리

### 문서화 파일

#### `README.md`
- 프로젝트 전체 개요 및 설치/실행 가이드 (한국어)
- 설치 방법, API 키 설정, 사용법, 스크린샷

#### `CLAUDE.md`
- Claude Code AI 어시스턴트를 위한 작업 지침서
- 프로젝트 아키텍처, 개발 명령어, 기술적 세부사항

#### `knowledge_graph.md`
- LangChain의 그래프 변환 패턴 및 구조 문서화

#### `neo4jgraph.md`
- Neo4j 그래프 데이터베이스 특화 문서

### 컴포넌트 설명 문서

#### `component_explanation/`
프로젝트의 주요 기술 컴포넌트들에 대한 심화 설명 디렉토리

- **`streamlit.md`**: 웹 애플리케이션 프레임워크 역할과 필요성
- **`langchain.md`**: LLM 통합 및 그래프 변환 프레임워크 분석
- **`neo4j.md`**: 그래프 데이터베이스의 역할과 GraphRAG 기능
- **`openrouter.md`**: 통합 AI 모델 접근 플랫폼의 이점과 활용

### 프로토타입 파일

#### `knowledge_graph.ipynb`
- Jupyter 노트북 형태의 프로토타입 및 실험 환경
- 알고리즘 테스트, 데이터 분석, 시각화 실험

### 자산 파일

#### `assets/`
- 프로젝트 문서화를 위한 스크린샷 및 이미지 자산 (11개 파일)
- API 키 설정, 환경 구성, Neo4j 연결, GitHub 설정 관련 이미지

### 출력 및 시각화 파일

#### `knowledge_graph.html`
- **역할**: 개별 문서에서 추출된 지식 그래프의 인터랙티브 시각화
- **특징**: PyVis로 생성된 물리 기반 네트워크 레이아웃
- **자동 생성**: 텍스트 처리 시마다 업데이트

#### `accumulated_knowledge_graph.html`
- **역할**: Neo4j에 저장된 모든 문서의 통합 지식 그래프 시각화
- **특징**: 여러 문서의 지식을 연결한 누적 네트워크
- **메타데이터**: 소스 문서, 생성 시간 등 포함

## 데이터 흐름

1. **입력**: 사용자가 `app.py`를 통해 텍스트 또는 파일 업로드
2. **처리**: `generate_knowledge_graph.py`에서 OpenRouter/LangChain을 통한 LLM 호출
3. **추출**: LLMGraphTransformer가 텍스트에서 엔티티와 관계 추출
4. **저장**: 옵션에 따라 Neo4j 데이터베이스에 그래프 데이터 저장
5. **시각화**: PyVis를 통한 인터랙티브 네트워크 그래프 생성
6. **출력**: HTML 파일로 시각화 결과 저장 및 웹 표시

## 기술 스택 요약

- **Frontend**: Streamlit (Python 웹 앱)
- **Backend**: LangChain + OpenRouter (LLM 통합)
- **Database**: Neo4j (그래프 데이터베이스)
- **Visualization**: PyVis (네트워크 시각화)
- **Development**: Jupyter Notebook (프로토타이핑)
- **Deployment**: 환경 변수 기반 설정 관리