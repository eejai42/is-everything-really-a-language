# Test Results: english

## Summary

| Metric | Value |
|--------|-------|
| Total Fields Tested | 184 |
| Passed | 132 |
| Failed | 52 |
| Score | 71.7% |
| Duration | 3m 49s |

## Results by Entity

### language_candidates

- Fields: 132/184 (71.7%)
- Computed columns: has_grammar, question, predicted_answer, prediction_predicates, prediction_fail, is_description_of, is_open_closed_world_conflicted, relationship_to_concept

| PK | Field | Expected | Actual |
|-----|-------|----------|--------|
| a-coffee-mug | prediction_predicates | No Syntax & No Parsing Neede & | No Syntax & No Parsing Needed  |
| a-coffee-mug | prediction_fail |  | A Coffee Mug Isn't a Family Fe |
| a-coffee-mug | is_description_of | False | True |
| a-coffee-mug | relationship_to_concept | IsMirrorOf | IsDescriptionOf |
| a-game-of-fortnite | prediction_fail |  | A Game of Fortnite Isn't a Fam |
| a-game-of-fortnite | is_description_of | False | True |
| a-game-of-fortnite | relationship_to_concept | IsMirrorOf | IsDescriptionOf |
| a-running-app | prediction_fail |  | A Running App  Isn't a Family  |
| a-running-app | is_description_of | False | True |
| a-running-app | relationship_to_concept | IsMirrorOf | IsDescriptionOf |
| a-smartphone | prediction_predicates | No Syntax & No Parsing Neede & | No Syntax & No Parsing Needed  |
| a-smartphone | prediction_fail |  | A Smartphone Isn't a Family Fe |
| a-smartphone | is_description_of | False | True |
| a-smartphone | relationship_to_concept | IsMirrorOf | IsDescriptionOf |
| a-thunderstorm | prediction_fail |  | A Thunderstorm Isn't a Family  |
| a-thunderstorm | is_description_of | False | True |
| a-thunderstorm | relationship_to_concept | IsMirrorOf | IsDescriptionOf |
| a-uml-file | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| an-docx-doc | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| an-xlsx-doc | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| ... | ... | (32 more) | ... |
