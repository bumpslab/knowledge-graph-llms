# 바이브 코딩으로 지식 그래프 기반 QA 애플리케이션 만들기

> **다음 자료들도 읽어보세요**: 
>- [Github Copilot 사용자 지정 지침](https://docs.github.com/ko/copilot/how-tos/configure-custom-instructions/add-repository-instructions)  
>- [Github Copilot chat 기능](https://docs.github.com/ko/copilot/how-tos/use-chat/use-chat-in-ide#using-keywords-in-your-prompt) 
>- [Github Copilot Tips, tricks, best practices](https://github.blog/developer-skills/github/how-to-use-github-copilot-in-your-ide-tips-tricks-and-best-practices/)

## 목표
1. 지식 그래프를 생성을 개선해봅시다.
2. 생성한 지식 그래프를 활용한 질의응답(Q&A) 애플리케이션을 만들어 봅시다.  

우선 본격적으로 코드베이스를 수정하기 전에 코드베이스에 대해서 이해해봅시다.

> 참고: 본 실습에서는 **`Gemini-2.5-Pro`** 를 사용하는 것을 권장 드립니다.  
> 유스케이스에 따라 가장 적합한 모델이 다를 수 있습니다.   
> [Github 공식 문서: 모델 비교](https://docs.github.com/ko/copilot/reference/ai-models/model-comparison)  
> [Github Copilot을 쓸 때 무슨 모델을 써야하나요?](https://github.blog/ai-and-ml/github-copilot/which-ai-model-should-i-use-with-github-copilot/)

코드베이스에 대한 질문을 하기 위해서는 "Ask" 모드를 사용하는 것이 좋습니다.  
다음과 같이 질문해봅시다.
> #Codebase에 대해 설명해줘.

좀 더 자세히 질문하고 싶다면,
> #Codebase에 대해 완전히 이해하고 싶어. 이 프로젝트가 어떤 구조로 짜여져 있는지, 주요 파일, 함수, 클래스 등에 대해 자세히 설명해줘

코드에 대해 더 자세히 알고 싶다면 코드를 드래그 해서 선택 한 뒤, **`ctrl + I`**, (mac에서는 **`cmd + I`**)를 누른 후 **`/explain`** 명령어를 사용하여 코드에 대한 설명을 받아봅시다.

# 1. 시스템 프롬프트를 업데이트 하여 지식 그래프 생성 고도화 하기

### kg_config.py 수정
kg config.py 파일에 있는 **`BIOMEDICAL_ENTITIES`** 와 **`BIOMEDICAL_RELATIONSHIPS`** 이 저희가 관심 있는 모든 객체와 관계를 포함하는지 살펴봅시다. 잘 떠오르지 않는다면 Copilot에게 나의 설명을 설명하여 적절한 entity와 관계를 추천 받아봅시다.  
```
너는 바이오 도메인, 특히 코로나 19의 전문가야. 나는 LLM을 이용해서 COVID-19 논문 텍스트를 가지고 지식 그래프를 구축하려고 해. 현재 내가 LLM에게 추출하라고 한 Entity와 Relation의 목록은 #kg_config.py에 있어. 하지만 이는 실제 논문들에 등장할 수 있는 entity와 relation에 비하면 턱없이 부족해. COVID-19 지식 그래프를 구축하기 위해 추가적으로 추출해야할 entity와 relation이 뭐가 있는지 나열해줘.
```
Ask 모드 혹은 Agent 모드 둘 다 좋습니다.

**버전 관리**:
```bash
git add .
git commit -m "enhance biomedical entities and relationships"
git push
```

### SYSTEM_PROMPT 수정 
generate_knowledge_graph.py에 보면 **`SYSTEM_PROMPT`** 변수에 노드와 relation을 추출하기 위한 지시사항이 적혀 있는 것을 볼 수 있습니다. 지시사항을 보고 수정할 점이 없는지 Ask 모드에 질문해봅시다. 
```
너는 바이오 도메인, 특히 코로나 19의 전문가야. 나는 LLM을 이용해서 COVID-19 논문 텍스트를 가지고 지식 그래프를 구축하려고 해. 현재 내가 LLM에게 추출하라고 한 Entity와 Relation의 목록은 #kg_config.py에 있어. generate_knowledge_graph.py의 SYSTEM_PROMPT를 적절히 구성하기 위해서 고쳐야 할 점을 나열해줘.
```

혹은

```
너는 바이오 도메인, 특히 코로나 19의 전문가야. 나는 LLM을 이용해서 COVID-19 논문 텍스트를 가지고 지식 그래프를 구축하려고 해. 현재 내가 LLM에게 추출하라고 한 Entity와 Relation의 목록은 #kg_config.py에 있어. generate_knowledge_graph.py의 SYSTEM_PROMPT에 어떤 내용이 포함되어야 잘 추출할 수 있을까? .md 형태로 정리해줘.
```

**버전 관리**:
```bash
git add .
git commit -m "improve system prompt for graph data extraction"
git push
```

# 2. QA 어플리케이션 만들기
## 단계별 접근 방법

### 전체 개요
복잡한 RAG QA 애플리케이션을 한 번에 구축하는 것은 어렵습니다. **복잡한 작업은 단계별로 쪼개서 진행하는게 좋습니다**. 각 단계에서 작동하는 버전을 만들고, 테스트하고, 버전 관리를 한 후 다음 단계로 넘어가는 것이 중요합니다.

**4단계 로드맵:**
1. **UI 구축** → 채팅 인터페이스 완성
2. **기본 연결** → 간단한 QA 기능 구현 
3. **고급 기능** → 정교한 질의응답 시스템 구축
4. **검증 & 개선** → 전체 시스템 테스트 및 최적화

각 단계마다 **작동하는 프로토타입**을 만들어 점진적으로 발전시켜 나갑니다.

### 1단계: 챗봇 UI 구축
**목표**: Gemini와 같은 현대적인 채팅 인터페이스 만들기

코파일럿에게 다음과 같이 요청하세요:
```
"Streamlit을 사용해서 Gemini처럼 깔끔한 채팅 UI를 만들어줘. 
사용자 메시지와 AI 응답을 구분해서 보여주고, 
메시지 입력창과 전송 버튼이 있어야 해."
```
> 생각하는 구체적 UI 디자인이나 배치가 있다면 그 설명도 요청에 포함해보세요.
> 요구사항이 많다면 멀티턴 대화를 통해 하나씩 단계별로 해나가는 것도 도움이 됩니다.

**검증하기**:
- `streamlit run app.py` 실행
- 채팅 UI가 정상적으로 표시되는지 확인
- 메시지 입력과 표시가 잘 되는지 테스트

**버전 관리**:
```bash
git add .
git commit -m "add chatbot UI"
git push
```

### 2단계: 기본 GraphCypherQAChain 구현
**목표**: 간단한 그래프 기반 질의응답 시스템 구축


코파일럿에게 다음과 같이 요청하세요:
```
"#building_qa_app.md의 GraphCypherQAChain 부분을 참고해서 
우리 Neo4j 지식 그래프와 연결되는 기본적인 QA 기능을 구현해줘.
Streamlit 채팅 UI와 통합해서 사용자 질문에 답할 수 있게 해줘."
```
> copilot 유료 버전의 경우 #fetch 명령어를 통해 url을 직접 참고하게 할 수 있습니다.

**핵심 구현 요소**:
- Neo4j 연결 설정
- GraphCypherQAChain 초기화
- 사용자 질문 → Cypher 쿼리 → 답변 생성 파이프라인
- 기본적인 에러 핸들링

**검증하기**:
- 지식 그래프에 있는 엔티티에 대해 질문
- 관계에 대한 질문 테스트
- 응답이 정확한지 확인

**버전 관리**:
```bash
git add .
git commit -m "implement basic GraphCypherQAChain integration"
git push
```

### 3단계: 고급 구현 (LangGraph 활용)
**목표**: 더욱 정교한 질의응답 시스템 구축

코파일럿에게 다음과 같이 요청하세요:
  ```
  "#building_qa_app.md의 LangGraph를 사용한 고급 구현 부분을 참고해서 
  더 정확하고 안정적인 QA 시스템을 만들어줘.
  특히 다음 기능들을 포함해줘:
  - 질문 검증 (guardrails)
  - Few-shot prompting
  - Cypher 쿼리 검증 및 수정
  - 에러 처리"
  ```

**고급 기능들**:
- **가드레일**: 지식 그래프 관련 질문만 처리
- **Few-shot 예제**: 더 정확한 Cypher 쿼리 생성
- **쿼리 검증**: 생성된 Cypher 쿼리의 구문 및 의미 검증
- **자동 수정**: 오류가 있는 쿼리 자동 교정
- **상세한 로깅**: 각 단계별 처리 과정 추적

**검증하기**:
- 복잡한 질문들로 테스트
- 잘못된 질문에 대한 적절한 거부 확인
- 쿼리 수정 기능 테스트

**버전 관리**:
```bash
git add .
git commit -m "implement advanced QA system with LangGraph"
git push
```

> 다른 기능들도 자유롭게 구현해보세요.
> 테스트와 기능 개선을 반복하며 어플리케이션을 고도화 해봅시다.

## 학습 포인트 요약

### 기술적 학습
1. **RAG 시스템 구조**: 검색 → 증강 → 생성의 전체 파이프라인 이해
2. **지식 그래프 활용**: 구조화된 데이터를 통한 정확한 정보 검색
3. **LangChain 생태계**: GraphCypherQAChain과 LangGraph의 활용법
4. **프롬프트 엔지니어링**: Few-shot learning과 가드레일 구현

### 개발 방법론
1. **점진적 개발**: 간단한 버전부터 시작해서 단계적으로 복잡도 증가
2. **지속적 검증**: 각 단계에서 기능 확인 및 테스트
3. **버전 관리**: 의미 있는 단위로 커밋하여 롤백 가능한 상태 유지
4. **문서 활용**: 기존 문서와 예제를 효과적으로 활용한 개발