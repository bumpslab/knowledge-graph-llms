"""
Configuration file for biomedical knowledge graph extraction
Customize entities, relationships, and extraction parameters here
"""

# Core biomedical entities - expand as needed
BIOMEDICAL_ENTITIES = [
    # Molecular entities
    "Gene", "Enzyme", "Antibody", "Antigen",
    "Chemokine", "Mutation", "Serotype", "Epitope",
    
    # Pathological entities  
    "Disease", "Symptom", "Pathology", "Complication", "Syndrome",
    "Clinical_outcome", "Disease_severity", "Adverse_event", "Side_effect",
    "Risk_factor",
    
    # Anatomical entities
    "Cell_type", "Tissue_type", 
    "Cellular_component", "Receptor", "Membrane",
    
    # Microbial entities
    "Virus", "Viral_gene", 
    "Viral_mutation", "Pathogen",
    
    # Therapeutic entities
    "Drug", "Drug_class", "Vaccine", 
    "Treatment_protocol", "Clinical_trial", "Therapy",
    
    # Process entities
    "Biological_process",

    # Population/Environmental
    "Population_group", "Environmental_factor"
]

# Biomedical relationships matching available entities
BIOMEDICAL_RELATIONSHIPS = [
    # Molecular interactions
    ("Drug", "BINDS_TO", "Receptor"),
    ("Virus", "BINDS_TO", "Receptor"),
    ("Antibody", "BINDS_TO", "Antigen"),
    ("Chemokine", "BINDS_TO", "Receptor"),
    
    # Regulatory relationships
    ("Gene", "ENCODES", "Enzyme"),
    ("Drug", "INHIBITS", "Enzyme"),
    ("Viral_gene", "ENCODES", "Enzyme"),
    ("Gene", "ASSOCIATED_WITH", "Mutation"),
    ("Mutation", "AFFECTS", "Gene"),
    
    # Pathological relationships
    ("Virus", "INFECTS", "Cell_type"),
    ("Pathogen", "CAUSES", "Disease"),
    ("Mutation", "CAUSES", "Disease"),
    ("Viral_mutation", "CAUSES", "Disease"),
    ("Gene", "ASSOCIATED_WITH", "Disease"),
    ("Risk_factor", "PREDISPOSES_TO", "Disease"),
    ("Disease", "MANIFESTS_AS", "Symptom"),
    ("Disease", "PROGRESSES_TO", "Complication"),
    ("Syndrome", "INCLUDES", "Symptom"),
    ("Pathology", "INDICATES", "Disease"),
    
    # Therapeutic relationships
    ("Drug", "TREATS", "Disease"),
    ("Drug", "REDUCES", "Symptom"),
    ("Drug", "PREVENTS", "Disease"),
    ("Vaccine", "PREVENTS", "Disease"),
    ("Drug", "ANTAGONIZES", "Virus"),
    ("Drug", "INHIBITS", "Pathogen"),
    ("Treatment_protocol", "IMPROVES", "Clinical_outcome"),
    ("Treatment_protocol", "INCLUDES", "Drug"),
    ("Therapy", "TREATS", "Disease"),
    ("Drug", "CAUSES", "Side_effect"),
    ("Drug", "CAUSES", "Adverse_event"),
    ("Drug_class", "INCLUDES", "Drug"),
    
    # Physiological relationships
    ("Enzyme", "PARTICIPATES_IN", "Biological_process"),
    ("Gene", "PARTICIPATES_IN", "Biological_process"),
    ("Viral_gene", "PARTICIPATES_IN", "Biological_process"),
    ("Disease", "AFFECTS", "Tissue_type"),
    ("Virus", "AFFECTS", "Cell_type"),
    ("Pathogen", "AFFECTS", "Cellular_component"),
    
    # Diagnostic relationships
    ("Symptom", "INDICATES", "Disease"),
    ("Serotype", "IDENTIFIES", "Virus"),
    ("Epitope", "IDENTIFIES", "Antigen"),
    ("Clinical_trial", "TESTS", "Drug"),
    ("Clinical_trial", "TESTS", "Vaccine"),
    
    # Epidemiological relationships
    ("Population_group", "SUSCEPTIBLE_TO", "Disease"),
    ("Environmental_factor", "RISK_FACTOR_FOR", "Disease"),
    ("Disease_severity", "CORRELATES_WITH", "Clinical_outcome"),
    
    # Temporal relationships
    ("Symptom", "PRECEDES", "Disease"),
    ("Treatment_protocol", "FOLLOWED_BY", "Clinical_outcome"),
    ("Disease", "CONCURRENT_WITH", "Complication"),
    
    # Location relationships
    ("Virus", "DETECTED_IN", "Tissue_type"),
    ("Disease", "OCCURS_IN", "Population_group"),
    ("Pathogen", "FOUND_IN", "Cell_type"),
    ("Epitope", "LOCATED_ON", "Antigen"),
    ("Receptor", "LOCATED_ON", "Membrane"),
    ("Cellular_component", "PART_OF", "Cell_type")
]

# Node properties to extract (currently disabled)
NODE_PROPERTIES = None

# Model configuration
MODEL_CONFIG = {
    "model_name": "microsoft/mai-ds-r1:free",  # Free model via OpenRouter
    "temperature": 0,  # Deterministic extraction
    "base_url": "https://openrouter.ai/api/v1"
}

# Extraction settings
EXTRACTION_CONFIG = {
    "include_source": True,  # Track source documents
    "base_entity_label": True,  # Add __Entity__ label for indexing
    "chunk_size": 1500,  # Max characters per document chunk
    "overlap": 200  # Overlap between chunks
}