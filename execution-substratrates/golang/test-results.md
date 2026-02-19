# Test Results: golang

## Summary

| Metric | Value |
|--------|-------|
| Total Fields Tested | 184 |
| Passed | 181 |
| Failed | 3 |
| Score | 98.4% |
| Duration | 100ms |

## Results by Entity

### language_candidates

- Fields: 181/184 (98.4%)
- Computed columns: has_grammar, question, predicted_answer, prediction_predicates, prediction_fail, is_description_of, is_open_closed_world_conflicted, relationship_to_concept

| PK | Field | Expected | Actual |
|-----|-------|----------|--------|
| falsifier-a | prediction_fail | None | Falsifier A Isn't a Family Feu |
| falsifier-b | prediction_fail | None | Falsifier B Is a Family Feud L |
| owa-cwa-falsifier | prediction_fail | None |  - Open World vs. Closed World |
