# Test Results: english

## Summary

| Metric | Value |
|--------|-------|
| Total Fields Tested | 363 |
| Passed | 256 |
| Failed | 107 |
| Score | 70.5% |
| Duration | 4m 26s |

## Results by Entity

### language_candidates

- Fields: 256/363 (70.5%)
- Computed columns: has_grammar, question, predicted_answer, predicted_biological_language_core, predicted_biological_language_strict, bio_hockett_score, prediction_predicates, prediction_fail, is_description_of, is_open_closed_world_conflicted, relationship_to_concept

| PK | Field | Expected | Actual |
|-----|-------|----------|--------|
| a-coffee-mug | prediction_predicates | No Syntax & No Parsing Neede & | No Syntax & No Parsing Needed  |
| a-coffee-mug | prediction_fail |  | A Coffee Mug Isn't a Family Fe |
| a-coffee-mug | relationship_to_concept | IsMirrorOf | IsDescriptionOf |
| a-game-of-fortnite | prediction_fail |  | A Game of Fortnite Isn't a Fam |
| a-game-of-fortnite | relationship_to_concept | IsMirrorOf | IsDescriptionOf |
| a-running-app | prediction_fail |  | A Running App  Isn't a Family  |
| a-running-app | relationship_to_concept | IsMirrorOf | IsDescriptionOf |
| a-smartphone | prediction_predicates | No Syntax & No Parsing Neede & | No Syntax & No Parsing Needed  |
| a-smartphone | prediction_fail |  | A Smartphone Isn't a Family Fe |
| a-smartphone | relationship_to_concept | IsMirrorOf | IsDescriptionOf |
| a-thunderstorm | prediction_fail |  | A Thunderstorm Isn't a Family  |
| a-thunderstorm | relationship_to_concept | IsMirrorOf | IsDescriptionOf |
| a-uml-file | bio_hockett_score | 0 | 8 |
| a-uml-file | is_description_of | True | False |
| an-docx-doc | bio_hockett_score | 0 | 8 |
| an-docx-doc | is_description_of | True | False |
| an-xlsx-doc | bio_hockett_score | 0 | 8 |
| an-xlsx-doc | is_description_of | True | False |
| ant-pheromone-trail-system | predicted_answer | True | False |
| ant-pheromone-trail-system | predicted_biological_language_core | False | True |
| ... | ... | (87 more) | ... |
