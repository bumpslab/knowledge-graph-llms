# 생명의학 도메인 특화 구성: kg_config.py

> **참조:**
> - [kg_config.py](../kg_config.py)
> - [llm_graph_transformer.py](../llm_graph_transformer.py)

## 개요

본 프로젝트는 일반적인 지식 그래프가 아닌 **생명의학 연구에 특화된 지식 그래프**를 구축하기 위해 도메인별 맞춤 구성을 제공합니다. `kg_config.py`는 생명의학 논문에서 추출할 엔티티와 관계를 정의하는 핵심 설정 파일입니다.

## 생명의학 도메인 특화의 필요성

### 1. 일반 NLP vs 생명의학 NLP
```python
# 일반적인 엔티티: "Person", "Organization", "Location"
# 생명의학 특화 엔티티: "ViralStrain", "GeneExpression", "ImmuneResponse"
```

### 2. 전문 용어의 정확한 인식
- **바이러스학**: ViralStrain, CellType, TissueType
- **면역학**: ImmuneResponse, Antibody, Receptor  
- **분자생물학**: GeneExpression, BiologicalProcess, Enzyme
- **임상의학**: Disease, Symptom, TreatmentProtocol

### 3. 복잡한 생물학적 관계 모델링
```python
# 단순한 관계: "WORKS_FOR", "LOCATED_IN"
# 생명의학 관계: "UPREGULATES", "CONFERS_RESISTANCE_TO", "IS_BIOMARKER_FOR"
```

## 핵심 구성 요소

### 1. 생명의학 엔티티 (BIOMEDICAL_ENTITIES)
```python
BIOMEDICAL_ENTITIES = [
    "ViralStrain",          # 바이러스 변종 (예: SARS-CoV-2, Delta variant)
    "CellType",             # 세포 타입 (예: T cell, macrophage)
    "Disease",              # 질병 (예: COVID-19, diabetes)
    "GeneExpression",       # 유전자 발현 (예: ACE2, TMPRSS2)
    "ImmuneResponse",       # 면역 반응 (예: cytokine storm)
    "Drug",                 # 약물 (예: remdesivir, dexamethasone)
    "Antibody",             # 항체 (예: neutralizing antibodies)
    "BiologicalProcess"     # 생물학적 과정 (예: viral replication)
]
```

### 2. 생명의학 관계 (BIOMEDICAL_RELATIONSHIPS)
#### 바이러스 병원성 및 숙주 상호작용
```python
("ViralStrain", "CAUSES", "Disease"),
("ViralStrain", "INFECTS", "CellType"),
("ViralStrain", "INDUCES", "ImmuneResponse")
```

#### 면역 반응 및 염증
```python
("ImmuneResponse", "TARGETS", "ViralStrain"),
("ImmuneResponse", "UPREGULATES", "GeneExpression"),
("ImmuneResponse", "DOWNREGULATES", "GeneExpression")
```

#### 치료 및 중재
```python
("Drug", "TREATS", "Disease"),
("Drug", "INHIBITS", "BiologicalProcess"),
("Vaccine", "INDUCES", "ImmuneResponse")
```

#### 분자 및 세포 생물학
```python
("GeneExpression", "IS_BIOMARKER_FOR", "Disease"),
("BiologicalProcess", "ACTIVATES", "ImmuneResponse"),
("Receptor", "BINDS_TO", "ViralStrain")
```

## 추출 설정 (EXTRACTION_CONFIG)

### 1. 청킹 전략
```python
EXTRACTION_CONFIG = {
    "chunk_size": 1500,     # 생명의학 논문의 복잡한 문장 구조 고려
    "overlap": 200,         # 엔티티 간 관계 유지를 위한 중복 구간
}
```

### 2. 메타데이터 관리
```python
"include_source": True,      # 논문 출처 추적
"base_entity_label": True,   # 인덱싱 최적화
```

## 커스텀 LLM 그래프 변환기

### 1. 도메인 특화 프롬프트
```python
# llm_graph_transformer.py에서 구현
SYSTEM_PROMPT = (
    "You are a top-tier algorithm designed for extracting information in structured "
    "formats to build a knowledge graph.\n"
    "You are also an expert in biomedical domain knowledge.\n"
    "DO NOT use generic terms like 'Gene', 'Protein' for Node IDs.\n"
    "Use specific names or identifiers from the text, such as 'BRCA1', 'Diabetes', etc."
)
```

### 2. 엔티티 검증 및 필터링
- 사전 정의된 엔티티 타입에만 제한
- 생명의학 온톨로지와 일치하는 관계만 허용
- 일반적 용어 대신 구체적 식별자 요구

## 실제 활용 사례

### 1. COVID-19 연구 논문 분석
```python
# 추출되는 엔티티 예시:
# - ViralStrain: "SARS-CoV-2", "Delta variant", "Omicron"
# - Disease: "COVID-19", "pneumonia", "ARDS"
# - Drug: "remdesivir", "tocilizumab", "dexamethasone"
# - ImmuneResponse: "cytokine storm", "neutralizing antibodies"
```

### 2. 관계 추출 예시
```python
# 논문에서 추출되는 관계:
# ("SARS-CoV-2", "CAUSES", "COVID-19")
# ("Delta variant", "INFECTS", "lung epithelial cells")
# ("remdesivir", "INHIBITS", "viral replication")
# ("vaccination", "INDUCES", "neutralizing antibodies")
```

## 확장성과 유연성

### 1. 새로운 연구 분야 추가
```python
# 예: 암 연구를 위한 엔티티 확장
NEW_ENTITIES = ["OncogeneExpression", "TumorSuppressor", "Metastasis"]
NEW_RELATIONSHIPS = [
    ("OncogeneExpression", "PROMOTES", "Metastasis"),
    ("TumorSuppressor", "INHIBITS", "CellProliferation")
]
```

### 2. 동적 구성 업데이트
- 연구 트렌드에 따른 엔티티 타입 추가
- 새로운 생물학적 발견에 따른 관계 유형 확장
- 특정 연구 프로젝트를 위한 맞춤형 구성

## 품질 보장 메커니즘

### 1. 온톨로지 기반 검증
- 생명의학 표준 온톨로지(Gene Ontology, UMLS 등)와의 일치성 검증
- 엔티티 명명 규칙의 일관성 유지

### 2. 관계의 생물학적 타당성
- 생물학적으로 불가능한 관계 조합 방지
- 도메인 전문가에 의한 관계 유형 검증

### 3. 추출 품질 모니터링
- 엔티티 추출 정확도 추적
- 관계 추출의 생물학적 타당성 평가

## 미래 발전 방향

### 1. AI 모델과의 통합
- 생명의학 전용 언어모델(BioBERT, ClinicalBERT)과의 결합
- 도메인 특화 임베딩을 통한 의미론적 검색 강화

### 2. 표준화 및 상호운용성
- FAIR 데이터 원칙 준수
- 국제 생명의학 데이터베이스와의 호환성 확보

### 3. 실시간 지식 업데이트
- PubMed 등 논문 데이터베이스와의 실시간 연동
- 신규 발견사항의 자동 통합 및 검증

이 도메인 특화 구성은 일반적인 지식 그래프 도구를 생명의학 연구의 복잡성과 특수성에 맞게 조정하여, 연구자들이 방대한 생명의학 문헌에서 의미 있는 통찰을 효율적으로 추출할 수 있도록 지원합니다.