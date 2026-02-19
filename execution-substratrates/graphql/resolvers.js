/**
 * ERB SDK - GraphQL Resolvers (JavaScript)
 * =========================================
 * Generated from effortless-rulebook/effortless-rulebook.json
 *
 * All calculation functions are dynamically generated from rulebook formulas.
 */

// =============================================================================
// CALCULATED FIELD FUNCTIONS
// =============================================================================

// Level 1 calculations
// ----------------------------------------

/**
 * Formula: ={{HasSyntax}} = TRUE()
 */
function calcHasGrammar(candidate) {
  return (candidate.hasSyntax === true);
}

/**
 * Formula: ="Is " & {{Name}} & " a language?"
 */
function calcQuestion(candidate) {
  return `Is ${candidate.name || ""} a language?`;
}

/**
 * Formula: ={{DistanceFromConcept}} > 1
 */
function calcIsDescriptionOf(candidate) {
  return (candidate.distanceFromConcept > 1);
}

/**
 * Formula: =AND({{IsOpenWorld}}, {{IsClosedWorld}})
 */
function calcIsOpenClosedWorldConflicted(candidate) {
  return ((candidate.isOpenWorld === true) && (candidate.isClosedWorld === true));
}

/**
 * Formula: =IF({{DistanceFromConcept}} = 1, "IsMirrorOf", "IsDescriptionOf")
 */
function calcRelationshipToConcept(candidate) {
  return ((candidate.distanceFromConcept === 1) ? 'IsMirrorOf' : 'IsDescriptionOf');
}

// Level 2 calculations
// ----------------------------------------

/**
 * Formula: =AND(   {{HasSyntax}},   {{RequiresParsing}},   {{IsDescriptionOf}},   {{HasLinearDecodingPressure}},   {{ResolvesToAnAST}},   {{IsStableOntologyReference}},   NOT({{CanBeHeld}}),   NOT({{HasIdentity}}) )
 */
function calcPredictedAnswer(candidate) {
  return ((candidate.hasSyntax === true) && (candidate.requiresParsing === true) && (candidate.isDescriptionOf === true) && (candidate.hasLinearDecodingPressure === true) && (candidate.resolvesToAnAST === true) && (candidate.isStableOntologyReference === true) && ((candidate.canBeHeld !== true) === true) && ((candidate.hasIdentity !== true) === true));
}

/**
 * Formula: =IF({{HasSyntax}}, "Has Syntax", "No Syntax") & " & " & IF({{RequiresParsing}}, "Requires Parsing", "No Parsing Neede") & " & " & IF({{IsDescriptionOf}}, "Describes the thing", "Is the Thing") & " & " & IF({{HasLinearDecodingPressure}}, "Has Linear Decoding Pressure", "No Decoding Pressure") & " & " & IF({{ResolvesToAnAST}}, "Resolves to AST", "No AST") & ", " & "  " & IF({{IsStableOntologyReference}}, "Is Stable Ontology", "Not 'Ontology'") & "\n AND " & "  " & IF({{CanBeHeld}}, "Can Be Held", "Can't Be Held") & ", " & "  " & IF({{HasIdentity}}, "Has Identity", "Has no Identity")
 */
function calcPredictionPredicates(candidate) {
  return `${(candidate.hasSyntax ? 'Has Syntax' : 'No Syntax') || ""} & ${(candidate.requiresParsing ? 'Requires Parsing' : 'No Parsing Neede') || ""} & ${(candidate.isDescriptionOf ? 'Describes the thing' : 'Is the Thing') || ""} & ${(candidate.hasLinearDecodingPressure ? 'Has Linear Decoding Pressure' : 'No Decoding Pressure') || ""} & ${(candidate.resolvesToAnAST ? 'Resolves to AST' : 'No AST') || ""},   ${(candidate.isStableOntologyReference ? 'Is Stable Ontology' : 'Not \'Ontology\'') || ""}\\n AND   ${(candidate.canBeHeld ? 'Can Be Held' : 'Can\'t Be Held') || ""},   ${(candidate.hasIdentity ? 'Has Identity' : 'Has no Identity') || ""}`;
}

// Level 3 calculations
// ----------------------------------------

/**
 * Formula: =IF(NOT({{PredictedAnswer}} = {{IsLanguage}}),   {{Name}} & " " & IF({{PredictedAnswer}}, "Is", "Isn't") & " a Family Feud Language, but " &    IF({{IsLanguage}}, "Is", "Is Not") & " marked as a 'Language Candidate.'") & IF({{IsOpenClosedWorldConflicted}}, " - Open World vs. Closed World Conflict.")
 */
function calcPredictionFail(candidate) {
  return `${(((candidate.predictedAnswer === candidate.isLanguage) !== true) ? `${candidate.name || ""} ${(candidate.predictedAnswer ? 'Is' : 'Isn\'t') || ""} a Family Feud Language, but ${(candidate.isLanguage ? 'Is' : 'Is Not') || ""} marked as a 'Language Candidate.'` : null) || ""}${(candidate.isOpenClosedWorldConflicted ? ' - Open World vs. Closed World Conflict.' : null) || ""}`;
}

// =============================================================================
// EXPORTS
// =============================================================================

module.exports = {
  calcHasGrammar,
  calcQuestion,
  calcIsDescriptionOf,
  calcIsOpenClosedWorldConflicted,
  calcRelationshipToConcept,
  calcPredictedAnswer,
  calcPredictionPredicates,
  calcPredictionFail,
};
