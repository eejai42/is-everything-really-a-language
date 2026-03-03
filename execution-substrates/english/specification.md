# Specification Document for Rulebook: PUBLISHED - ERB_semiotics-is-everything-a-language

## Overview
This rulebook provides a structured framework for evaluating various candidates to determine if they can be classified as a language. It includes a set of calculated fields that derive insights based on raw input data about each language candidate. The rulebook is designed to facilitate the classification process by offering clear criteria and formulas for evaluation.

## Entities and Calculated Fields

### Entity: LanguageCandidates

#### Input Fields (Type: raw)
1. **LanguageCandidateId**
   - **Type:** string
   - **Description:** Unique identifier for the language candidate.

2. **Name**
   - **Type:** string
   - **Description:** Name of the language candidate being classified.

3. **IsLanguage**
   - **Type:** boolean
   - **Description:** Indicates if the candidate is classified as a language.

4. **HasSyntax**
   - **Type:** boolean
   - **Description:** Indicates if the language candidate has syntax and/or grammar.

5. **CanBeHeld**
   - **Type:** boolean
   - **Description:** Indicates if the candidate is physical/material.

6. **IsParsed**
   - **Type:** boolean
   - **Description:** Indicates if the information requires parsing before meaning can be extracted.

7. **ResolvesToAnAST**
   - **Type:** boolean
   - **Description:** Indicates if the information resolves to an Abstract Syntax Tree (AST).

8. **HasLinearDecodingPressure**
   - **Type:** boolean
   - **Description:** Indicates if there is linear decoding pressure in the candidate.

9. **IsStableOntologyReference**
   - **Type:** boolean
   - **Description:** Indicates if the candidate is a stable ontology reference.

10. **HasIdentity**
    - **Type:** boolean
    - **Description:** Indicates if the candidate can be assigned a unique identifier.

11. **DistanceFromConcept**
    - **Type:** integer
    - **Description:** Distance from the core concept being evaluated.

12. **IsOpenWorld**
    - **Type:** boolean
    - **Description:** Indicates if the candidate is considered an open world.

13. **IsClosedWorld**
    - **Type:** boolean
    - **Description:** Indicates if the candidate is considered a closed world.

#### Calculated Fields (Type: calculated)

1. **HasGrammar**
   - **Description:** Determines if the candidate has grammar based on the presence of syntax.
   - **How to Compute:** If `HasSyntax` is true, then `HasGrammar` is true; otherwise, it is false.
   - **Formula:** `={{HasSyntax}} = TRUE()`
   - **Example:** If `HasSyntax` is true, then `HasGrammar` is true.

2. **Question**
   - **Description:** Constructs a question that could be asked in a Family Feud style.
   - **How to Compute:** Combine the phrase "Is " with the `Name` of the candidate and append " a language?".
   - **Formula:** `="Is " & {{Name}} & " a language?"`
   - **Example:** For `Name` = "English", the output would be "Is English a language?".

3. **PredictedAnswer**
   - **Description:** Predicts if the candidate is likely to be considered a language based on various criteria.
   - **How to Compute:** The answer is true if all of the following conditions are met:
     - `HasSyntax` is true
     - `IsParsed` is true
     - `IsDescriptionOf` is true
     - `HasLinearDecodingPressure` is true
     - `ResolvesToAnAST` is true
     - `IsStableOntologyReference` is true
     - `CanBeHeld` is false
     - `HasIdentity` is false
   - **Formula:** `=AND({{HasSyntax}}, {{IsParsed}}, {{IsDescriptionOf}}, {{HasLinearDecodingPressure}}, {{ResolvesToAnAST}}, {{IsStableOntologyReference}}, NOT({{CanBeHeld}}), NOT({{HasIdentity}}))`
   - **Example:** If all conditions are met for "English", `PredictedAnswer` would be true.

4. **PredictedBiologicalLanguage_Core**
   - **Description:** Determines if the candidate meets the core biological language criteria.
   - **How to Compute:** The answer is true if all of the following conditions are met:
     - `Bio_IsEvolvedCommunicationSystem` is true
     - `Bio_HasSemanticity` is true
     - `Bio_HasArbitrariness` is true
     - `Bio_HasDiscreteness` is true
     - `Bio_HasDualityOfPatterning` is true
     - `Bio_HasProductivity` is true
     - `Bio_HasDisplacement` is true
     - `Bio_HasCulturalTransmission` is true
   - **Formula:** `=AND({{Bio_IsEvolvedCommunicationSystem}}, {{Bio_HasSemanticity}}, {{Bio_HasArbitrariness}}, {{Bio_HasDiscreteness}}, {{Bio_HasDualityOfPatterning}}, {{Bio_HasProductivity}}, {{Bio_HasDisplacement}}, {{Bio_HasCulturalTransmission}})`
   - **Example:** If all biological criteria are met for "English", `PredictedBiologicalLanguage_Core` would be true.

5. **PredictedBiologicalLanguage_Strict**
   - **Description:** Determines if the candidate meets the strict biological language criteria.
   - **How to Compute:** The answer is true if `PredictedBiologicalLanguage_Core` is true and both `Bio_HasInterchangeability` and `Bio_HasFeedback` are true.
   - **Formula:** `=AND({{PredictedBiologicalLanguage_Core}}, {{Bio_HasInterchangeability}}, {{Bio_HasFeedback}})`
   - **Example:** If "English" meets the strict criteria, `PredictedBiologicalLanguage_Strict` would be true.

6. **Bio_HockettScore**
   - **Description:** Computes a score based on various biological language attributes.
   - **How to Compute:** Sum the boolean values of the following attributes:
     - `Bio_HasSemanticity`
     - `Bio_HasArbitrariness`
     - `Bio_HasDiscreteness`
     - `Bio_HasDualityOfPatterning`
     - `Bio_HasProductivity`
     - `Bio_HasDisplacement`
     - `Bio_HasCulturalTransmission`
     - `Bio_HasInterchangeability`
     - `Bio_HasFeedback`
     - `Bio_HasBroadcastTransmission`
     - `Bio_HasRapidFading`
   - **Formula:** `=SUM(IF({{Bio_HasSemanticity}},1,0), IF({{Bio_HasArbitrariness}},1,0), IF({{Bio_HasDiscreteness}},1,0), IF({{Bio_HasDualityOfPatterning}},1,0), IF({{Bio_HasProductivity}},1,0), IF({{Bio_HasDisplacement}},1,0), IF({{Bio_HasCulturalTransmission}},1,0), IF({{Bio_HasInterchangeability}},1,0), IF({{Bio_HasFeedback}},1,0), IF({{Bio_HasBroadcastTransmission}},1,0), IF({{Bio_HasRapidFading}},1,0))`
   - **Example:** If all biological attributes for "English" are true, the `Bio_HockettScore` would be 11.

7. **PredictionPredicates**
   - **Description:** Constructs a string that summarizes the predicates affecting the prediction.
   - **How to Compute:** Combine the results of various boolean fields into a descriptive string.
   - **Formula:** `=IF({{HasSyntax}}, "Has Syntax", "No Syntax") & " & " & IF({{IsParsed}}, "Requires Parsing", "No Parsing Needed") & " & " & IF({{IsDescriptionOf}}, "Describes the thing", "Is the Thing") & " & " & IF({{HasLinearDecodingPressure}}, "Has Linear Decoding Pressure", "No Decoding Pressure") & " & " & IF({{ResolvesToAnAST}}, "Resolves to AST", "No AST") & ", " & IF({{IsStableOntologyReference}}, "Is Stable Ontology", "Not 'Ontology'") & " AND " & IF({{CanBeHeld}}, "Can Be Held", "Can't Be Held") & ", " & IF({{HasIdentity}}, "Has Identity", "Has no Identity")`
   - **Example:** For "English", the output might be "Has Syntax & Requires Parsing & Describes the thing & Has Linear Decoding Pressure & Resolves to AST, Is Stable Ontology AND Can't Be Held, Has no Identity".

8. **PredictionFail**
   - **Description:** Provides an explanation if the predicted answer does not match the actual classification.
   - **How to Compute:** If `PredictedAnswer` does not equal `IsLanguage`, construct a message explaining the mismatch.
   - **Formula:** `=IF(NOT({{PredictedAnswer}} = {{IsLanguage}}), {{Name}} & " " & IF({{PredictedAnswer}}, "Is", "Isn't") & " a Family Feud Language, but " & IF({{IsLanguage}}, "Is", "Is Not") & " marked as a 'Language Candidate.'", "") & IF({{IsOpenClosedWorldConflicted}}, " - Open World vs. Closed World Conflict.", "")`
   - **Example:** If `PredictedAnswer` for "A Coffee Mug" is false and `IsLanguage` is true, the output would be "A Coffee Mug Isn't a Family Feud Language, but Is marked as a 'Language Candidate.'".

9. **IsOpenClosedWorldConflicted**
   - **Description:** Indicates if there is a conflict between being classified as both open and closed world.
   - **How to Compute:** The answer is true if both `IsOpenWorld` and `IsClosedWorld` are true.
   - **Formula:** `=AND({{IsOpenWorld}}, {{IsClosedWorld}})`
   - **Example:** If both are true for "A Game of Fortnite", `IsOpenClosedWorldConflicted` would be true.

10. **IsDescriptionOf**
    - **Description:** Indicates if the candidate is a description of the concept based on its distance.
    - **How to Compute:** The answer is true if `DistanceFromConcept` is greater than 1.
    - **Formula:** `={{DistanceFromConcept}} > 1`
    - **Example:** If `DistanceFromConcept` for "English" is 2, `IsDescriptionOf` would be true.

11. **RelationshipToConcept**
    - **Description:** Determines the relationship of the candidate to the core concept based on distance.
    - **How to Compute:** If `DistanceFromConcept` equals 1, the output is "IsMirrorOf"; otherwise, it is "IsDescriptionOf".
    - **Formula:** `=IF({{DistanceFromConcept}} = 1, "IsMirrorOf", "IsDescriptionOf")`
    - **Example:** For "A Coffee Mug" with `DistanceFromConcept` of 1, the output would be "IsMirrorOf".

This specification provides a comprehensive guide to understanding how to compute the calculated fields for each language candidate based on the raw input data in the rulebook. Each calculation is defined clearly, ensuring that the values can be derived accurately without needing to reference the original formulas directly.