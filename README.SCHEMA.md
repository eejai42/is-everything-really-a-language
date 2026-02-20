# Effortless Rulebook

### Generated from:

> This builds ssotme tools including those that are disabled which regenerates this file.

```
$ cd ./docs
$ ssotme -build -id
```


> CMCC rulebook generated directly from Airtable base.

**Model ID:** `appEMeBJDL9wcHWOS`

---

## Formal Arguments

The following logical argument establishes that "language" can be formalized as a computable classification, and demonstrates that not everything qualifies as a language under this definition.


## Language Candidates

The following entities have been evaluated against the operational definition of "language" using testable predicates.

| Name | Category | Is Language? | HasSyntax | RequiresParsing | HasLinearDecodingPressure | StableOntologyReference | README |
|------|----------|--------------|-----------|-----------------|---------------------------|-------------------------|--------|

### Predicate Legend

| Predicate | Description |
|-----------|-------------|
| **HasSyntax** | Has formal syntactic rules governing valid expressions |
| **RequiresParsing** | Understanding requires parsing/interpreting structured input |
| **HasLinearDecodingPressure** | Requires sequential/linear interpretation to extract meaning |
| **StableOntologyReference** | Provides stable references to concepts over time |

---

## Table Schemas

### Table: Customers

> Table: Customers

#### Schema

| Field | Type | Data Type | Nullable | Description |
|-------|------|-----------|----------|-------------|
| `CustomerId` | raw | string | No | - |
| `Customer` | raw | string | Yes | - |
| `EmailAddress` | raw | string | Yes | - |
| `FirstName` | raw | string | Yes | - |
| `LastName` | raw | string | Yes | - |
| `FullName` | calculated | string | Yes | - |

**Formula for `FullName`:**
```
={{FirstName}} & " " & {{LastName}}
```


#### Sample Data (3 records)

| Field | Value |
|-------|-------|
| `CustomerId` | cust0001 |
| `Customer` | CUST0001 |
| `EmailAddress` | jane.smith@email.com |
| `FirstName` | Jane |
| `LastName` | Smith |
| `FullName` | Jane Smith |

---


## Metadata

**Summary:** Airtable export with schema-first type mapping: Schemas, Data, Relationships (FK links), Lookups (INDEX/MATCH), Aggregations (SUMIFS/COUNTIFS/Rollups), and Calculated fields (formulas) in Excel dialect. Field types are determined from Airtable's schema metadata FIRST (no coercion), with intelligent fallback to formula/data analysis only when schema is unavailable.

### Conversion Details

| Property | Value |
|----------|-------|
| Source Base ID | `appEMeBJDL9wcHWOS` |
| Table Count | 1 |
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

