# ERB Specification - Language Classification Rulebook

---

## Overview

The primary goal of this formal rulebook system is to challenge the prevailing notion that "everything is a language," while simultaneously providing a clear and structured definition of what constitutes a language. By treating language as a typed construct defined by specific, testable properties, the system aims to establish a logical framework that delineates true languages from entities that may merely be interpreted as communicative or meaningful. This formalization not only clarifies the concept of language but also provides a basis for rigorous analysis and classification.

At the heart of this system lies the operational definition of language, which asserts that an item qualifies as a language if it possesses syntax, requires parsing, serializes meaning, and functions as an ontology or descriptor system. This definition is essential in filtering out various forms of communication that do not meet the established criteria. The formalization relies on a set of predicates—such as HasSyntax, RequiresParsing, and HasLinearDecodingPressure—that collectively determine whether something can be classified as a language. By applying these predicates, we can systematically evaluate candidates and establish a clear boundary for what constitutes a language.

The model structure operates by taking raw input properties and transforming them into calculated outputs that facilitate classification. Each candidate is assessed against the defined predicates, leading to calculated fields that predict whether the candidate meets the criteria for being a language. The resulting outputs indicate whether a candidate is classified as a language or not, allowing for a comprehensive evaluation of various entities. Through this structured approach, the system has successfully classified 23 candidates as not being languages, reinforcing the validity of the operational definition.

The key insight of this formalization is the importance of distinguishing between language systems, sign vehicles, and semiotic processes. Not everything that conveys meaning qualifies as a language; some entities, like objects or phenomena, may serve as sign vehicles or contribute to semiotic processes without possessing the structural elements that define a true language. Understanding these distinctions enables a more nuanced view of communication and meaning, and it highlights the role of running applications as a complex area that embodies both language systems and dynamic interactions. This clarity is crucial for fields ranging from linguistics to computer science, where precise definitions can significantly impact theoretical and practical applications.

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

1. Check the value of HasSyntax.
2. If HasSyntax is true, then HasGrammar is true. Otherwise, it is false.

---

### Question

**Formula:** `="Is " & {{Name}} & " a language?"`

**How to compute:**

1. Take the value of Name.
2. Combine it with the phrase 'Is ' and the phrase ' a language?'.
3. The result is the value of Question.

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

1. Check the values of HasSyntax, RequiresParsing, IsDescriptionOf, HasLinearDecodingPressure, ResolvesToAnAST, IsStableOntologyReference, CanBeHeld, and HasIdentity.
2. If all the first six are true and the last two are false, then PredictedAnswer is true. Otherwise, it is false.

---

### PredictionPredicates

**Formula:** `=IF({{HasSyntax}}, "Has Syntax", "No Syntax") & ", " & IF({{RequiresParsing}}, "Requires Parsing", "No Parsing Needed") & ", " & IF({{IsDescriptionOf}}, "Describes the thing", "Is the Thing") & ", " & IF({{HasLinearDecodingPressure}}, "Has Linear Decoding Pressure", "No Decoding Pressure") & ", " & IF({{ResolvesToAnAST}}, "Resolves to AST", "No AST") & ", " & IF({{IsStableOntologyReference}}, "Is Stable Ontology", "Not 'Ontology'") & ", " & IF({{CanBeHeld}}, "Can Be Held", "Can't Be Held") & " And " & IF({{HasIdentity}}, "Has Identity", "Has no Identity")`

**How to compute:**

1. Check the values of HasSyntax, RequiresParsing, IsDescriptionOf, HasLinearDecodingPressure, ResolvesToAnAST, IsStableOntologyReference, CanBeHeld, and HasIdentity.
2. For each field, append the corresponding phrase based on its value.
3. Combine all phrases with commas and 'And' for the last two to form PredictionPredicates.

---

### PredictionFail

**Formula:** `=IF(NOT({{PredictedAnswer}} = {{IsLanguage}}),
  {{Name}} & " " & IF({{PredictedAnswer}}, "Is", "Isn't") & " a Family Feud Language, but " & 
  IF({{IsLanguage}}, "Is", "Is Not") & " marked as a 'Language Candidate.'", "") & IF({{IsOpenClosedWorldConflicted}}, " - Open World vs. Closed World Conflict.", "")`

**How to compute:**

1. Check if PredictedAnswer is not equal to IsLanguage.
2. If they are not equal, create a message indicating the status of Name as a language candidate.
3. Append a note if IsOpenClosedWorldConflicted is true.

---

### IsDescriptionOf

**Formula:** `={{DistanceFromConcept}} > 1`

**How to compute:**

1. Look at the value of DistanceFromConcept.
2. If it is greater than 1, then IsDescriptionOf is true. Otherwise, it is false.

---

### IsOpenClosedWorldConflicted

**Formula:** `=AND({{IsOpenWorld}}, {{IsClosedWorld}})`

**How to compute:**

1. Check the values of IsOpenWorld and IsClosedWorld.
2. If both are true, then IsOpenClosedWorldConflicted is true. Otherwise, it is false.

---

### RelationshipToConcept

**Formula:** `=IF({{DistanceFromConcept}} = 1, "IsMirrorOf", "IsDescriptionOf")`

**How to compute:**

1. Check the value of DistanceFromConcept.
2. If it equals 1, then RelationshipToConcept is 'IsMirrorOf'. If it is not 1, then it is 'IsDescriptionOf'.

---
