# Streamlit: 웹 애플리케이션 프레임워크

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
- **OpenRouter API**: LLM 모델 호출을 위한 설정 관리

### 3. 시각화 플랫폼
- **PyVis 그래프**: 추출된 지식 그래프의 인터랙티브 시각화
- **누적 그래프**: 여러 문서에서 추출된 지식의 통합 보기
- **실시간 렌더링**: 처리 완료 즉시 결과 시각화

## Streamlit의 필요성

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

## 대안 기술과의 비교

### vs. Flask/Django
- **장점**: 설정이 간단하고 데이터 앱에 특화
- **단점**: 복잡한 웹 애플리케이션에는 제한적

### vs. Jupyter Notebook
- **장점**: 공유 가능한 웹 앱 형태로 배포
- **단점**: 대화형 개발 환경의 유연성은 부족

### vs. React/Vue.js
- **장점**: Python 개발자에게 친숙, 백엔드 통합 용이
- **단점**: 프론트엔드 커스터마이징 제한

## 이 프로젝트에서의 구체적 활용

### 1. 파일 업로드 및 텍스트 처리
```python
# app.py에서의 활용 예시
uploaded_file = st.file_uploader("파일을 선택하세요", type=['txt', 'pdf', 'docx'])
if uploaded_file:
    content = uploaded_file.read().decode('utf-8')
    graph_data = await extract_graph_data(content)
```

### 2. 설정 관리
```python
# 사이드바를 통한 Neo4j 설정
with st.sidebar:
    st.header("Neo4j 설정")
    neo4j_uri = st.text_input("Neo4j URI")
    neo4j_username = st.text_input("사용자명")
    neo4j_password = st.text_input("비밀번호", type="password")
```

### 3. 결과 시각화
```python
# 그래프 시각화 및 표시
if graph_data:
    html_content = visualize_graph(graph_data)
    st.components.v1.html(html_content, height=600)
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

## 결론

Streamlit은 데이터 중심 웹 애플리케이션을 빠르게 구축하는 데 매우 효과적인 도구입니다. 특히 이 지식 그래프 프로젝트처럼 텍스트 처리, 데이터 시각화, 외부 서비스 연동이 필요한 경우에 이상적인 선택입니다. 

복잡한 웹 개발 지식 없이도 사용자 친화적인 인터페이스를 제공하면서, Python 백엔드 로직과의 원활한 통합을 가능하게 하여 개발 생산성을 크게 향상시킵니다.