# ERB Specification - Language Classification Rulebook

---

## Overview

The objective of this formal rulebook system is to clarify the concept of "language" and decisively address the assertion that "everything is a language." By establishing a rigorous framework, the system aims to define language as a structured construct characterized by specific, testable properties. This not only helps refine our understanding of what constitutes a language but also serves to delineate the boundaries of its application in various contexts, thus preventing the overextension of the term.

At the heart of this system lies a clear operational definition of language. An item qualifies as a language if it possesses essential attributes: it must have syntax, require parsing, serialize meaning, and function as a stable ontology descriptor. This definition not only provides a foundation for identifying languages but also establishes criteria to distinguish genuine languages from other forms of communication or representation that may lack the necessary structural components.

To effectively classify candidates as languages or not, the system utilizes a set of raw input predicates that capture critical properties related to language. These predicates, such as HasSyntax, RequiresParsing, and HasLinearDecodingPressure, form the basis of calculated outputs that assess whether an item meets the operational definition. The resulting classifications are derived from a systematic evaluation of these properties, leading to a conclusion about each candidate's status as a language. In this analysis, all 23 evaluated candidates were determined to be non-languages, underscoring the robustness of the classification criteria.

The key insight of this formalized approach is the significant distinction it makes between language systems, sign vehicles, and semiotic processes. This differentiation is crucial for understanding various forms of communication and meaning production. By clearly identifying what qualifies as a language, the system allows for a more nuanced exploration of how we interact with and interpret our world, ultimately enhancing our ability to model and analyze complex communicative phenomena.

---

## Model Structure

The model operates on a set of raw predicates (input properties) that are evaluated for each candidate,
which then feed into calculated fields that derive the final classification.

### Raw Predicates (Inputs)

These are the fundamental properties evaluated for each candidate:

- **IsLanguage** (boolean)
- **HasSyntax** (boolean)
- **CanBeHeld** (boolean)
- **HasIdentity** (boolean)
- **RequiresParsing** (boolean)
- **ResolvesToAnAST** (boolean)
- **HasLinearDecodingPressure** (boolean)
- **IsStableOntologyReference** (boolean)
- **IsLiveOntologyEditor** (boolean)
- **IsOpenWorld** (boolean)
- **IsClosedWorld** (boolean)
- **DistanceFromConcept** (integer)
- **DimensionalityWhileEditing** (string)
- **ModelObjectFacilityLayer** (string)

### Calculated Fields (Derived)

These fields are computed from the raw predicates:

- **HasGrammar**
- **Question**
- **PredictedAnswer**
- **PredictionPredicates**
- **PredictionFail**
- **IsDescriptionOf**
- **IsOpenClosedWorldConflicted**
- **RelationshipToConcept**

---

## Core Language Definition

An item qualifies as a **Language** if and only if ALL of these are true:

1. HasSyntax = true
2. RequiresParsing = true
3. HasLinearDecodingPressure = true
4. StableOntologyReference = true
5. CanBeHeld = false
6. HasIdentity = false
7. DistanceFromConcept = 2

---

## Calculated Field Instructions

### HasGrammar

**Formula:** `={{HasSyntax}} = TRUE()`

**How to compute:**

1. Look at the value of HasSyntax. 2. If HasSyntax is true, then HasGrammar is true. If HasSyntax is false, then HasGrammar is false.

---

### Question

**Formula:** `="Is " & {{Name}} & " a language?"`

**How to compute:**

1. Take the value of Name. 2. Combine it with the text 'Is ' and ' a language?' to form a complete question.

---

### PredictedAnswer

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

**How to compute:**

1. Check if HasSyntax is true. 2. Check if RequiresParsing is true. 3. Check if IsDescriptionOf is true. 4. Check if HasLinearDecodingPressure is true. 5. Check if ResolvesToAnAST is true. 6. Check if IsStableOntologyReference is true. 7. Check if CanBeHeld is false. 8. Check if HasIdentity is false. 9. If all conditions are met, PredictedAnswer is true; otherwise, false.

---

### PredictionPredicates

**Formula:** `=IF({{HasSyntax}}, "Has Syntax", "No Syntax") & ", " & IF({{RequiresParsing}}, "Requires Parsing", "No Parsing Needed") & ", " & IF({{IsDescriptionOf}}, "Describes the thing", "Is the Thing") & ", " & IF({{HasLinearDecodingPressure}}, "Has Linear Decoding Pressure", "No Decoding Pressure") & ", " & IF({{ResolvesToAnAST}}, "Resolves to AST", "No AST") & ", " & IF({{IsStableOntologyReference}}, "Is Stable Ontology", "Not 'Ontology'") & ", " & IF({{CanBeHeld}}, "Can Be Held", "Can't Be Held") & " And " & IF({{HasIdentity}}, "Has Identity", "Has no Identity")`

**How to compute:**

1. Check if HasSyntax is true or false. 2. Check if RequiresParsing is true or false. 3. Check if IsDescriptionOf is true or false. 4. Check if HasLinearDecodingPressure is true or false. 5. Check if ResolvesToAnAST is true or false. 6. Check if IsStableOntologyReference is true or false. 7. Check if CanBeHeld is true or false. 8. Check if HasIdentity is true or false. 9. Combine all these results into a single string.

---

### PredictionFail

**Formula:** `=IF(NOT({{PredictedAnswer}} = {{IsLanguage}}),
  {{Name}} & " " & IF({{PredictedAnswer}}, "Is", "Isn't") & " a Family Feud Language, but " & 
  IF({{IsLanguage}}, "Is", "Is Not") & " marked as a 'Language Candidate.'", "") & IF({{IsOpenClosedWorldConflicted}}, " - Open World vs. Closed World Conflict.", "")`

**How to compute:**

1. Determine if PredictedAnswer is not equal to IsLanguage. 2. If they are not equal, form a statement about Name and whether it is a Family Feud Language. 3. Include if IsOpenClosedWorldConflicted is true.

---

### IsDescriptionOf

**Formula:** `={{DistanceFromConcept}} > 1`

**How to compute:**

1. Look at the value of DistanceFromConcept. 2. If it is greater than 1, then IsDescriptionOf is true; otherwise, it is false.

---

### IsOpenClosedWorldConflicted

**Formula:** `=AND({{IsOpenWorld}}, {{IsClosedWorld}})`

**How to compute:**

1. Check if IsOpenWorld is true. 2. Check if IsClosedWorld is true. 3. If both are true, then IsOpenClosedWorldConflicted is true; otherwise, it is false.

---

### RelationshipToConcept

**Formula:** `=IF({{DistanceFromConcept}} = 1, "IsMirrorOf", "IsDescriptionOf")`

**How to compute:**

1. Look at the value of DistanceFromConcept. 2. If it equals 1, then RelationshipToConcept is 'IsMirrorOf'. 3. If it does not equal 1, then it is 'IsDescriptionOf'.

---
