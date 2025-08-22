# 지식 그래프 생성기

<mark><b>LangChain</b></mark>과 <mark><b>OpenRouter</b></mark> API를 사용하여 텍스트 입력에서 그래프 데이터(엔티티 및 관계)를 추출하고, 그래프 정보를 <mark><b>Neo4j</b></mark> GraphDB에 저장하며 인터랙티브 그래프를 시각화하는 <mark><b>Streamlit</b></mark> 애플리케이션입니다.
![CleanShot 2025-05-28 at 13 11 46](https://github.com/user-attachments/assets/4fef9158-8dd8-432d-bb8a-b53953a82c6c)

👉 이 저장소는 Thu Vu의 [Youtube 튜토리얼](https://www.youtube.com/watch?v=O-T_6KOXML4)과 [github 저장소](https://github.com/thu-vu92/knowledge-graph-llms)를 기반으로 만들어졌습니다:

## 기능
텍스트에서 그래프 데이터 추출, Graph DB에 데이터 저장, Streamlit UI 이용한 시각화

- 두 가지 입력 방법: 텍스트 업로드(.txt 파일) 또는 직접 텍스트 입력
- 인터랙티브 지식 그래프 시각화
- 물리 기반 레이아웃을 통한 사용자 정의 가능한 그래프 표시
- OpenRouter API에서 제공하는 LLM을 활용한 엔티티 관계 추출
- Neo4j DB에 엔티티, 관계 저장

### 필수 요구사항

- <mark><b>Github</b></mark> 계정 및 <mark><b>Github Codespaces</b><mark> 세팅
- <mark><b>Neo4j</b></mark> 설정
- <mark><b>OpenRouter</b></mark> API 키

## 설정

### 1. Github 계정 및 Github Codespaces 설정

1. [https://github.com/](https://github.com/) 접속, 우상단 <mark><b>Sign up</b></mark> 클릭
2. <mark><b>Continue with Google</b></mark> 선택 혹은 정보 입력 후 <mark><b>Create account</b></mark> 선택
3. 이 저장소를 **자신의 github 저장소로 fork:**
![Alt text](./assets/Fork.png)

4. [https://github.com/features/codespaces?locale=ko-KR](https://github.com/features/codespaces?locale=ko-KR) 접속, <mark><b>무료로 시작하기</b></mark> 클릭
5. fork한 저장소를 이용하여 codespace 생성
![Alt text](./assets/create_new_codespace.png)

6. 다음과 같은 화면이 나올 시 정상적으로 완료된 상태
![Alt text](./assets/example_screen.png)

> **참고:**   
> 자신의 저장소를 이용해서 codespace를 생성하게 되면
> git clone <my repo url>를 한 것과 동일한 상태로 vscode와 터미널을 사용할 수 있습니다.  
> codespace를 사용하지 않는다면 터미널에서 git clone <my repo url>을 실행해서 원격 저장소를 로컬로 불러와야 합니다.

---
### 2. Neo4j 설정

1. [https://neo4j.com/product/auradb/](https://neo4j.com/product/auradb/)로 이동하여 <mark><b>Start Free</b></mark>를 클릭
2. <mark><b>Continue with Google</b></mark>을 클릭하고 로그인
3. 각 단계를 거쳐 필요한 정보를 입력
4. <mark><b>Create instance</b></mark>를 클릭
5. <mark><b>Download to Continue</b></mark>를 클릭
![Alt text](./assets/neo4j_setup.png)
6. .txt 파일이 <mark><b>Downloads</b></mark> 디렉토리에 있는지, 다음과 같은 정보를 포함하는지 확인
![Alt text](./assets/neo4j_credentials.png)
7. 페이지 로딩 완료 시 <mark><b>Dashboards</b></mark> 클릭 후 Dashboard를 Instance와 연결하기
![Alt text](./assets/connect_dashboard.png)
---
### 3. OpenRouter API 키 가져오기

1. [https://openrouter.ai/](https://openrouter.ai/)에서 github으로 로그인
2. <mark><b>Authorize OpenRouterTeam</b></mark>을 클릭
3. 우측 상단 아이콘을 클릭하고 <mark><b>Keys</b></mark>를 클릭
![Alt text](./assets/openrouter_1.png)
4. <mark><b>Create API Key</b></mark>를 클릭
![Alt text](./assets/CreateAPIKey.png)
5. 이름을 입력하고 <mark><b>credit limit</b></mark>을 0으로 설정한 후 <mark><b>Create</b></mark>를 클릭
![Alt text](./assets/createapikey_2.png) 
6. API 키를 복사하여 **쉽게 접근할 수 있는 곳에 저장하고 다른 사람과 공유하지 마십시오.**
![Alt text](./assets/saveapikey.png)
---
## 설치
**의존성(패키지를 실행시키기 위한 패키지) 설치**를 위해 <mark><b>uv</b></mark> 사용을 권장합니다. <mark><b>uv</b></mark>를 설치하고 가상 환경을 활성화하십시오.  
<mark><b>uv</b></mark> 설치:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

가상 환경 생성 및 활성화:
```
uv venv 
source .venv/bin/activate
```

### 의존성

이 패키지가 작동하기 위해서는 다음 Python 패키지가 설치 되어있어야 합니다.

- <mark><b>langchain (>= 0.1.0)</b></mark>: 핵심 LLM 프레임워크
- <mark><b>langchain-experimental (>= 0.0.45)</b></mark>: 실험적 LangChain 기능
- <mark><b>langchain-openai (>= 0.1.0)</b></mark>: LangChain용 OpenAI 통합
- <mark><b>langchain-neo4j</b></mark>: LangChain용 Neo4j 통합
- <mark><b>python-dotenv (>= 1.0.0)</b></mark>: 환경 변수 지원
- <mark><b>pyvis (>= 0.3.2)</b></mark>: 그래프 시각화
- <mark><b>streamlit (>= 1.32.0)</b></mark>: 웹 UI 프레임워크

제공된 <mark><b>requirements.txt</b></mark> 파일을 사용하여 모든 **필수 의존성을 설치하십시오:**

```bash
uv pip install -r requirements.txt
```
---
### OpenRouter API Key와 Neo4j 자격 증명

**루트 디렉토리**에 <mark><b>OpenRouter API</b></mark> 키, <mark><b>Neo4j</b></mark> uri 및 자격 증명이 포함된 <mark><b>.env</b></mark> **파일을 생성하세요:**
```
OPENROUTER_API_KEY=your_openai_api_key_here
NEO4J_URI=your_neo4j_url_here
NEO4J_USERNAME=your_neo4j_username_here
NEO4J_PASSWORD=your_neo4j_password_here
```
![Alt text](./assets/make_env.png)
---
## 애플리케이션 실행

<mark><b>Streamlit</b></mark> 앱을 실행하려면:

```bash
streamlit run app.py
```

이렇게 하면 애플리케이션이 시작되고 기본 웹 브라우저에서 열립니다(일반적으로 http://localhost:8501).

## 사용법

1. 사이드바에서 입력 방법을 선택하세요 (txt 업로드 또는 텍스트 입력)
2. 파일을 업로드하는 경우 컴퓨터에서 .txt 파일을 선택하세요
3. 직접 입력을 사용하는 경우 텍스트 영역에 텍스트를 입력하거나 붙여넣기 하세요
4. "Generate Knowledge Graph" 버튼을 클릭하세요
5. 그래프가 생성될 때까지 기다리세요 (텍스트 길이에 따라 몇 분 정도 소요될 수 있습니다)
6. 인터랙티브 지식 그래프를 탐색하세요:
   - 노드를 드래그하여 그래프를 재배치
   - 노드와 엣지에 마우스를 올려 추가 정보 확인
   - 마우스 휠을 사용하여 확대/축소
   - 특정 노드와 엣지에 대해 그래프 필터링

## 작동 원리

이 애플리케이션은 <mark><b>OpenRouter API</b></mark>를 통해 다양한 LLM 모델에 접근하고, <mark><b>LangChain</b></mark>의 LLMGraphTransformer를 사용하여 텍스트에서 지식 그래프를 생성합니다:

### 1. 텍스트 처리 및 엔터티 추출
- <mark><b>OpenRouter API</b></mark>를 통해 Microsoft의 모델 등 다양한 LLM에 접근
- <mark><b>LLMGraphTransformer</b></mark>가 입력 텍스트를 분석하여 엔터티(인물, 조직, 장소, 개념 등)를 식별
- 엔터티 간의 의미적 관계를 추출하여 구조화된 그래프 데이터로 변환

### 2. Neo4j 그래프 데이터베이스 저장
- 추출된 엔터티와 관계를 <mark><b>Neo4j GraphDB</b></mark>에 영구 저장
- 각 노드에 소스 문서명과 생성 시간 등 메타데이터 추가
- 여러 문서의 지식을 누적하여 종합적인 지식 그래프 구축

### 3. 인터랙티브 시각화
- <mark><b>PyVis</b></mark>를 사용하여 그래프를 인터랙티브 HTML로 변환
- 물리 기반 레이아웃으로 노드와 엣지를 동적 배치
- 필터링, 확대/축소, 드래그 등 다양한 상호작용 기능 제공

### 4. 누적 지식 관리
- 여러 문서에서 추출된 지식을 하나의 통합된 그래프로 결합
- 문서 간 공통 엔터티 연결을 통한 지식 네트워크 확장
- 시간에 따른 지식 축적과 관계 발견 지원

## 라이선스

이 프로젝트는 MIT 라이선스 하에 라이선스됩니다 - 소프트웨어의 자유로운 사용, 수정 및 배포를 허용하는 허용적 오픈 소스 라이선스입니다.

자세한 내용은 [MIT 라이선스](https://opensource.org/licenses/MIT) 문서를 참조하세요.
