# Streamlit: 생명의학 지식 그래프 웹 인터페이스

> **참조:**
> - [https://github.com/streamlit/streamlit](https://github.com/streamlit/streamlit)


## 개요

Streamlit은 Python 기반의 오픈소스 웹 애플리케이션 프레임워크로, 데이터 과학자와 머신러닝 엔지니어가 복잡한 웹 개발 지식 없이도 인터랙티브한 웹 앱을 빠르게 구축할 수 있게 해주는 도구입니다.

## 이 프로젝트에서의 역할

본 지식 그래프 프로젝트에서 Streamlit은 다음과 같은 핵심 역할을 담당합니다:

### 1. 사용자 인터페이스 제공
- **텍스트 입력**: 파일 업로드 또는 직접 텍스트 입력을 위한 인터페이스
- **설정 제어**: 사이드바를 통한 Neo4j 연결 설정 및 그래프 옵션 제어
- **실시간 피드백**: 진행 상황 표시 및 오류 메시지 표시

### 2. 백엔드 서비스와의 연결
- **LangChain 통합**: `generate_knowledge_graph.py`의 함수들을 웹 인터페이스를 통해 호출
- **Neo4j 연동**: 그래프 데이터베이스 저장 및 조회 기능의 UI 제공
- **Google Gemini API**: LLM 모델 호출을 위한 설정 관리
- **생명의학 도메인 특화**: 커스텀 엔티티 및 관계 타입으로 도메인 특화 지식 그래프 구축

### 3. 시각화 플랫폼
- **PyVis 그래프**: 추출된 지식 그래프의 인터랙티브 시각화
- **누적 그래프**: 여러 문서에서 추출된 지식의 통합 보기
- **실시간 렌더링**: 처리 완료 즉시 결과 시각화

## Streamlit의 특징

### 1. 신속한 프로토타이핑
```python
# 복잡한 웹 개발 없이 간단한 코드로 UI 생성
import streamlit as st
uploaded_file = st.file_uploader("파일을 업로드하세요", type=['txt', 'pdf'])
```

### 2. 사용자 친화적 인터페이스
- **직관적 조작**: 드래그 앤 드롭, 슬라이더, 버튼 등 친숙한 UI 요소
- **반응형 디자인**: 다양한 화면 크기에 자동 적응
- **실시간 업데이트**: 입력 변경 시 즉시 결과 반영

### 3. 개발 생산성 향상
- **코드 중심**: HTML, CSS, JavaScript 없이 순수 Python으로 개발
- **핫 리로딩**: 코드 수정 시 자동으로 페이지 새로고침
- **내장 위젯**: 데이터 시각화 및 상호작용을 위한 풍부한 컴포넌트

## 주요 기능과 활용

### 1. 입력 처리
```python
# 다양한 입력 방식 지원
text_input = st.text_area("텍스트를 입력하세요")
uploaded_file = st.file_uploader("파일 업로드")
```

### 2. 상태 관리
```python
# 세션 상태를 통한 데이터 유지
if 'graph_data' not in st.session_state:
    st.session_state.graph_data = None
```

### 3. 레이아웃 제어
```python
# 사이드바와 메인 영역 분리
with st.sidebar:
    neo4j_enabled = st.checkbox("Neo4j에 저장")
    
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(graph)
```
## 이 프로젝트에서의 구체적 활용

### 1. 파일 업로드 및 텍스트 처리
```python
# app.py에서의 활용 예시
uploaded_file = st.file_uploader("Upload file", type=["txt"])
if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    if st.sidebar.button("Generate Knowledge Graph"):
        net = generate_knowledge_graph(text, document_name, store_in_neo4j)
```

### 2. 입력 방식 선택 및 Neo4j 저장 옵션
```python
# 사이드바를 통한 입력 방식 및 저장 옵션 설정
st.sidebar.title("Input document")
input_method = st.sidebar.radio(
    "Choose an input method:",
    ["Upload txt", "Input text"]
)

st.sidebar.title("Storage Options")
store_in_neo4j = st.sidebar.checkbox("Store in Neo4j database", value=True)
```

### 3. 결과 시각화 및 누적 그래프
```python
# 그래프 시각화 및 표시
if st.sidebar.button("Generate Knowledge Graph"):
    net = generate_knowledge_graph(text, document_name, store_in_neo4j)
    output_file = "knowledge_graph.html"
    net.save_graph(output_file)
    
    HtmlFile = open(output_file, 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=1000)

# 누적 그래프 기능
if st.sidebar.button("Show Accumulated Graph"):
    net = get_accumulated_graph_visualization()
    if net is not None:
        output_file = "accumulated_knowledge_graph.html"
        net.save_graph(output_file)
        HtmlFile = open(output_file, 'r', encoding='utf-8')
        components.html(HtmlFile.read(), height=1000)
```

## 장점과 한계

### 장점
1. **빠른 개발**: 복잡한 웹 개발 과정 생략
2. **Python 생태계**: NumPy, Pandas, Matplotlib 등과 원활한 통합
3. **배포 용이성**: Streamlit Cloud를 통한 간편한 배포
4. **커뮤니티**: 활발한 오픈소스 커뮤니티와 풍부한 자료

### 한계
1. **커스터마이징**: UI 디자인의 제한된 자유도
2. **성능**: 대용량 데이터 처리 시 성능 이슈
3. **상태 관리**: 복잡한 상태 관리의 어려움
4. **멀티유저**: 동시 사용자 지원의 제한

## 현재 프로젝트의 주요 특징

### 1. 간소화된 UI 구조
- **와이드 레이아웃**: `layout="wide"`로 그래프 시각화에 최적화
- **사이드바 중심**: 모든 컨트롤이 사이드바에 집약되어 직관적 조작
- **실시간 피드백**: 처리 과정을 단계별로 표시 (`st.spinner`, `st.success`)

### 2. 이중 입력 방식 지원
- **파일 업로드**: TXT 파일 업로드를 통한 배치 처리
- **직접 입력**: 텍스트 영역을 통한 즉시 처리
- **동적 인터페이스**: 선택된 입력 방식에 따라 UI 적응

### 3. 누적 지식 관리
- **개별 그래프**: 각 문서별 독립적인 지식 그래프 생성
- **누적 그래프**: Neo4j에서 모든 문서의 지식을 통합하여 시각화
- **메타데이터 추적**: 각 지식의 출처 문서 및 생성 시간 기록

### 4. 생명의학 연구 최적화
- **대용량 논문 처리**: 청킹을 통한 긴 학술 논문 자동 처리
- **전문 용어 추출**: 생명의학 도메인 특화 엔티티 및 관계 추출
- **연구 협업**: 여러 논문의 지식을 통합한 종합적 분석

Streamlit은 이 생명의학 지식 그래프 프로젝트에서 **연구자 친화적인 인터페이스**를 제공합니다. 복잡한 AI 모델과 그래프 데이터베이스를 간단한 클릭 몇 번으로 조작할 수 있게 하여, 생명의학 연구자들이 기술적 복잡성에 신경 쓰지 않고 연구 내용에 집중할 수 있도록 지원합니다.