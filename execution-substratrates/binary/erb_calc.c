/*
 * ERB Calculation Functions - Binary/Native Implementation
 * =========================================================
 *
 * This file implements ALL calculation functions from the ERB rulebook
 * as native C code. The computation logic is entirely in native code;
 * Python only handles JSON I/O and calls these functions via ctypes.
 *
 * Using libc functions (strlen, strcpy, strstr, etc.) is expected and allowed,
 * as these are standard library primitives, not computation logic.
 *
 * DAG Execution Order:
 *   Level 0: Raw fields (from JSON)
 *   Level 1: category_contains_language, has_grammar, relationship_to_concept, family_fued_question
 *   Level 2: is_a_family_feud_top_answer (depends on category_contains_language)
 *   Level 3: family_feud_mismatch (depends on is_a_family_feud_top_answer)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

/* Thread-local buffer for string returns */
static __thread char result_buffer[4096];

/*
 * Helper: Convert string to lowercase in-place
 */
static void str_tolower(char *str) {
    for (int i = 0; str[i]; i++) {
        str[i] = tolower((unsigned char)str[i]);
    }
}

/*
 * Level 1: calc_category_contains_language
 * ----------------------------------------
 * Formula: FIND("language", LOWER(category)) > 0
 * Returns: true if "language" appears in the lowercased category
 */
bool calc_category_contains_language(const char *category) {
    if (category == NULL || strlen(category) == 0) {
        return false;
    }

    /* Copy to buffer and lowercase */
    char lower_category[1024];
    strncpy(lower_category, category, sizeof(lower_category) - 1);
    lower_category[sizeof(lower_category) - 1] = '\0';
    str_tolower(lower_category);

    /* Search for "language" substring */
    return strstr(lower_category, "language") != NULL;
}

/*
 * Level 1: calc_has_grammar
 * -------------------------
 * Formula: {{HasSyntax}} = TRUE()
 * Returns: true if has_syntax is true, false otherwise
 */
bool calc_has_grammar(bool has_syntax) {
    return has_syntax;
}

/*
 * Level 1: calc_relationship_to_concept
 * -------------------------------------
 * Formula: IF(distance_from_concept = 1, "IsMirrorOf", "IsDescriptionOf")
 * Returns: pointer to static string
 */
const char* calc_relationship_to_concept(int distance_from_concept) {
    if (distance_from_concept == 1) {
        return "IsMirrorOf";
    }
    return "IsDescriptionOf";
}

/*
 * Level 1: calc_family_fued_question
 * ----------------------------------
 * Formula: "Is " & name & " a language?"
 * Returns: pointer to thread-local buffer with the result
 *
 * NOTE: The result is valid until the next call from the same thread.
 */
const char* calc_family_fued_question(const char *name) {
    const char *safe_name = (name != NULL) ? name : "";
    snprintf(result_buffer, sizeof(result_buffer), "Is %s a language?", safe_name);
    return result_buffer;
}

/*
 * Level 2: calc_is_a_family_feud_top_answer
 * -----------------------------------------
 * Formula: AND(
 *   category_contains_language,
 *   has_syntax,
 *   NOT(can_be_held),
 *   meaning_is_serialized,
 *   requires_parsing,
 *   is_ongology_descriptor,
 *   NOT(has_identity),
 *   distance_from_concept = 2
 * )
 *
 * Note: category_contains_language is computed internally (Level 1 dependency)
 */
bool calc_is_a_family_feud_top_answer(
    const char *category,
    bool has_syntax,
    bool can_be_held,
    bool meaning_is_serialized,
    bool requires_parsing,
    bool is_ongology_descriptor,
    bool has_identity,
    int distance_from_concept
) {
    /* Compute Level 1 dependency */
    bool category_contains_language = calc_category_contains_language(category);

    /* All conditions must be true (8-way AND) */
    return (
        category_contains_language &&
        has_syntax &&
        !can_be_held &&
        meaning_is_serialized &&
        requires_parsing &&
        is_ongology_descriptor &&
        !has_identity &&
        (distance_from_concept == 2)
    );
}

/*
 * Level 3: calc_family_feud_mismatch
 * ----------------------------------
 * Formula: IF(is_a_family_feud_top_answer != chosen_language_candidate,
 *   name & " " & IF(is_a_family_feud_top_answer, "Is", "Isn't") &
 *   " a Family Feud Language, but " &
 *   IF(chosen_language_candidate, "Is", "Is Not") &
 *   " marked as a 'Language Candidate.'",
 *   NULL
 * )
 *
 * Returns: pointer to thread-local buffer with result, or NULL if no mismatch
 */
const char* calc_family_feud_mismatch(
    const char *name,
    bool is_top_answer,
    bool chosen_language_candidate
) {
    /* If they match, return NULL */
    if (is_top_answer == chosen_language_candidate) {
        return NULL;
    }

    /* Build mismatch message */
    const char *safe_name = (name != NULL) ? name : "";
    const char *is_word = is_top_answer ? "Is" : "Isn't";
    const char *marked_word = chosen_language_candidate ? "Is" : "Is Not";

    snprintf(result_buffer, sizeof(result_buffer),
        "%s %s a Family Feud Language, but %s marked as a 'Language Candidate.'",
        safe_name, is_word, marked_word);

    return result_buffer;
}

/*
 * Convenience function: compute is_a_family_feud_top_answer and then mismatch
 * This wraps the Level 2 + Level 3 computation in one call.
 */
const char* calc_family_feud_mismatch_full(
    const char *name,
    const char *category,
    bool has_syntax,
    bool can_be_held,
    bool meaning_is_serialized,
    bool requires_parsing,
    bool is_ongology_descriptor,
    bool has_identity,
    int distance_from_concept,
    bool chosen_language_candidate
) {
    /* Compute Level 2 */
    bool is_top_answer = calc_is_a_family_feud_top_answer(
        category, has_syntax, can_be_held, meaning_is_serialized,
        requires_parsing, is_ongology_descriptor, has_identity, distance_from_concept
    );

    /* Compute Level 3 */
    return calc_family_feud_mismatch(name, is_top_answer, chosen_language_candidate);
}
