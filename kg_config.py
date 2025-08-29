"""
Configuration file for biomedical knowledge graph extraction
Customize entities, relationships, and extraction parameters here
"""

BIOMEDICAL_ENTITIES = ["ViralStrain","CellType","TissueType","OrganSystem","Disease","ClinicalOutcome",
    "Drug","Vaccine","TreatmentProtocol","GeneExpression","GeneVariant","BiologicalProcess", "Demographics", "ClinicalMeasurement" ,"Symptom",
    "ImmuneResponse", "Antibody", "Receptor", "Enzyme"]

# Biomedical relationships matching available entities
BIOMEDICAL_RELATIONSHIPS = [
    # Viral Pathogenesis & Host Interaction
    ("ViralStrain", "CAUSES", "Disease"),
    ("ViralStrain", "INFECTS", "CellType"),
    ("ViralStrain", "IS_FOUND_IN", "TissueType"),
    ("ViralStrain", "ACTIVATES", "BiologicalProcess"),
    ("ViralStrain", "INHIBITS", "BiologicalProcess"),
    ("ViralStrain", "INDUCES", "ImmuneResponse"),

    # Disease Pathology and Clinical Manifestation
    ("Disease", "INDUCES_PATHOLOGY_IN", "TissueType"),
    ("Disease", "INDUCES_PATHOLOGY_IN", "OrganSystem"),
    ("Disease", "IS_CHARACTERIZED_BY", "BiologicalProcess"),
    ("Disease", "INHIBITS", "BiologicalProcess"),
    ("Disease", "INDUCES", "Symptom"),
    ("Disease", "INDUCES", "ImmuneResponse"),
    ("Disease", "IMPAIRS", "ImmuneResponse"),
    
    # Immune Response & Inflammation
    ("ImmuneResponse", "TARGETS", "ViralStrain"),
    ("ImmuneResponse", "OCCURS_IN", "TissueType"),
    ("ImmuneResponse", "OCCURS_IN", "OrganSystem"),
    ("ImmuneResponse", "INVOLVES", "CellType"),
    ("ImmuneResponse", "ACTIVATES", "BiologicalProcess"),
    ("ImmuneResponse", "INHIBITS", "BiologicalProcess"),
    ("ImmuneResponse", "UPREGULATES", "GeneExpression"),
    ("ImmuneResponse", "DOWNREGULATES", "GeneExpression"),
    ("ImmuneResponse", "INDUCES", "Symptom"),
    ("ImmuneResponse", "IS_BIOMARKER_FOR", "Disease"),
    
    # Molecular and Cellular Biology
    ("GeneExpression", "IS_EXPRESSED_IN", "CellType"),
    ("GeneExpression", "IS_EXPRESSED_IN", "TissueType"),
    ("GeneExpression", "IS_BIOMARKER_FOR", "Disease"),
    ("GeneExpression", "ACTIVATES", "BiologicalProcess"),
    ("GeneExpression", "INHIBITS", "BiologicalProcess"),
    ("BiologicalProcess", "ACTIVATES", "BiologicalProcess"),
    ("BiologicalProcess", "INHIBITS", "BiologicalProcess"),
    ("BiologicalProcess", "UPREGULATES", "GeneExpression"),
    ("BiologicalProcess", "DOWNREGULATES", "GeneExpression"),
    ("BiologicalProcess", "TREATS", "Disease"),
    ("BiologicalProcess", "AFFECTS", "CellType"),
    ("BiologicalProcess", "RELIEVES", "Symptom"),
    ("BiologicalProcess", "ACTIVATES", "ImmuneResponse"),
    ("BiologicalProcess", "INHIBITS", "ImmuneResponse"),
    ("CellType", "DIFFERENTIATES_INTO", "CellType"),
    ("CellType", "INFILTRATES_INTO", "TissueType"),
    ("CellType", "INITIATES", "ImmuneResponse"),
    ("CellType", "ACTIVATES", "BiologicalProcess"),
    ("CellType", "UPREGULATES", "GeneExpression"),

    # Genetics and Predisposition
    ("GeneVariant", "IS_RISK_FACTOR_FOR", "Disease"),
    ("GeneVariant", "REDUCES_RISK_OF", "Disease"),
    ("GeneVariant", "HAS_POSITIVE_CORRELATION_WITH", "GeneExpression"),
    ("GeneVariant", "HAS_NEGATIVE_CORRELATION_WITH", "GeneExpression"),
    ("GeneVariant", "CONFERS_RESISTANCE_TO", "Drug"),
    ("GeneVariant", "CONFERS_SUSCEPTIBILITY_TO", "Drug"),
    ("GeneVariant", "IS_BIOMARKER_FOR", "Disease"),
    
    # Therapeutics and Interventions
    ("Drug", "TREATS", "Disease"),
    ("Drug", "TARGETS", "ViralStrain"),
    ("Drug", "ACTIVATES", "BiologicalProcess"),
    ("Drug", "INHIBITS", "BiologicalProcess"),
    ("Drug", "UPREGULATES", "GeneExpression"),
    ("Drug", "DOWNREGULATES", "GeneExpression"),
    ("Drug", "ACTIVATES", "ImmuneResponse"),
    ("Drug", "INHIBITS", "ImmuneResponse"),
    ("Vaccine", "INDUCES", "ImmuneResponse"),
    ("Vaccine", "PREVENTS", "Disease"),
    ("Vaccine", "INDUCES", "BiologicalProcess"),
    ("Vaccine", "INDUCES", "ClinicalOutcome"),
    ("TreatmentProtocol", "TREATS", "Disease"),
    ("TreatmentProtocol", "INDUCES", "ClinicalOutcome"),

    # Demographics & Clinical Measurements:
    ("Demographics", "IS_RISK_FACTOR_FOR", "Disease"),
    ("Demographics", "IS_ASSOCIATED_WITH", "GeneVariant"),
    ("ClinicalMeasurement", "IS_ELEVATED_IN", "Demographics"),
    ("ClinicalMeasurement", "IS_DECREASED_IN", "Demographics"),
    ("ClinicalMeasurement", "IS_RISK_FACTOR_FOR", "Disease"),
    ("ClinicalMeasurement", "IS_BIOMARKER_FOR", "Disease"),
    ("ClinicalMeasurement", "IS_ELEVATED_IN", "Disease"),
    ("ClinicalMeasurement", "IS_DECREASED_IN", "Disease"),

    # Antibody 
    ("Antibody", "BINDS_TO", "ViralStrain"),
    ("Antibody", "BINDS_TO", "Receptor"),
    ("Antibody", "IS_PRODUCED_BY", "CellType"),
    ("Vaccine", "INDUCES_PRODUCTION_OF", "Antibody"),

    # Receptor
    ("Receptor", "IS_EXPRESSED_ON", "CellType"),
    ("Receptor", "BINDS_TO", "ViralStrain"),
    ("Receptor", "UPREGULATES", "GeneExpression"),
    ("Receptor", "DOWNREGULATES", "GeneExpression"),
    ("Drug", "BLOCKS", "Receptor"),
    ("Drug", "BINDS_TO", "Receptor"),
    ("Drug", "ACTIVATES", "Receptor"),

    # Enzyme
    ("Enzyme", "IS_EXPRESSED_IN", "CellType"),
    ("Enzyme", "CATALYZES", "BiologicalProcess"),
    ("Drug", "ACTIVATES", "Enzyme"),
    ("Drug", "INHIBITS", "Enzyme"),

    # Symptoms
    ("Drug", "RELIEVES", "Symptom"),
    ("TreatmentProtocol", "RELIEVES", "Symptom")
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