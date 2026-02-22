-- ============================================================================
-- SOURCE: ERBCustomizations table, record: 02b-customize-functions.sql
-- If you see SQL errors below, check this customization in Airtable
-- ============================================================================

-- Prediction Fail: Returns TRUE when predicted_answer doesn't match is_language
DROP FUNCTION IF EXISTS calc_language_candidates_prediction_fail_x;

CREATE OR REPLACE FUNCTION calc_language_candidates_prediction_fail_x(p_language_candidate_id TEXT)
RETURNS TEXT AS $$
  SELECT NULLIF(
    COALESCE(
      CASE
        WHEN COALESCE(calc_language_candidates_predicted_answer(p_language_candidate_id), FALSE)
             != COALESCE(is_language, FALSE)
        THEN name || ' ' ||
             CASE WHEN calc_language_candidates_predicted_answer(p_language_candidate_id) THEN 'Is' ELSE 'Isn''t' END ||
             ' a Family Feud Language, but ' ||
             CASE WHEN is_language THEN 'Is' ELSE 'Is Not' END ||
             ' marked as a ''Language Candidate.'''
      END,
      ''
    ) ||
    COALESCE(
      CASE
        WHEN calc_language_candidates_is_open_closed_world_conflicted(p_language_candidate_id)
        THEN ' - Open World vs. Closed World Conflict.'
      END,
      ''
    ),
    ''
  )
  FROM language_candidates
  WHERE language_candidate_id = p_language_candidate_id;
$$ LANGUAGE SQL STABLE SECURITY DEFINER;

DROP FUNCTION calc_language_candidates_question;

CREATE OR REPLACE FUNCTION public.calc_language_candidates_question(p_language_candidate_id text)
 RETURNS text
 LANGUAGE plpgsql
 STABLE SECURITY DEFINER
AS $function$
BEGIN
  RETURN ('Is ' || (SELECT NULLIF(name, '''') FROM language_candidates WHERE language_candidate_id = p_language_candidate_id) || ' a language?')::text;
END;
$function$
