# Test Results: xlsx

## Summary

| Metric | Value |
|--------|-------|
| Total Fields Tested | 184 |
| Passed | 158 |
| Failed | 26 |
| Score | 85.9% |
| Duration | 313ms |

## Results by Entity

### language_candidates

- Fields: 158/184 (85.9%)
- Computed columns: has_grammar, question, predicted_answer, prediction_predicates, prediction_fail, is_description_of, is_open_closed_world_conflicted, relationship_to_concept

| PK | Field | Expected | Actual |
|-----|-------|----------|--------|
| a-coffee-mug | prediction_predicates | No Syntax & No Parsing Neede & | No Syntax & No Parsing Neede & |
| a-game-of-fortnite | prediction_predicates | No Syntax & Requires Parsing & | No Syntax & Requires Parsing & |
| a-running-app | prediction_predicates | No Syntax & Requires Parsing & | No Syntax & Requires Parsing & |
| a-smartphone | prediction_predicates | No Syntax & No Parsing Neede & | No Syntax & No Parsing Neede & |
| a-thunderstorm | prediction_predicates | No Syntax & Requires Parsing & | No Syntax & Requires Parsing & |
| a-uml-file | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| an-docx-doc | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| an-xlsx-doc | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| binary-code | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| docx-editing | prediction_predicates | No Syntax & No Parsing Neede & | No Syntax & No Parsing Neede & |
| editing-airtable-base | prediction_predicates | No Syntax & No Parsing Neede & | No Syntax & No Parsing Neede & |
| english | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| falsifier-a | prediction_predicates | No Syntax & Requires Parsing & | No Syntax & Requires Parsing & |
| falsifier-a | prediction_fail | None | Falsifier A Isn't a Family Feu |
| falsifier-b | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| falsifier-b | prediction_fail | None | Falsifier B Is a Family Feud L |
| math | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| owa-cwa-falsifier | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| owa-cwa-falsifier | prediction_fail | None |  - Open World vs. Closed World |
| owl-rdf-graphql-generally | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| ... | ... | (6 more) | ... |
