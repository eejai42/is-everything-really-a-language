# Test Results: binary

## Summary

| Metric | Value |
|--------|-------|
| Total Fields Tested | 184 |
| Passed | 147 |
| Failed | 37 |
| Score | 79.9% |
| Duration | 0.3s |

## Results by Entity

### language_candidates

- Fields: 147/184 (79.9%)
- Computed columns: has_grammar, question, predicted_answer, prediction_predicates, prediction_fail, is_description_of, is_open_closed_world_conflicted, relationship_to_concept

| PK | Field | Expected | Actual |
|-----|-------|----------|--------|
| a-uml-file | predicted_answer | True | False |
| a-uml-file | prediction_predicates | Has Syntax, Requires Parsing,  | Has Syntax, Requires Parsing,  |
| a-uml-file | prediction_fail |  | A UML File Isn't a Family Feud |
| an-docx-doc | predicted_answer | True | False |
| an-docx-doc | prediction_predicates | Has Syntax, Requires Parsing,  | Has Syntax, Requires Parsing,  |
| an-docx-doc | prediction_fail |  | An DOCX Doc Isn't a Family Feu |
| an-xlsx-doc | predicted_answer | True | False |
| an-xlsx-doc | prediction_predicates | Has Syntax, Requires Parsing,  | Has Syntax, Requires Parsing,  |
| an-xlsx-doc | prediction_fail |  | An XLSX Doc Isn't a Family Feu |
| binary-code | predicted_answer | True | False |
| binary-code | prediction_predicates | Has Syntax, Requires Parsing,  | Has Syntax, Requires Parsing,  |
| binary-code | prediction_fail |  | Binary Code Isn't a Family Feu |
| editing-airtable-base | prediction_predicates | No Syntax, No Parsing Needed,  | No Syntax, No Parsing Needed,  |
| english | predicted_answer | True | False |
| english | prediction_predicates | Has Syntax, Requires Parsing,  | Has Syntax, Requires Parsing,  |
| english | prediction_fail |  | English Isn't a Family Feud La |
| falsifier-b | predicted_answer | True | False |
| falsifier-b | prediction_predicates | Has Syntax, Requires Parsing,  | Has Syntax, Requires Parsing,  |
| falsifier-b | prediction_fail | Falsifier B Is a Family Feud L |  |
| math | predicted_answer | True | False |
| ... | ... | (17 more) | ... |
