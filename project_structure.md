# 프로젝트 구조

## 디렉토리 트리 구조

```
knowledge-graph-llms/
├── LICENSE                            # MIT 라이선스 파일
├── README.md                          # 프로젝트 설명서 (한국어)
├── accumulated_knowledge_graph.html   # 통합 지식 그래프 시각화 (자동생성)
├── app.py                            # Streamlit 메인 웹 애플리케이션
├── biorxiv_filtered.csv              # bioRxiv 데이터셋
├── building_qa_app.md                # QA 앱 구축 가이드
├── component_explanation/            # 컴포넌트 설명 문서
│   ├── langchain.md                 # LangChain 설명
│   ├── neo4j.md                     # Neo4j 설명
│   └── streamlit.md                 # Streamlit 설명
├── generate_knowledge_graph.py       # 지식 그래프 생성 핵심 로직
├── kg_config.py                      # 지식 그래프 설정 모듈
├── knowledge_graph.html              # 개별 지식 그래프 시각화 (자동생성)
├── knowledge_graph.ipynb            # Jupyter 노트북 프로토타입
├── llm_graph_transformer.py          # LLM 그래프 변환 모듈
├── neo4jgraph.md                    # Neo4j 그래프 관련 문서
├── papers/                          # COVID-19 연구 논문 샘플
│   ├── Transcriptional_reprogramming_from_innate_immune_functions_to.txt
│   ├── role_of_genetic_variants_and_gene_expression_in_covid19.txt
│   ├── sars_cov2_vaccination_induces_mucosal_antibody_responses.txt
│   └── variant_specific_symptoms_of_covid19_in_England.txt
├── project_structure.md             # 이 파일 - 프로젝트 구조 설명
├── requirements.txt                  # Python 의존성 패키지 목록
├── sample_papers.py                 # biorxiv_filtered.csv 데이터를 이용해 ./papers/ 안에 논문 텍스트 파일 추가하는 스크립트
├── vibe.example.md                  # 개발 예제 및 가이드
└── assets/                          # 스크린샷 및 이미지 자산
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
- **외부 API 통합**: Google Gemini API를 통한 LLM 접근

### 새로운 모듈 파일들

#### `biomedical_kg_extractor.py`
- **역할**: 생의학 분야 특화 지식 그래프 추출기
- **기능**: 의료/생명과학 논문에서 특화된 엔티티 및 관계 추출

#### `kg_config.py`
- **역할**: 지식 그래프 설정 및 구성 관리
- **기능**: LLM 모델 설정, 추출 파라미터 관리

#### `llm_graph_transformer.py`
- **역할**: LLM을 통한 그래프 변환 로직
- **기능**: 텍스트를 구조화된 그래프 데이터로 변환

#### `neo4j_graph.py`
- **역할**: Neo4j 그래프 데이터베이스 전용 관리 모듈
- **기능**: Neo4j 연결, 쿼리, 데이터 저장/조회 최적화

#### `run_kg_extraction.py`
- **역할**: 배치 처리용 지식 그래프 추출 스크립트
- **기능**: 대량 문서 처리, 자동화된 추출 파이프라인

#### `sample_papers.py`
- **역할**: 샘플 논문 데이터 관리
- **기능**: 테스트용 논문 로딩, 전처리, 샘플 데이터 제공

### 데이터 및 리소스

#### `papers/`
- **역할**: COVID-19 관련 연구 논문 샘플 저장소
- **포함**: 4개의 텍스트 형태 연구 논문 파일
- **용도**: 애플리케이션 테스트 및 데모용 데이터

#### `biorxiv_filtered.csv`
- **역할**: bioRxiv 논문 메타데이터 필터링된 데이터셋
- **용도**: 대량 논문 처리 실험 및 분석

### 문서화 파일

#### `README.md`
- 프로젝트 전체 개요 및 설치/실행 가이드 (한국어)
- GitHub Codespaces, Neo4j, Google Gemini API 설정 가이드

#### `CLAUDE.md`
- Claude Code AI 어시스턴트를 위한 작업 지침서
- 프로젝트 아키텍처, 개발 명령어, 기술적 세부사항

#### `building_qa_app.md`
- **새로운 기능**: QA(질의응답) 애플리케이션 구축 가이드
- **내용**: 지식 그래프 기반 질의응답 시스템 구현 방법

#### `vibe.example.md`
- **역할**: 개발 예제 및 실습 가이드
- **내용**: 코드 고도화를 위한 실습 예제 및 개발 방향 제시

#### `neo4jgraph.md`
- Neo4j 그래프 데이터베이스 특화 문서

### 컴포넌트 설명 문서

#### `component_explanation/`
프로젝트의 주요 기술 컴포넌트들에 대한 심화 설명 디렉토리

- **`streamlit.md`**: 웹 애플리케이션 프레임워크 역할과 필요성
- **`langchain.md`**: LLM 통합 및 그래프 변환 프레임워크 분석
- **`neo4j.md`**: 그래프 데이터베이스의 역할과 GraphRAG 기능
- **`openrouter.md`**: 통합 AI 모델 접근 플랫폼의 이점과 활용

### 설정 및 환경 파일

#### `requirements.txt`
- **역할**: Python 의존성 패키지 목록
- **주요 패키지**:
  - `streamlit`: 웹 애플리케이션 프레임워크
  - `langchain`: LLM 통합 프레임워크
  - `langchain-google-genai`: Google Gemini API 통합
  - `langchain-experimental`: 실험적 기능 (그래프 변환)
  - `langchain-neo4j`: Neo4j 통합
  - `pyvis`: 네트워크 시각화 라이브러리
  - `python-dotenv`: 환경 변수 관리

### 프로토타입 파일

#### `knowledge_graph.ipynb`
- Jupyter 노트북 형태의 프로토타입 및 실험 환경
- 알고리즘 테스트, 데이터 분석, 시각화 실험

### 출력 및 시각화 파일

#### `knowledge_graph.html`
- **역할**: 개별 문서에서 추출된 지식 그래프의 인터랙티브 시각화
- **특징**: PyVis로 생성된 물리 기반 네트워크 레이아웃
- **자동 생성**: 텍스트 처리 시마다 업데이트

#### `accumulated_knowledge_graph.html`
- **역할**: Neo4j에 저장된 모든 문서의 통합 지식 그래프 시각화
- **특징**: 여러 문서의 지식을 연결한 누적 네트워크
- **메타데이터**: 소스 문서, 생성 시간 등 포함

### 자산 파일

#### `assets/`
- 프로젝트 문서화를 위한 스크린샷 및 이미지 자산

## 데이터 흐름

1. **입력**: 사용자가 `app.py`를 통해 텍스트 또는 파일 업로드
2. **처리**: `generate_knowledge_graph.py`에서 Google Gemini API/LangChain을 통한 LLM 호출
3. **추출**: LLMGraphTransformer가 텍스트에서 엔티티와 관계 추출
4. **저장**: 옵션에 따라 Neo4j 데이터베이스에 그래프 데이터 저장
5. **시각화**: PyVis를 통한 인터랙티브 네트워크 그래프 생성
6. **출력**: HTML 파일로 시각화 결과 저장 및 웹 표시

## 기술 스택 요약

- **Frontend**: Streamlit (Python 웹 앱)
- **Backend**: LangChain + Google Gemini API (LLM 통합)
- **Database**: Neo4j (그래프 데이터베이스)
- **Visualization**: PyVis (네트워크 시각화)
- **Development**: Jupyter Notebook (프로토타이핑)
- **Deployment**: 환경 변수 기반 설정 관리
- **Data Processing**: 생의학 논문 특화 처리 파이프라인

## 주요 변경사항

### 아키텍처 개선
- **모듈화**: 단일 파일에서 기능별 모듈로 분리
- **특화 모듈**: 생의학 분야 특화 추출기 추가
- **설정 관리**: 별도 설정 모듈로 구성 관리 개선

### API 변경
- **OpenRouter → Google Gemini**: 더 안정적인 Google Gemini API로 변경
- **Gemini 2.5 Flash**: 최신 모델 활용으로 성능 향상

### 데이터 처리 강화
- **샘플 데이터**: COVID-19 논문 4편 추가
- **배치 처리**: 대량 문서 처리를 위한 스크립트 추가
- **데이터셋**: bioRxiv 필터링된 데이터셋 포함

### 문서화 확장
- **QA 앱 가이드**: 질의응답 시스템 구축 가이드 추가
- **실습 가이드**: vibe.example.md를 통한 개발 예제 제공
- **구조 설명**: 상세한 프로젝트 구조 문서화