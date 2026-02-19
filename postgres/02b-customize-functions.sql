-- ============================================================================
-- SOURCE: ERBCustomizations table, record: 03b-customize-functions.sql
-- If you see SQL errors below, check this customization in Airtable
-- ============================================================================

-- Formula: ="Is " & {{Name}} & " a language?"
CREATE OR REPLACE FUNCTION calc_language_candidates_family_feud_question(p_language_candidate_id TEXT)
RETURNS TEXT AS $$
  SELECT 'Is ' || COALESCE(name, '') || ' a language?'
  FROM language_candidates
  WHERE language_candidate_id = p_language_candidate_id;
$$ LANGUAGE SQL STABLE SECURITY DEFINER;

CREATE OR REPLACE FUNCTION public.calc_language_candidates_question(p_language_candidate_id text)
 RETURNS text
 LANGUAGE plpgsql
 STABLE SECURITY DEFINER
AS $function$
BEGIN
  RETURN ('Is ' || (SELECT NULLIF(name, '''') FROM language_candidates WHERE language_candidate_id = p_language_candidate_id) || ' a language?')::text;
END;
$function$;


-- Formula: =IF(NOT({{PredictedAnswer}} = {{IsLanguage}}),
--   {{Name}} & " " & IF({{PredictedAnswer}}, "Is", "Isn't") & " a Family Feud Language, but " &
--   IF({{IsLanguage}}, "Is", "Is Not") & " marked as a 'Language Candidate.'") &
--   IF({{IsOpenClosedWorldConflicted}}, " - Open World vs. Closed World Conflict.")
CREATE OR REPLACE FUNCTION calc_language_candidates_family_feud_mismatch(p_language_candidate_id TEXT)
RETURNS TEXT AS $$
  SELECT
    CASE
      WHEN COALESCE(calc_language_candidates_predicted_answer(p_language_candidate_id), FALSE)
           = COALESCE(is_language, FALSE)
      THEN
        CASE
          WHEN calc_language_candidates_is_open_closed_world_conflicted(p_language_candidate_id)
          THEN ' - Open World vs. Closed World Conflict.'
          ELSE NULL
        END
      ELSE name || ' ' ||
           CASE WHEN calc_language_candidates_predicted_answer(p_language_candidate_id) THEN 'Is' ELSE 'Isn''t' END ||
           ' a Family Feud Language, but ' ||
           CASE WHEN is_language THEN 'Is' ELSE 'Is Not' END ||
           ' marked as a ''Language Candidate.''' ||
           CASE
             WHEN calc_language_candidates_is_open_closed_world_conflicted(p_language_candidate_id)
             THEN ' - Open World vs. Closed World Conflict.'
             ELSE ''
           END
    END
  FROM language_candidates
  WHERE language_candidate_id = p_language_candidate_id;
$$ LANGUAGE SQL STABLE SECURITY DEFINER;