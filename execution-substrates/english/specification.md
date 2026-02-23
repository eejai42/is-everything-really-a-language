# Specification Document for Rulebook: PUBLISHED - ERB_semiotics-is-everything-a-language

## Overview
This rulebook defines a set of criteria and calculated fields to classify various entities as language candidates based on specific properties. It is derived from an Airtable base and includes various entities with attributes that help determine whether something qualifies as a language. The calculated fields derive their values from raw input fields, allowing for automated assessments based on defined logical conditions.

## LanguageCandidates

### Input Fields
1. **LanguageCandidateId**
   - **Type:** string
   - **Description:** Unique identifier for the language candidate.

2. **Name**
   - **Type:** string
   - **Description:** Name of the language candidate being classified.

3. **HasSyntax**
   - **Type:** boolean
   - **Description:** Indicates whether the language candidate has syntax and/or grammar.

4. **CanBeHeld**
   - **Type:** boolean
   - **Description:** Indicates if the candidate is physical/material and could theoretically be held.

5. **DistanceFromConcept**
   - **Type:** integer
   - **Description:** Numeric representation of how far the candidate is from the core concept of a language.

6. **IsLanguage**
   - **Type:** boolean
   - **Description:** Indicates if the candidate is classified as a language.

### Calculated Fields

1. **HasGrammar**
   - **Description:** Indicates if the candidate has grammar, generally inferred from the presence of syntax.
   - **Calculation:** This field is true if `HasSyntax` is true.
   - **Formula:** `={{HasSyntax}} = TRUE()`
   - **Example:** If `HasSyntax` is true, then `HasGrammar` will also be true.

2. **Question**
   - **Description:** A question formatted for a Family Feud style poll.
   - **Calculation:** The question is constructed by concatenating "Is " with the `Name` of the candidate and appending " a language?".
   - **Formula:** `="Is " & {{Name}} & " a language?"`
   - **Example:** For a candidate named "English", the question would be "Is English a language?".

3. **PredictedAnswer**
   - **Description:** The predicted answer based on a combination of properties that suggest whether the candidate is a language.
   - **Calculation:** This field is true if all of the following conditions are met:
     - `HasSyntax` is true
     - `RequiresParsing` is true
     - `IsDescriptionOf` is true
     - `HasLinearDecodingPressure` is true
     - `ResolvesToAnAST` is true
     - `IsStableOntologyReference` is true
     - `CanBeHeld` is false
     - `HasIdentity` is false
   - **Formula:** `=AND({{HasSyntax}}, {{RequiresParsing}}, {{IsDescriptionOf}}, {{HasLinearDecodingPressure}}, {{ResolvesToAnAST}}, {{IsStableOntologyReference}}, NOT({{CanBeHeld}}), NOT({{HasIdentity}}))`
   - **Example:** For "English", if all conditions are met, `PredictedAnswer` would be true.

4. **PredictionPredicates**
   - **Description:** A string summarizing the predicates that led to the predicted answer.
   - **Calculation:** This field concatenates multiple conditions into a descriptive string.
   - **Formula:** 
     ```
     =IF({{HasSyntax}}, "Has Syntax", "No Syntax") & " & " & IF({{RequiresParsing}}, "Requires Parsing", "No Parsing Needed") & " & " & IF({{IsDescriptionOf}}, "Describes the thing", "Is the Thing") & " & " & IF({{HasLinearDecodingPressure}}, "Has Linear Decoding Pressure", "No Decoding Pressure") & " & " & IF({{ResolvesToAnAST}}, "Resolves to AST", "No AST") & ", " & IF({{IsStableOntologyReference}}, "Is Stable Ontology", "Not 'Ontology'") & " AND " & IF({{CanBeHeld}}, "Can Be Held", "Can't Be Held") & ", " & IF({{HasIdentity}}, "Has Identity", "Has no Identity")
     ```
   - **Example:** For "English", the output might be "Has Syntax & Requires Parsing & Describes the thing & Has Linear Decoding Pressure & Resolves to AST, Is Stable Ontology AND Can't Be Held, Has no Identity".

5. **PredictionFail**
   - **Description:** Provides an explanation if the predicted answer does not match the candidate's status.
   - **Calculation:** If `PredictedAnswer` does not equal `IsLanguage`, it constructs a message indicating the mismatch and flags any open/closed world conflicts.
   - **Formula:** 
     ```
     =IF(NOT({{PredictedAnswer}} = {{IsLanguage}}), {{Name}} & " " & IF({{PredictedAnswer}}, "Is", "Isn't") & " a Family Feud Language, but " & IF({{IsLanguage}}, "Is", "Is Not") & " marked as a 'Language Candidate.'", "") & IF({{IsOpenClosedWorldConflicted}}, " - Open World vs. Closed World Conflict.", "")
     ```
   - **Example:** For "A Coffee Mug", if `PredictedAnswer` is false and `IsLanguage` is true, the output would be "A Coffee Mug Is not a Family Feud Language, but Is marked as a 'Language Candidate.'".

6. **IsDescriptionOf**
   - **Description:** Indicates if the candidate describes the concept based on its distance from the core concept.
   - **Calculation:** This field is true if `DistanceFromConcept` is greater than 1.
   - **Formula:** `={{DistanceFromConcept}} > 1`
   - **Example:** If `DistanceFromConcept` is 2, `IsDescriptionOf` would be true.

7. **IsOpenClosedWorldConflicted**
   - **Description:** Indicates if there is a conflict between being classified as both open and closed world.
   - **Calculation:** This field is true if both `IsOpenWorld` and `IsClosedWorld` are true.
   - **Formula:** `=AND({{IsOpenWorld}}, {{IsClosedWorld}})`
   - **Example:** If both `IsOpenWorld` and `IsClosedWorld` are true, then `IsOpenClosedWorldConflicted` will be true.

8. **RelationshipToConcept**
   - **Description:** Indicates the relationship of the candidate to the core concept.
   - **Calculation:** If `DistanceFromConcept` equals 1, it outputs "IsMirrorOf"; otherwise, it outputs "IsDescriptionOf".
   - **Formula:** `=IF({{DistanceFromConcept}} = 1, "IsMirrorOf", "IsDescriptionOf")`
   - **Example:** If `DistanceFromConcept` is 1 for "A Coffee Mug", the output would be "IsMirrorOf".

## Conclusion
This specification document provides a comprehensive guide to understanding how to compute the calculated fields for the language candidates defined in the rulebook. By following the outlined steps and formulas, one can accurately derive the necessary values from the raw input fields.