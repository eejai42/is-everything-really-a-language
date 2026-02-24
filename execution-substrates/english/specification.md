# Specification Document for Rulebook: PUBLISHED - ERB_semiotics-is-everything-a-language

## Overview
This rulebook provides a structured framework for evaluating various language candidates based on specific criteria. It includes a set of calculated fields that derive insights about whether a candidate qualifies as a language, based on attributes such as syntax, parsing, and identity. The rulebook is generated from an Airtable base and includes detailed descriptions of each field, along with the necessary formulas for calculating derived values.

## Entity: LanguageCandidates

### Input Fields (Type: Raw)
1. **LanguageCandidateId**
   - **Type:** String
   - **Description:** Unique identifier for the language candidate.

2. **Name**
   - **Type:** String
   - **Description:** Name of the language candidate being classified.

3. **IsLanguage**
   - **Type:** Boolean
   - **Description:** Indicates if the candidate is considered a language.

4. **HasSyntax**
   - **Type:** Boolean
   - **Description:** Indicates if the language candidate has syntax and/or grammar.

5. **CanBeHeld**
   - **Type:** Boolean
   - **Description:** Indicates if the candidate is physical/material and could theoretically be held.

6. **DistanceFromConcept**
   - **Type:** Integer
   - **Description:** A numerical representation of how closely the candidate relates to a specific concept.

7. **HasIdentity**
   - **Type:** Boolean
   - **Description:** Indicates if the candidate can be assigned a unique identifier.

8. **IsParsed**
   - **Type:** Boolean
   - **Description:** Indicates if the knowledge/information requires parsing before meaning can be extracted.

9. **ResolvesToAnAST**
   - **Type:** Boolean
   - **Description:** Indicates if the knowledge/information can be represented as an Abstract Syntax Tree (AST).

10. **HasLinearDecodingPressure**
    - **Type:** Boolean
    - **Description:** Indicates if the candidate has linear decoding pressure.

11. **IsStableOntologyReference**
    - **Type:** Boolean
    - **Description:** Indicates if the candidate is a stable ontology reference.

12. **IsOpenWorld**
    - **Type:** Boolean
    - **Description:** Indicates if the candidate is considered to be in an open world context.

13. **IsClosedWorld**
    - **Type:** Boolean
    - **Description:** Indicates if the candidate is considered to be in a closed world context.

14. **IsDescriptionOf**
    - **Type:** Boolean
    - **Description:** Indicates if the candidate describes a concept rather than being the concept itself.

### Calculated Fields (Type: Calculated)

1. **HasGrammar**
   - **Description:** Determines if the candidate has grammar based on the presence of syntax.
   - **Calculation:** If `HasSyntax` is true, then `HasGrammar` is true.
   - **Formula:** `={{HasSyntax}} = TRUE()`
   - **Example:** If `HasSyntax` for "English" is true, then `HasGrammar` will also be true.

2. **Question**
   - **Description:** Constructs a question that could be posed to a group of people, family feud style.
   - **Calculation:** The question is formed by concatenating "Is ", the candidate's name, and " a language?".
   - **Formula:** `="Is " & {{Name}} & " a language?"`
   - **Example:** For "English", the question will be "Is English a language?".

3. **PredictedAnswer**
   - **Description:** Predicts the most popular answer based on various criteria.
   - **Calculation:** The answer is true if all of the following conditions are met:
     - Has syntax
     - Is parsed
     - Is a description of a concept
     - Has linear decoding pressure
     - Resolves to an AST
     - Is a stable ontology reference
     - Cannot be held
     - Has no identity
   - **Formula:** `=AND({{HasSyntax}}, {{IsParsed}}, {{IsDescriptionOf}}, {{HasLinearDecodingPressure}}, {{ResolvesToAnAST}}, {{IsStableOntologyReference}}, NOT({{CanBeHeld}}), NOT({{HasIdentity}}))`
   - **Example:** For "English", if all conditions are met, `PredictedAnswer` will be true.

4. **PredictionPredicates**
   - **Description:** Summarizes the predicates that led to the prediction.
   - **Calculation:** Concatenates the results of various predicates into a descriptive string.
   - **Formula:** 
     ```
     =IF({{HasSyntax}}, "Has Syntax", "No Syntax") & " & " & 
     IF({{IsParsed}}, "Requires Parsing", "No Parsing Needed") & " & " & 
     IF({{IsDescriptionOf}}, "Describes the thing", "Is the Thing") & " & " & 
     IF({{HasLinearDecodingPressure}}, "Has Linear Decoding Pressure", "No Decoding Pressure") & " & " & 
     IF({{ResolvesToAnAST}}, "Resolves to AST", "No AST") & ", " & 
     IF({{IsStableOntologyReference}}, "Is Stable Ontology", "Not 'Ontology'") & " AND " & 
     IF({{CanBeHeld}}, "Can Be Held", "Can't Be Held") & ", " & 
     IF({{HasIdentity}}, "Has Identity", "Has no Identity")
     ```
   - **Example:** For "English", the predicates will yield a string summarizing its characteristics.

5. **PredictionFail**
   - **Description:** Provides a message explaining any mismatch between the predicted answer and the actual classification.
   - **Calculation:** If the predicted answer does not match `IsLanguage`, it constructs an explanation message.
   - **Formula:** 
     ```
     =IF(NOT({{PredictedAnswer}} = {{IsLanguage}}),
       {{Name}} & " " & IF({{PredictedAnswer}}, "Is", "Isn't") & " a Family Feud Language, but " & 
       IF({{IsLanguage}}, "Is", "Is Not") & " marked as a 'Language Candidate.'", "") & 
       IF({{IsOpenClosedWorldConflicted}}, " - Open World vs. Closed World Conflict.", "")
     ```
   - **Example:** If "A Coffee Mug" is predicted to be a language but is marked as not being one, the output will indicate the mismatch.

6. **IsDescriptionOf**
   - **Description:** Determines if the candidate describes a concept based on its distance from the concept.
   - **Calculation:** If `DistanceFromConcept` is greater than 1, then it is a description.
   - **Formula:** `={{DistanceFromConcept}} > 1`
   - **Example:** If "English" has a `DistanceFromConcept` of 2, then `IsDescriptionOf` will be true.

7. **IsOpenClosedWorldConflicted**
   - **Description:** Checks for conflicts between open and closed world designations.
   - **Calculation:** True if both `IsOpenWorld` and `IsClosedWorld` are true.
   - **Formula:** `=AND({{IsOpenWorld}}, {{IsClosedWorld}})`
   - **Example:** If both flags are true for "Falsifier A", then this field will indicate a conflict.

8. **RelationshipToConcept**
   - **Description:** Defines the relationship of the candidate to a concept based on its distance.
   - **Calculation:** If `DistanceFromConcept` equals 1, it is a mirror; otherwise, it describes the concept.
   - **Formula:** `=IF({{DistanceFromConcept}} = 1, "IsMirrorOf", "IsDescriptionOf")`
   - **Example:** For "A UML File" with a `DistanceFromConcept` of 2, the output will be "IsDescriptionOf".

## Conclusion
This specification outlines how to compute the calculated fields for the `LanguageCandidates` entity within the rulebook. By following the provided formulas and examples, users can derive the necessary values for each candidate without needing to reference the original formulas directly.