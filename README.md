# Effortless Rulebook

### Generated from: 

> This builds ssotme tools including those that are disabled which regenerates this file.

```
$ cd ./docs
$ ssotme -build -id
```


> CMCC rulebook generated directly from Airtable base.

**Model ID:** `appC8XTj95lubn6hz`

---

## Tables

### IsEverythingALanguage

> Table: IsEverythingALanguage

#### Schema

| Field | Type | Data Type | Nullable | Description |
|-------|------|-----------|----------|-------------|
| `IsEverythingALanguageId` | raw | string | No | - |
| `Name` | raw | string | Yes | - |
| `ArgumentName` | raw | string | Yes | - |
| `ArgumentCategory` | raw | string | Yes | - |
| `StepType` | raw | string | Yes | - |
| `Statement` | raw | string | Yes | - |
| `Formalization` | raw | string | Yes | - |
| `RelatedCandidateName` | raw | string | Yes | - |
| `RelatedCandidateId` | raw | string | Yes | - |
| `EvidenceFromRulebook` | raw | string | Yes | - |
| `Notes` | raw | string | Yes | - |


#### Sample Data (16 records)

| Field | Value |
|-------|-------|
| `IsEverythingALanguageId` | neial-001 |
| `Name` | NEIAL-001 |
| `ArgumentName` | LanguageCanBeFormalized |
| `ArgumentCategory` | Definition |
| `StepType` | Motivation |
| `Statement` | To avoid the slogan 'Everything is a language', treat 'language' as a typed construct defined by testable properties (syntax, parsing, serialized meaning, and descriptor-role). |
| `Notes` | This keeps 'can be interpreted' separate from 'is a language system'. |
| `Formalization` |  |
| `RelatedCandidateName` |  |
| `RelatedCandidateId` |  |
| `EvidenceFromRulebook` |  |

---

### LanguageCandidates

> Table: LanguageCandidates

#### Schema

| Field | Type | Data Type | Nullable | Description |
|-------|------|-----------|----------|-------------|
| `LanguageCandidateId` | raw | string | No | - |
| `Name` | raw | string | Yes | - |
| `Is_A_Family_Feud_Top_Answer` | calculated | boolean | Yes | - |
| `Category` | raw | string | Yes | - |
| `CanBeHeld` | raw | boolean | Yes | - |
| `Meaning_Is_Serialized` | raw | boolean | Yes | - |
| `RequiresParsing` | raw | boolean | Yes | - |
| `IsOngologyDescriptor` | raw | boolean | Yes | - |
| `HasSyntax` | raw | boolean | Yes | - |
| `ChosenLanguageCandidate` | raw | boolean | Yes | - |
| `FamilyFeudMismatch` | calculated | string | Yes | - |
| `SortOrder` | raw | integer | Yes | - |
| `FamilyFuedQuestion` | calculated | string | Yes | - |
| `HasIdentity` | raw | boolean | Yes | - |
| `RelationshipToConcept` | calculated | string | Yes | - |
| `DistanceFromConcept` | raw | integer | Yes | - |
| `CategoryContainsLanguage` | calculated | boolean | Yes | - |
| `HasGrammar` | calculated | string | Yes | - |

**Formula for `Is_A_Family_Feud_Top_Answer`:**
```
=AND(
  {{CategoryContainsLanguage}},
  {{HasSyntax}},
  NOT({{CanBeHeld}}),
  {{Meaning_Is_Serialized}},
  {{RequiresParsing}},
  {{IsOngologyDescriptor}},
  NOT({{HasIdentity}}),
  {{DistanceFromConcept}}=2
)
```

**Formula for `FamilyFeudMismatch`:**
```
=IF(NOT({{Is_A_Family_Feud_Top_Answer}} = {{ChosenLanguageCandidate}}),
  {{Name}} & " " & IF({{Is_A_Family_Feud_Top_Answer}}, "Is", "Isn't") & " a Family Feud Language, but " & 
  IF({{ChosenLanguageCandidate}}, "Is", "Is Not") & " marked as a 'Language Candidate.'")
```

**Formula for `FamilyFuedQuestion`:**
```
="Is " & {{Name}} & " a language?"
```

**Formula for `RelationshipToConcept`:**
```
=IF({{DistanceFromConcept}} = 1, "IsMirrorOf", "IsDescriptionOf")
```

**Formula for `CategoryContainsLanguage`:**
```
=FIND("language", LOWER({{Category}})) > 0
```

**Formula for `HasGrammar`:**
```
={{HasSyntax}}
```


#### Sample Data (24 records)

| Field | Value |
|-------|-------|
| `LanguageCandidateId` | running-calculator-app |
| `Name` | Running Calculator App |
| `RequiresParsing` | true |
| `Category` | Running Software |
| `SortOrder` | 18 |
| `FamilyFuedQuestion` | Is Running Calculator App a language? |
| `HasIdentity` | true |
| `RelationshipToConcept` | IsMirrorOf |
| `DistanceFromConcept` | 1 |
| `Is_A_Family_Feud_Top_Answer` | false |
| `CanBeHeld` | false |
| `Meaning_Is_Serialized` | false |
| `IsOngologyDescriptor` | false |
| `HasSyntax` | false |
| `ChosenLanguageCandidate` | false |
| `FamilyFeudMismatch` |  |
| `CategoryContainsLanguage` | false |
| `HasGrammar` |  |

---


## Metadata

**Summary:** Airtable export with schema-first type mapping: Schemas, Data, Relationships (FK links), Lookups (INDEX/MATCH), Aggregations (SUMIFS/COUNTIFS/Rollups), and Calculated fields (formulas) in Excel dialect. Field types are determined from Airtable's schema metadata FIRST (no coercion), with intelligent fallback to formula/data analysis only when schema is unavailable.

### Conversion Details

| Property | Value |
|----------|-------|
| Source Base ID | `appC8XTj95lubn6hz` |
| Table Count | 2 |
| Tool Version | 2.0.0 |
| Export Mode | schema_first_type_mapping |
| Field Type Mapping | checkbox→boolean, number→number/integer, multipleRecordLinks→relationship, multipleLookupValues→lookup, rollup→aggregation, count→aggregation, formula→calculated |

### Type Inference

- **Enabled:** true
- **Priority:** airtable_metadata (NO COERCION) → formula_analysis → reference_resolution → data_analysis (fallback only)
- **Airtable Type Mapping:** checkbox→boolean, singleLineText→string, multilineText→string, number→number/integer, datetime→datetime, singleSelect→string, email→string, url→string, phoneNumber→string
- **Data Coercion Hierarchy:** Only used as fallback when Airtable schema unavailable: datetime → number → integer → boolean → base64 → json → string
- **Nullable Support:** true
- **Error Value Handling:** #NUM!, #ERROR!, #N/A, #REF!, #DIV/0!, #VALUE!, #NAME? are treated as NULL

---

*Generated from effortless-rulebook.json*

