# Test Results: uml

## Summary

| Metric | Value |
|--------|-------|
| Total Fields Tested | 184 |
| Passed | 138 |
| Failed | 46 |
| Score | 75.0% |
| Duration | 96ms |

## Results by Entity

### language_candidates

- Fields: 138/184 (75.0%)
- Computed columns: has_grammar, question, predicted_answer, prediction_predicates, prediction_fail, is_description_of, is_open_closed_world_conflicted, relationship_to_concept

| PK | Field | Expected | Actual |
|-----|-------|----------|--------|
| a-coffee-mug | prediction_predicates | No Syntax & No Parsing Neede & | No Syntax & No Parsing Neede & |
| a-coffee-mug | prediction_fail | None |  |
| a-game-of-fortnite | prediction_predicates | No Syntax & Requires Parsing & | No Syntax & Requires Parsing & |
| a-game-of-fortnite | prediction_fail | None |  |
| a-running-app | prediction_predicates | No Syntax & Requires Parsing & | No Syntax & Requires Parsing & |
| a-running-app | prediction_fail | None |  |
| a-smartphone | prediction_predicates | No Syntax & No Parsing Neede & | No Syntax & No Parsing Neede & |
| a-smartphone | prediction_fail | None |  |
| a-thunderstorm | prediction_predicates | No Syntax & Requires Parsing & | No Syntax & Requires Parsing & |
| a-thunderstorm | prediction_fail | None |  |
| a-uml-file | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| a-uml-file | prediction_fail | None |  |
| an-docx-doc | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| an-docx-doc | prediction_fail | None |  |
| an-xlsx-doc | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| an-xlsx-doc | prediction_fail | None |  |
| binary-code | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| binary-code | prediction_fail | None |  |
| docx-editing | prediction_predicates | No Syntax & No Parsing Neede & | No Syntax & No Parsing Neede & |
| docx-editing | prediction_fail | None |  |
| ... | ... | (26 more) | ... |
