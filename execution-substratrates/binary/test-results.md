# Test Results: binary

## Summary

| Metric | Value |
|--------|-------|
| Total Fields Tested | 184 |
| Passed | 100 |
| Failed | 84 |
| Score | 54.3% |
| Duration | 0.3s |

## Results by Entity

### language_candidates

- Fields: 100/184 (54.3%)
- Computed columns: has_grammar, question, predicted_answer, prediction_predicates, prediction_fail, is_description_of, is_open_closed_world_conflicted, relationship_to_concept

| PK | Field | Expected | Actual |
|-----|-------|----------|--------|
| a-coffee-mug | question | Is A Coffee Mug a language? | None |
| a-coffee-mug | prediction_predicates | No Syntax, No Parsing Needed,  | None |
| a-coffee-mug | relationship_to_concept | IsMirrorOf | None |
| a-game-of-fortnite | question | Is A Game of Fortnite a langua | None |
| a-game-of-fortnite | prediction_predicates | No Syntax, Requires Parsing, I | None |
| a-game-of-fortnite | relationship_to_concept | IsMirrorOf | None |
| a-running-app | question | Is A Running App  a language? | None |
| a-running-app | prediction_predicates | No Syntax, Requires Parsing, I | None |
| a-running-app | relationship_to_concept | IsMirrorOf | None |
| a-smartphone | question | Is A Smartphone a language? | None |
| a-smartphone | prediction_predicates | No Syntax, No Parsing Needed,  | None |
| a-smartphone | relationship_to_concept | IsMirrorOf | None |
| a-thunderstorm | question | Is A Thunderstorm a language? | None |
| a-thunderstorm | prediction_predicates | No Syntax, Requires Parsing, I | None |
| a-thunderstorm | relationship_to_concept | IsMirrorOf | None |
| a-uml-file | question | Is A UML File a language? | None |
| a-uml-file | predicted_answer | True | False |
| a-uml-file | prediction_predicates | Has Syntax, Requires Parsing,  | None |
| a-uml-file | relationship_to_concept | IsDescriptionOf | None |
| an-docx-doc | question | Is An DOCX Doc a language? | None |
| ... | ... | (64 more) | ... |
