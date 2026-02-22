# ERB Glossary - Predicate Definitions

Human-readable definitions for all predicates in the Effortless Rulebook.

---

## Raw Predicates (Input Fields)

### LanguageCandidateId

**Type:** string

This string uniquely identifies a candidate for classification as a language. It is used to track and reference specific language candidates throughout the classification process.

---

### Name

**Type:** string

This string represents the name of the language candidate being evaluated. It is essential for identification and discussion about the candidate.

---

### IsLanguage

**Type:** boolean

This boolean indicates whether the candidate is classified as a language. It is a crucial final determination in the classification process.

---

### HasSyntax

**Type:** boolean

This boolean indicates whether the candidate has a defined syntax, which refers to its structure and rules for forming valid expressions. A positive answer contributes to classifying the candidate as a language.

---

### CanBeHeld

**Type:** boolean

This boolean indicates if the candidate can be physically held or manipulated. If it cannot be held, it may suggest that the candidate is more abstract, aiding in its classification as a language.

---

### Category

**Type:** string

This string describes the category or type of the language candidate, such as programming language, natural language, or markup language. It helps in contextualizing the candidate within broader language classifications.

---

### HasIdentity

**Type:** boolean

This boolean indicates whether the candidate has a distinct identity or definition that sets it apart from other candidates. A lack of identity may support classifying it as a language.

---

### RequiresParsing

**Type:** boolean

This boolean indicates whether the candidate requires parsing, which is the process of analyzing its structure. Candidates that require parsing are more likely to be classified as languages.

---

### ResolvesToAnAST

**Type:** boolean

This boolean indicates whether the candidate can be transformed into an Abstract Syntax Tree (AST), a structured representation of its syntax. This capability is a strong indicator that the candidate is a language.

---

### HasLinearDecodingPressure

**Type:** boolean

This boolean indicates whether the candidate experiences linear decoding pressure, meaning it processes information in a linear fashion. This characteristic supports the classification of the candidate as a language.

---

### IsStableOntologyReference

**Type:** boolean

This boolean indicates whether the candidate serves as a stable reference within an ontology, a formal representation of knowledge. A stable ontology reference is often a hallmark of a language.

---

### IsLiveOntologyEditor

**Type:** boolean

This boolean indicates whether the candidate functions as a live editor for an ontology. If it is a live editor, it may imply that the candidate functions more dynamically, which could influence its classification.

---

### IsOpenWorld

**Type:** boolean

This boolean indicates whether the candidate operates in an open world context, where new information can continuously be added. This context can affect how the candidate is classified as a language.

---

### IsClosedWorld

**Type:** boolean

This boolean indicates whether the candidate operates in a closed world context, where all possible information is known. The classification as a language may differ depending on whether it is open or closed.

---

### DistanceFromConcept

**Type:** integer

This numeric value measures how far the candidate is conceptually from being a defined language. A lower distance may indicate a closer relationship to being classified as a language.

---

### DimensionalityWhileEditing

**Type:** string

This string describes the dimensionality of the candidate while it is being edited. Understanding its dimensionality can provide insights into its complexity and help determine if it fits the criteria for a language.

---

### ModelObjectFacilityLayer

**Type:** string

This string indicates the layer of abstraction at which the candidate operates within a modeling framework. It helps in understanding the candidate's functionality and its potential classification as a language.

---

### SortOrder

**Type:** integer

This integer indicates the order in which candidates are prioritized for evaluation or classification. It is used to manage the classification process efficiently.

---

## Calculated Predicates (Computed Fields)

### HasGrammar

**Type:** boolean
**Formula:** `={{HasSyntax}} = TRUE()`

This boolean indicates whether the candidate has defined grammatical rules. Having grammar is a strong indicator that the candidate can be classified as a language.

---

### Question

**Type:** string
**Formula:** `="Is " & {{Name}} & " a language?"`

This string formulates a question about whether the candidate is a language. It serves as a prompt for evaluation during the classification process.

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

This boolean represents an automated assessment of whether the candidate is likely a language based on its characteristics. It guides further investigation into the classification.

---

### PredictionPredicates

**Type:** string
**Formula:** `=IF({{HasSyntax}}, "Has Syntax", "No Syntax") & ", " & IF({{RequiresParsing}}, "Requires Parsing", "No Parsing Needed") & ", " & IF({{IsDescriptionOf}}, "Describes the thing", "Is the Thing") & ", " & IF({{HasLinearDecodingPressure}}, "Has Linear Decoding Pressure", "No Decoding Pressure") & ", " & IF({{ResolvesToAnAST}}, "Resolves to AST", "No AST") & ", " & IF({{IsStableOntologyReference}}, "Is Stable Ontology", "Not 'Ontology'") & ", " & IF({{CanBeHeld}}, "Can Be Held", "Can't Be Held") & " And " & IF({{HasIdentity}}, "Has Identity", "Has no Identity")`

This string summarizes the key characteristics of the candidate, highlighting aspects like syntax and parsing requirements. It provides a quick overview of the candidate's attributes for classification.

---

### PredictionFail

**Type:** string
**Formula:** `=IF(NOT({{PredictedAnswer}} = {{IsLanguage}}),
  {{Name}} & " " & IF({{PredictedAnswer}}, "Is", "Isn't") & " a Family Feud Language, but " & 
  IF({{IsLanguage}}, "Is", "Is Not") & " marked as a 'Language Candidate.'", "") & IF({{IsOpenClosedWorldConflicted}}, " - Open World vs. Closed World Conflict.", "")`

This string details any inconsistencies between the predicted classification and the actual classification of the candidate. It serves as a feedback mechanism to refine the classification process.

---

### IsDescriptionOf

**Type:** boolean
**Formula:** `={{DistanceFromConcept}} > 1`

This boolean indicates whether the candidate is merely describing a concept rather than being a language itself. A positive answer might suggest that the candidate is not a language.

---

### IsOpenClosedWorldConflicted

**Type:** boolean
**Formula:** `=AND({{IsOpenWorld}}, {{IsClosedWorld}})`

This boolean indicates whether the candidate is simultaneously considered to be in both open and closed world contexts. Such a conflict may complicate its classification as a language.

---

### RelationshipToConcept

**Type:** string
**Formula:** `=IF({{DistanceFromConcept}} = 1, "IsMirrorOf", "IsDescriptionOf")`

This string describes the relationship of the candidate to the core concept of a language, indicating whether it mirrors or describes the language concept. This relationship helps clarify its classification.

---
