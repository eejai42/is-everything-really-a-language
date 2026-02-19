# Test Results: english

## Summary

| Metric | Value |
|--------|-------|
| Total Fields Tested | 184 |
| Passed | 89 |
| Failed | 95 |
| Score | 48.4% |
| Duration | 1.42s |

## Results by Entity

### language_candidates

- Fields: 89/184 (48.4%)
- Computed columns: has_grammar, question, predicted_answer, prediction_predicates, prediction_fail, is_description_of, is_open_closed_world_conflicted, relationship_to_concept

| PK | Field | Expected | Actual |
|-----|-------|----------|--------|
| a-coffee-mug | question | Is A Coffee Mug a language? | None |
| a-coffee-mug | predicted_answer | False | None |
| a-coffee-mug | prediction_predicates | No Syntax & No Parsing Neede & | None |
| a-coffee-mug | relationship_to_concept | IsMirrorOf | IsDescriptionOf |
| a-game-of-fortnite | question | Is A Game of Fortnite a langua | None |
| a-game-of-fortnite | predicted_answer | False | None |
| a-game-of-fortnite | prediction_predicates | No Syntax & Requires Parsing & | None |
| a-game-of-fortnite | relationship_to_concept | IsMirrorOf | IsDescriptionOf |
| a-running-app | question | Is A Running App  a language? | None |
| a-running-app | predicted_answer | False | None |
| a-running-app | prediction_predicates | No Syntax & Requires Parsing & | None |
| a-running-app | relationship_to_concept | IsMirrorOf | IsDescriptionOf |
| a-smartphone | question | Is A Smartphone a language? | None |
| a-smartphone | predicted_answer | False | None |
| a-smartphone | prediction_predicates | No Syntax & No Parsing Neede & | None |
| a-smartphone | relationship_to_concept | IsMirrorOf | IsDescriptionOf |
| a-thunderstorm | question | Is A Thunderstorm a language? | None |
| a-thunderstorm | predicted_answer | False | None |
| a-thunderstorm | prediction_predicates | No Syntax & Requires Parsing & | None |
| a-thunderstorm | relationship_to_concept | IsMirrorOf | IsDescriptionOf |
| ... | ... | (75 more) | ... |
