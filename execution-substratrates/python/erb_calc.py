"""
ERB Calculation Library (GENERATED - DO NOT EDIT)
=================================================
Generated from: effortless-rulebook/effortless-rulebook.json

This file contains pure functions that compute calculated fields
from raw field values. Shared by Python and YAML substrates.
"""

from typing import Optional, Any


# =============================================================================
# LEVEL 1 CALCULATIONS
# =============================================================================

def calc_has_grammar(has_syntax):
    """Formula: ={{HasSyntax}} = TRUE()"""
    return (has_syntax == True)

def calc_question(name):
    """Formula: ="Is " & {{Name}} & " a language?" """
    return ('Is ' + str(name or "") + ' a language?')

def calc_is_description_of(distance_from_concept):
    """Formula: ={{DistanceFromConcept}} > 1"""
    return (distance_from_concept > 1)

def calc_is_open_closed_world_conflicted(is_open_world, is_closed_world):
    """Formula: =AND({{IsOpenWorld}}, {{IsClosedWorld}})"""
    return ((is_open_world is True) and (is_closed_world is True))

def calc_relationship_to_concept(distance_from_concept):
    """Formula: =IF({{DistanceFromConcept}} = 1, "IsMirrorOf", "IsDescriptionOf")"""
    return ('IsMirrorOf' if (distance_from_concept == 1) else 'IsDescriptionOf')


# =============================================================================
# LEVEL 2 CALCULATIONS
# =============================================================================

def calc_predicted_answer(has_syntax, requires_parsing, is_description_of, has_linear_decoding_pressure, resolves_to_an_ast, is_stable_ontology_reference, can_be_held, has_identity):
    """Formula: =AND(
  {{HasSyntax}},
  {{RequiresParsing}},
  {{IsDescriptionOf}},
  {{HasLinearDecodingPressure}},
  {{ResolvesToAnAST}},
  {{IsStableOntologyReference}},
  NOT({{CanBeHeld}}),
  NOT({{HasIdentity}})
)"""
    return ((has_syntax is True) and (requires_parsing is True) and (is_description_of is True) and (has_linear_decoding_pressure is True) and (resolves_to_an_ast is True) and (is_stable_ontology_reference is True) and (can_be_held is not True) and (has_identity is not True))

def calc_prediction_predicates(has_syntax, requires_parsing, is_description_of, has_linear_decoding_pressure, resolves_to_an_ast, is_stable_ontology_reference, can_be_held, has_identity):
    """Formula: =IF({{HasSyntax}}, "Has Syntax", "No Syntax") & " & " & IF({{RequiresParsing}}, "Requires Parsing", "No Parsing Neede") & " & " & IF({{IsDescriptionOf}}, "Describes the thing", "Is the Thing") & " & " & IF({{HasLinearDecodingPressure}}, "Has Linear Decoding Pressure", "No Decoding Pressure") & " & " & IF({{ResolvesToAnAST}}, "Resolves to AST", "No AST") & ", " &
"  " & IF({{IsStableOntologyReference}}, "Is Stable Ontology", "Not 'Ontology'") & "\\n AND " &
"  " & IF({{CanBeHeld}}, "Can Be Held", "Can't Be Held") & ", " &
"  " & IF({{HasIdentity}}, "Has Identity", "Has no Identity")"""
    return (str(('Has Syntax' if has_syntax else 'No Syntax') if ('Has Syntax' if has_syntax else 'No Syntax') is not None else "") + ' & ' + str(('Requires Parsing' if requires_parsing else 'No Parsing Neede') if ('Requires Parsing' if requires_parsing else 'No Parsing Neede') is not None else "") + ' & ' + str(('Describes the thing' if is_description_of else 'Is the Thing') if ('Describes the thing' if is_description_of else 'Is the Thing') is not None else "") + ' & ' + str(('Has Linear Decoding Pressure' if has_linear_decoding_pressure else 'No Decoding Pressure') if ('Has Linear Decoding Pressure' if has_linear_decoding_pressure else 'No Decoding Pressure') is not None else "") + ' & ' + str(('Resolves to AST' if resolves_to_an_ast else 'No AST') if ('Resolves to AST' if resolves_to_an_ast else 'No AST') is not None else "") + ', ' + '  ' + str(('Is Stable Ontology' if is_stable_ontology_reference else "Not 'Ontology'") if ('Is Stable Ontology' if is_stable_ontology_reference else "Not 'Ontology'") is not None else "") + '\\n AND ' + '  ' + str(('Can Be Held' if can_be_held else "Can't Be Held") if ('Can Be Held' if can_be_held else "Can't Be Held") is not None else "") + ', ' + '  ' + str(('Has Identity' if has_identity else 'Has no Identity') if ('Has Identity' if has_identity else 'Has no Identity') is not None else ""))


# =============================================================================
# LEVEL 3 CALCULATIONS
# =============================================================================

def calc_prediction_fail(predicted_answer, is_language, name, is_open_closed_world_conflicted):
    """Formula: =IF(NOT({{PredictedAnswer}} = {{IsLanguage}}),
  {{Name}} & " " & IF({{PredictedAnswer}}, "Is", "Isn't") & " a Family Feud Language, but " & 
  IF({{IsLanguage}}, "Is", "Is Not") & " marked as a 'Language Candidate.'") & IF({{IsOpenClosedWorldConflicted}}, " - Open World vs. Closed World Conflict.")"""
    return (str(((str(name or "") + ' ' + str(('Is' if predicted_answer else "Isn't") if ('Is' if predicted_answer else "Isn't") is not None else "") + ' a Family Feud Language, but ' + str(('Is' if is_language else 'Is Not') if ('Is' if is_language else 'Is Not') is not None else "") + " marked as a 'Language Candidate.'") if (not (predicted_answer == is_language)) else None) if ((str(name or "") + ' ' + str(('Is' if predicted_answer else "Isn't") if ('Is' if predicted_answer else "Isn't") is not None else "") + ' a Family Feud Language, but ' + str(('Is' if is_language else 'Is Not') if ('Is' if is_language else 'Is Not') is not None else "") + " marked as a 'Language Candidate.'") if (not (predicted_answer == is_language)) else None) is not None else "") + str((' - Open World vs. Closed World Conflict.' if is_open_closed_world_conflicted else None) if (' - Open World vs. Closed World Conflict.' if is_open_closed_world_conflicted else None) is not None else ""))


# =============================================================================
# COMPOSITE FUNCTION
# =============================================================================

def compute_all_calculated_fields(record: dict) -> dict:
    """
    Compute all calculated fields for a record.
    Generated from rulebook formulas.
    """
    result = dict(record)

    # Level 1 calculations
    result['has_grammar'] = calc_has_grammar(result.get('has_syntax'))
    result['question'] = calc_question(result.get('name'))
    result['is_description_of'] = calc_is_description_of(result.get('distance_from_concept'))
    result['is_open_closed_world_conflicted'] = calc_is_open_closed_world_conflicted(result.get('is_open_world'), result.get('is_closed_world'))
    result['relationship_to_concept'] = calc_relationship_to_concept(result.get('distance_from_concept'))

    # Level 2 calculations
    result['predicted_answer'] = calc_predicted_answer(result.get('has_syntax'), result.get('requires_parsing'), result.get('is_description_of'), result.get('has_linear_decoding_pressure'), result.get('resolves_to_an_ast'), result.get('is_stable_ontology_reference'), result.get('can_be_held'), result.get('has_identity'))
    result['prediction_predicates'] = calc_prediction_predicates(result.get('has_syntax'), result.get('requires_parsing'), result.get('is_description_of'), result.get('has_linear_decoding_pressure'), result.get('resolves_to_an_ast'), result.get('is_stable_ontology_reference'), result.get('can_be_held'), result.get('has_identity'))

    # Level 3 calculations
    result['prediction_fail'] = calc_prediction_fail(result.get('predicted_answer'), result.get('is_language'), result.get('name'), result.get('is_open_closed_world_conflicted'))

    # Convert empty strings to None for string fields
    for key in ['family_feud_mismatch']:
        if result.get(key) == '':
            result[key] = None

    return result