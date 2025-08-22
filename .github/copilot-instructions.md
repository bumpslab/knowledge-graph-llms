# Copilot 지침서

이 파일은 이 저장소에서 코드 작업할 때 LLM에게 지침을 제공합니다.

## 프로젝트 개요

이 프로젝트는 LangChain을 사용하여 텍스트에서 엔터티와 관계를 추출하고 Neo4j에 저장하는 Streamlit 기반 지식 그래프 애플리케이션입니다. 직접적인 OpenAI 통합 대신 OpenRouter API를 사용하여 무료 모델을 포함한 다양한 모델을 사용할 수 있는 유연성을 제공합니다.

## 주요 아키텍처 구성 요소

- **app.py**: 입력 방법, Neo4j 저장 옵션, 누적 그래프 시각화를 위한 사이드바 컨트롤이 있는 메인 Streamlit 애플리케이션
- **generate_knowledge_graph.py**: 다음을 포함하는 핵심 로직:
  - `extract_graph_data()`: LLMGraphTransformer를 사용하여 텍스트를 그래프 문서로 변환하는 비동기 함수
  - `visualize_graph()`: 물리 기반 레이아웃을 가진 PyVis 네트워크 시각화
  - `store_graph_in_neo4j()`: 메타데이터 강화를 통한 Neo4j 저장
  - `get_accumulated_graph_visualization()`: 문서 전반에 걸친 모든 저장된 지식을 검색하고 시각화
- **OpenRouter 통합**: OpenRouter API를 가리키는 사용자 정의 기본 URL(`https://openrouter.ai/api/v1`)과 함께 ChatOpenAI 사용

## 개발 명령어

### 환경 설정
```bash
# uv를 사용한 의존성 설치 (권장)
uv pip install -r requirements.txt

# 또는 pip 사용
pip install -r requirements.txt

# 환경 변수 설정 (.env.example을 복사하고 수정)
cp .env.example .env
```

### 애플리케이션 실행
```bash
# Streamlit 개발 서버 시작
streamlit run app.py

# 앱은 http://localhost:8501에서 사용 가능
```

### 환경 구성
`.env`에 필요한 환경 변수:
- `OPENROUTER_API_KEY`: OpenRouter 서비스용 API 키
- `NEO4J_URI`: Neo4j 데이터베이스 연결 문자열 (예: bolt://localhost:7687)
- `NEO4J_USERNAME`: Neo4j 사용자명
- `NEO4J_PASSWORD`: Neo4j 비밀번호

## 주요 기술적 세부사항

### LLM 모델 구성
- 현재 OpenRouter를 통해 `microsoft/mai-ds-r1:free` 모델 사용
- 일관된 추출 결과를 위해 Temperature를 0으로 설정
- `generate_knowledge_graph.py`에서 `model_name` 매개변수를 수정하여 모델 변경 가능

### 데이터 흐름
1. 텍스트 입력 (파일 업로드 또는 수동 입력) → 
2. LLMGraphTransformer가 엔터티/관계 추출 → 
3. 메타데이터와 함께 Neo4j에 선택적 저장 (소스 문서, 타임스탬프) → 
4. 인터랙티브 기능을 가진 PyVis 시각화

### Neo4j 통합
- 지연 초기화를 통한 전역 연결 풀링
- 메타데이터 강화: 노드에 `source_document`와 `created_at` 추가
- 누적 그래프 기능: 여러 문서의 지식 결합
- 연결 실패에 대한 오류 처리

### 시각화 기능
- 사용자 정의 가능한 물리 매개변수를 가진 다크 테마
- 노드 필터링 및 엣지 검증
- 인터랙티브 컨트롤 (드래그, 줌, 호버 툴팁)
- 대형 그래프 탐색을 위한 필터 메뉴
- 독립 실행형 HTML 파일로 내보내기

## 파일 구조 참고사항

- `assets/`: 문서용 스크린샷 및 이미지
- `*.html`: 생성된 그래프 시각화 (런타임에 생성)
- `knowledge_graph.md`: 그래프 구성 패턴에 대한 LangChain 문서
- `neo4jgraph.md`: Neo4j 관련 추가 문서
- 포괄적인 설정 지침이 포함된 한국어 README.md

## 애플리케이션 테스트

애플리케이션이 작동하는지 확인하려면:
1. Neo4j가 실행 중이고 접근 가능한지 확인
2. 유효한 환경 변수 설정
3. `streamlit run app.py` 실행
4. 샘플 텍스트 입력으로 기본 그래프 생성 테스트
5. "누적 그래프 보기" 기능을 확인하여 Neo4j 저장 검증