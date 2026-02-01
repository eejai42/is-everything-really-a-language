-- ============================================================================
-- CUSTOM FUNCTIONS - User-defined calculation functions
-- ============================================================================
-- DAG Level 3: Only references Level 2 (top_family_feud_answer) and Level 0 (raw fields)
-- ============================================================================
CREATE OR REPLACE FUNCTION calc_language_candidates_family_feud_mismatch(p_language_candidate_id TEXT)
RETURNS TEXT AS $$
  SELECT
    CASE
      WHEN COALESCE(calc_language_candidates_top_family_feud_answer(p_language_candidate_id), FALSE)
           = COALESCE(chosen_language_candidate, FALSE)
      THEN NULL
      ELSE name || ' ' ||
           CASE WHEN calc_language_candidates_top_family_feud_answer(p_language_candidate_id) THEN 'Is' ELSE 'Isn''t' END ||
           ' a Family Feud Language, but ' ||
           CASE WHEN chosen_language_candidate THEN 'Is' ELSE 'Is Not' END ||
           ' marked as a ''Language Candidate.'''
    END
  FROM language_candidates
  WHERE language_candidate_id = p_language_candidate_id;
$$ LANGUAGE SQL STABLE SECURITY DEFINER;


CREATE OR REPLACE FUNCTION public.calc_language_candidates_family_fued_question(p_language_candidate_id text)
 RETURNS text
 LANGUAGE plpgsql
 STABLE SECURITY DEFINER
AS $function$
BEGIN
  RETURN ('Is ' || (SELECT NULLIF(name, '') FROM language_candidates WHERE language_candidate_id = p_language_candidate_id) || ' a language?')::text;
END;
$function$
