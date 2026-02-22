# Test Results: english

## Summary

| Metric | Value |
|--------|-------|
| Total Fields Tested | 184 |
| Passed | 145 |
| Failed | 39 |
| Score | 78.8% |
| Duration | 2m 50.6s |

## Results by Entity

### language_candidates

- Fields: 145/184 (78.8%)
- Computed columns: has_grammar, question, predicted_answer, prediction_predicates, prediction_fail, is_description_of, is_open_closed_world_conflicted, relationship_to_concept

| PK | Field | Expected | Actual |
|-----|-------|----------|--------|
| a-coffee-mug | prediction_predicates | No Syntax, No Parsing Needed,  | No Syntax, No Parsing Needed,  |
| a-coffee-mug | prediction_fail |  | A Coffee Mug isn't a Family Fe |
| a-game-of-fortnite | prediction_predicates | No Syntax, Requires Parsing, I | No Syntax, Requires Parsing, I |
| a-game-of-fortnite | prediction_fail |  | A Game of Fortnite isn't a Fam |
| a-running-app | prediction_predicates | No Syntax, Requires Parsing, I | No Syntax, Requires Parsing, I |
| a-running-app | prediction_fail |  | A Running App  isn't a Family  |
| a-smartphone | prediction_predicates | No Syntax, No Parsing Needed,  | No Syntax, No Parsing Needed,  |
| a-smartphone | prediction_fail |  | A Smartphone isn't a Family Fe |
| a-thunderstorm | prediction_predicates | No Syntax, Requires Parsing, I | No Syntax, Requires Parsing, I |
| a-thunderstorm | prediction_fail |  | A Thunderstorm isn't a Family  |
| a-uml-file | prediction_predicates | Has Syntax, Requires Parsing,  | Has Syntax, Requires Parsing,  |
| an-docx-doc | prediction_predicates | Has Syntax, Requires Parsing,  | Has Syntax, Requires Parsing,  |
| an-xlsx-doc | prediction_predicates | Has Syntax, Requires Parsing,  | Has Syntax, Requires Parsing,  |
| binary-code | prediction_predicates | Has Syntax, Requires Parsing,  | Has Syntax, Requires Parsing,  |
| docx-editing | prediction_predicates | No Syntax, No Parsing Needed,  | No Syntax, No Parsing Needed,  |
| docx-editing | prediction_fail |  | DOCX - Editing isn't a Family  |
| editing-airtable-base | prediction_predicates | No Syntax, No Parsing Needed,  | No Syntax, No Parsing Needed,  |
| editing-airtable-base | prediction_fail |  | Editing Airtable Base isn't a  |
| editing-airtable-base | is_description_of | True | False |
| english | prediction_predicates | Has Syntax, Requires Parsing,  | Has Syntax, Requires Parsing,  |
| ... | ... | (19 more) | ... |
