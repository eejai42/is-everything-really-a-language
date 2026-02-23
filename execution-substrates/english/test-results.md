# Test Results: english

## Summary

| Metric | Value |
|--------|-------|
| Total Fields Tested | 184 |
| Passed | 118 |
| Failed | 66 |
| Score | 64.1% |
| Duration | 1m 24s |

## Results by Entity

### language_candidates

- Fields: 118/184 (64.1%)
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
| a-thunderstorm | prediction_predicates | No Syntax & Requires Parsing & | No Syntax & Requires Parsing & |
| a-thunderstorm | prediction_fail |  | A Thunderstorm Isn't a Family  |
| a-thunderstorm | is_description_of | False | True |
| a-thunderstorm | relationship_to_concept | IsMirrorOf | IsDescriptionOf |
| a-uml-file | prediction_predicates | Has Syntax & Requires Parsing  | Has Syntax & Requires Parsing  |
| a-uml-file | is_description_of | True | False |
| ... | ... | (46 more) | ... |
