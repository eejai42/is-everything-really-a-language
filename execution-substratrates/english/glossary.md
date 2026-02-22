# ERB Glossary - Predicate Definitions

Human-readable definitions for all predicates in the Effortless Rulebook.

---

## Raw Predicates (Input Fields)

### LanguageCandidateId

**Type:** string

This predicate represents a unique identifier for a language candidate. It helps in tracking and referencing specific language candidates within the classification system.

---

### Name

**Type:** string

This predicate represents the name of the language candidate. It is used to identify and refer to the specific language in discussions and analyses.

---

### IsLanguage

**Type:** boolean

This boolean predicate indicates whether the candidate is classified as a language. It is a key factor in determining if the candidate meets the criteria to be considered a language.

---

### HasSyntax

**Type:** boolean

This predicate indicates whether the language candidate has a defined syntax. A positive value suggests that the candidate has structured rules for sentence formation, which is important for classification as a language.

---

### CanBeHeld

**Type:** boolean

This boolean predicate signifies whether the language candidate can be physically held or contained. It helps differentiate between tangible and intangible language forms in the classification process.

---

### Category

**Type:** string

This predicate categorizes the language candidate into a specific group or type. It aids in organizing candidates based on shared characteristics or features.

---

### HasIdentity

**Type:** boolean

This boolean predicate shows whether the language candidate has a distinct identity. A positive value indicates that the candidate is recognized as a unique language, which is a significant aspect of language classification.

---

### RequiresParsing

**Type:** boolean

This predicate indicates whether the language candidate necessitates parsing to understand its structure. If true, it suggests that the candidate has a complex structure requiring analysis, which is considered when determining language status.

---

### ResolvesToAnAST

**Type:** boolean

This boolean predicate measures whether the language candidate can be represented as an Abstract Syntax Tree (AST). A positive value indicates that the candidate can be broken down into a hierarchical structure, a feature often associated with programming languages.

---

### HasLinearDecodingPressure

**Type:** boolean

This predicate indicates whether the language candidate has linear decoding pressure, meaning it requires processing in a sequential manner. This characteristic is relevant in understanding the complexity and usability of the candidate as a language.

---

### IsStableOntologyReference

**Type:** boolean

This boolean predicate signifies whether the language candidate serves as a stable reference in ontology. A true value implies that the candidate is reliable for knowledge representation, which is important for its classification as a language.

---

### IsLiveOntologyEditor

**Type:** boolean

This predicate indicates whether the language candidate acts as a live editor for ontologies. If true, it suggests the candidate allows for dynamic updates and modifications, which can affect its classification.

---

### IsOpenWorld

**Type:** boolean

This boolean predicate shows whether the language candidate operates in an open-world context, where knowledge is not fully complete. This context can influence how the candidate is classified in terms of flexibility and adaptability.

---

### IsClosedWorld

**Type:** boolean

This predicate indicates whether the language candidate functions within a closed-world framework, where all knowledge is assumed to be known. This aspect is considered when determining the nature of the candidate in relation to language classification.

---

### DistanceFromConcept

**Type:** integer

This numeric value measures how far a language candidate is from a core language concept. A lower value suggests a closer alignment with fundamental language characteristics, which is crucial for classification.

---

### DimensionalityWhileEditing

**Type:** string

This predicate represents the complexity of the editing process for the language candidate. It is used to assess how intuitive or complicated it is to work with the candidate, impacting its classification as a language.

---

### ModelObjectFacilityLayer

**Type:** string

This predicate indicates the layer of the model object facility associated with the language candidate. It helps in understanding the structure and organization of the candidate within the broader classification framework.

---

### SortOrder

**Type:** integer

This numeric value defines the order in which language candidates are sorted or prioritized. It aids in organizing candidates for analysis and comparison during the classification process.

---

## Calculated Predicates (Computed Fields)

### HasGrammar

**Type:** boolean
**Formula:** `={{HasSyntax}} = TRUE()`

This boolean predicate indicates whether the language candidate possesses grammar rules. A true value suggests that the candidate has a formal structure, which is a key consideration in classifying it as a language.

---

### Question

**Type:** string
**Formula:** `="Is " & {{Name}} & " a language?"`

This string predicate formulates a question regarding whether the language candidate is a language. It serves as a prompt for evaluating the candidate's status within the classification system.

---

### PredictedAnswer

**Type:** boolean
**Formula:** `=AND(
  {{HasSyntax}},
  {{RequiresParsing}},
  {{IsDescriptionOf}},
  {{HasLinearDecodingPressure}},
  {{ResolvesToAnAST}},
  {{IsStableOntologyReference}},
  NOT({{CanBeHeld}}),
  NOT({{HasIdentity}})
)`

This boolean predicate predicts whether the language candidate meets the criteria to be classified as a language based on several factors. It synthesizes information from various predicates to assist in the classification decision.

---

### PredictionPredicates

**Type:** string
**Formula:** `=IF({{HasSyntax}}, "Has Syntax", "No Syntax") & ", " & IF({{RequiresParsing}}, "Requires Parsing", "No Parsing Needed") & ", " & IF({{IsDescriptionOf}}, "Describes the thing", "Is the Thing") & ", " & IF({{HasLinearDecodingPressure}}, "Has Linear Decoding Pressure", "No Decoding Pressure") & ", " & IF({{ResolvesToAnAST}}, "Resolves to AST", "No AST") & ", " & IF({{IsStableOntologyReference}}, "Is Stable Ontology", "Not 'Ontology'") & ", " & IF({{CanBeHeld}}, "Can Be Held", "Can't Be Held") & " And " & IF({{HasIdentity}}, "Has Identity", "Has no Identity")`

This string predicate summarizes the relevant characteristics of the language candidate based on its attributes. It provides an overview of the candidate’s features, aiding in the determination of its language status.

---

### PredictionFail

**Type:** string
**Formula:** `=IF(NOT({{PredictedAnswer}} = {{IsLanguage}}),
  {{Name}} & " " & IF({{PredictedAnswer}}, "Is", "Isn't") & " a Family Feud Language, but " & 
  IF({{IsLanguage}}, "Is", "Is Not") & " marked as a 'Language Candidate.'", "") & IF({{IsOpenClosedWorldConflicted}}, " - Open World vs. Closed World Conflict.", "")`

This string predicate outlines discrepancies between the predicted answer and the actual classification of the language candidate. It highlights conflicts and issues that may arise during the classification process.

---

### IsDescriptionOf

**Type:** boolean
**Formula:** `={{DistanceFromConcept}} > 1`

This boolean predicate indicates whether the language candidate serves as a description of a concept rather than being a language itself. A true value suggests that the candidate is more of a definitional or illustrative tool.

---

### IsOpenClosedWorldConflicted

**Type:** boolean
**Formula:** `=AND({{IsOpenWorld}}, {{IsClosedWorld}})`

This boolean predicate measures whether the language candidate presents conflicting attributes of being both open and closed world. A true value indicates a contradiction that must be resolved in the classification process.

---

### RelationshipToConcept

**Type:** string
**Formula:** `=IF({{DistanceFromConcept}} = 1, "IsMirrorOf", "IsDescriptionOf")`

This string predicate describes the relationship of the language candidate to the core concept of language. It clarifies whether the candidate is a direct representation or merely a description, which is essential for accurate classification.

---
