-- ============================================================================
-- SOURCE: ERBCustomizations table, record: 02b-customize-functions.sql
-- If you see SQL errors below, check this customization in Airtable
-- ============================================================================

-- Prediction Fail: Returns TRUE when predicted_answer doesn't match is_language
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
