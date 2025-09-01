"""
Configuration file for biomedical knowledge graph extraction
Customize entities, relationships, and extraction parameters here
"""

BIOMEDICAL_ENTITIES = ["ViralStrain","CellType","TissueType","OrganSystem","Disease","ClinicalOutcome",
    "Drug","Vaccine"]

# Biomedical relationships as documented in component_explanation/biomedical_config.md
BIOMEDICAL_RELATIONSHIPS = [
    # Viral Pathogenesis & Host Interaction
    ("ViralStrain", "CAUSES", "Disease"),
    ("ViralStrain", "INFECTS", "CellType"),
    ("ViralStrain", "INDUCES", "ImmuneResponse"),
    
    # Immune Response & Inflammation
    ("ImmuneResponse", "TARGETS", "ViralStrain"),
    ("ImmuneResponse", "UPREGULATES", "GeneExpression"),
    ("ImmuneResponse", "DOWNREGULATES", "GeneExpression"),
    
    # Therapeutics and Interventions
    ("Drug", "TREATS", "Disease"),
    ("Drug", "INHIBITS", "BiologicalProcess"),
    ("Vaccine", "INDUCES", "ImmuneResponse"),
    
    # Molecular and Cellular Biology
    ("GeneExpression", "IS_BIOMARKER_FOR", "Disease"),
    ("BiologicalProcess", "ACTIVATES", "ImmuneResponse"),
    ("Receptor", "BINDS_TO", "ViralStrain")
]

# Node properties to extract (currently disabled)
NODE_PROPERTIES = None

# Extraction settings
EXTRACTION_CONFIG = {
    "include_source": True,  # Track source documents
    "base_entity_label": True,  # Add __Entity__ label for indexing
    "chunk_size": 1500,  # Max characters per document chunk
    "overlap": 200  # Overlap between chunks
}

# Core biomedical entities - expand as needed
"""BIOMEDICAL_ENTITIES = [
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
"""