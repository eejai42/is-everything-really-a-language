// ERB SDK - Go Implementation (GENERATED - DO NOT EDIT)
// ======================================================
// Generated from: effortless-rulebook/effortless-rulebook.json
//
// This file contains structs and calculation functions
// for all tables defined in the rulebook.

package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
)

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

// boolVal safely dereferences a *bool, returning false if nil
func boolVal(b *bool) bool {
	if b == nil {
		return false
	}
	return *b
}

// stringVal safely dereferences a *string, returning "" if nil
func stringVal(s *string) string {
	if s == nil {
		return ""
	}
	return *s
}

// nilIfEmpty returns nil for empty strings, otherwise a pointer to the string
func nilIfEmpty(s string) *string {
	if s == "" {
		return nil
	}
	return &s
}

// intToString safely converts a *int to string, returning "" if nil
func intToString(i *int) string {
	if i == nil {
		return ""
	}
	return strconv.Itoa(*i)
}

// boolToString converts a bool to "true" or "false"
func boolToString(b bool) string {
	if b {
		return "true"
	}
	return "false"
}

// =============================================================================
// LANGUAGECANDIDATES TABLE
// =============================================================================

// LanguageCandidate represents a row in the LanguageCandidates table
type LanguageCandidate struct {
	LanguageCandidateId string `json:"language_candidate_id"`
	Name *string `json:"name"`
	IsLanguage *bool `json:"is_language"`
	HasSyntax *bool `json:"has_syntax"`
	CanBeHeld *bool `json:"can_be_held"`
	Category *string `json:"category"`
	HasIdentity *bool `json:"has_identity"`
	IsParsed *bool `json:"is_parsed"`
	ResolvesToAnAST *bool `json:"resolves_to_an_ast"`
	HasLinearDecodingPressure *bool `json:"has_linear_decoding_pressure"`
	IsStableOntologyReference *bool `json:"is_stable_ontology_reference"`
	IsLiveOntologyEditor *bool `json:"is_live_ontology_editor"`
	IsOpenWorld *bool `json:"is_open_world"`
	IsClosedWorld *bool `json:"is_closed_world"`
	DistanceFromConcept *int `json:"distance_from_concept"`
	DimensionalityWhileEditing *string `json:"dimensionality_while_editing"`
	ModelObjectFacilityLayer *string `json:"model_object_facility_layer"`
	SortOrder *int `json:"sort_order"`
	Bio_HasSemanticity *bool `json:"bio_has_semanticity"`
	Bio_HasArbitrariness *bool `json:"bio_has_arbitrariness"`
	Bio_HasDiscreteness *bool `json:"bio_has_discreteness"`
	Bio_HasDualityOfPatterning *bool `json:"bio_has_duality_of_patterning"`
	Bio_HasProductivity *bool `json:"bio_has_productivity"`
	Bio_HasDisplacement *bool `json:"bio_has_displacement"`
	Bio_HasCulturalTransmission *bool `json:"bio_has_cultural_transmission"`
	Bio_HasInterchangeability *bool `json:"bio_has_interchangeability"`
	Bio_HasFeedback *bool `json:"bio_has_feedback"`
	Bio_HasBroadcastTransmission *bool `json:"bio_has_broadcast_transmission"`
	Bio_HasRapidFading *bool `json:"bio_has_rapid_fading"`
	Bio_IsEvolvedCommunicationSystem *bool `json:"bio_is_evolved_communication_system"`
	Bio_PrimaryModality *string `json:"bio_primary_modality"`
	HasGrammar *bool `json:"has_grammar"`
	Question *string `json:"question"`
	PredictedAnswer *bool `json:"predicted_answer"`
	PredictedBiologicalLanguage_Core *bool `json:"predicted_biological_language_core"`
	PredictedBiologicalLanguage_Strict *bool `json:"predicted_biological_language_strict"`
	Bio_HockettScore *int `json:"bio_hockett_score"`
	PredictionPredicates *string `json:"prediction_predicates"`
	PredictionFail *string `json:"prediction_fail"`
	IsDescriptionOf *bool `json:"is_description_of"`
	IsOpenClosedWorldConflicted *bool `json:"is_open_closed_world_conflicted"`
	RelationshipToConcept *string `json:"relationship_to_concept"`
}

// --- Individual Calculation Functions ---

// CalcHasGrammar computes the HasGrammar calculated field
// Formula: ={{HasSyntax}} = TRUE()
func (tc *LanguageCandidate) CalcHasGrammar() bool {
	return (boolVal(tc.HasSyntax) == true)
}

// CalcQuestion computes the Question calculated field
// Formula: ="Is " & {{Name}} & " a language?"
func (tc *LanguageCandidate) CalcQuestion() string {
	return "Is " + stringVal(tc.Name) + " a language?"
}

// CalcPredictedAnswer computes the PredictedAnswer calculated field
// Formula: =OR(   AND(     {{HasSyntax}},     {{IsParsed}},     {{IsDescriptionOf}},     {{HasLinearDecodingPressure}},     {{ResolvesToAnAST}},     {{IsStableOntologyReference}},     NOT({{CanBeHeld}}),     NOT({{HasIdentity}})   ),   {{Bio_HockettScore}} > 0 )
func (tc *LanguageCandidate) CalcPredictedAnswer() bool {
	return ((boolVal(tc.HasSyntax) && boolVal(tc.IsParsed) && boolVal(tc.IsDescriptionOf) && boolVal(tc.HasLinearDecodingPressure) && boolVal(tc.ResolvesToAnAST) && boolVal(tc.IsStableOntologyReference) && !boolVal(tc.CanBeHeld) && !boolVal(tc.HasIdentity)) || (tc.Bio_HockettScore != nil && *tc.Bio_HockettScore > 0))
}

// CalcPredictedBiologicalLanguage_Core computes the PredictedBiologicalLanguage_Core calculated field
// Formula: =AND(   {{Bio_IsEvolvedCommunicationSystem}},   {{Bio_HasSemanticity}},   {{Bio_HasArbitrariness}},   {{Bio_HasDiscreteness}},   {{Bio_HasDualityOfPatterning}},   {{Bio_HasProductivity}},   {{Bio_HasDisplacement}},   {{Bio_HasCulturalTransmission}} )
func (tc *LanguageCandidate) CalcPredictedBiologicalLanguage_Core() bool {
	return (boolVal(tc.Bio_IsEvolvedCommunicationSystem) && boolVal(tc.Bio_HasSemanticity) && boolVal(tc.Bio_HasArbitrariness) && boolVal(tc.Bio_HasDiscreteness) && boolVal(tc.Bio_HasDualityOfPatterning) && boolVal(tc.Bio_HasProductivity) && boolVal(tc.Bio_HasDisplacement) && boolVal(tc.Bio_HasCulturalTransmission))
}

// CalcPredictedBiologicalLanguage_Strict computes the PredictedBiologicalLanguage_Strict calculated field
// Formula: =AND(   {{PredictedBiologicalLanguage_Core}},   {{Bio_HasInterchangeability}},   {{Bio_HasFeedback}} )
func (tc *LanguageCandidate) CalcPredictedBiologicalLanguage_Strict() bool {
	return (boolVal(tc.PredictedBiologicalLanguage_Core) && boolVal(tc.Bio_HasInterchangeability) && boolVal(tc.Bio_HasFeedback))
}

// CalcBio_HockettScore computes the Bio_HockettScore calculated field
// Formula: =SUM(IF({{Bio_HasSemanticity}},1,0), IF({{Bio_HasArbitrariness}},1,0), IF({{Bio_HasDiscreteness}},1,0), IF({{Bio_HasDualityOfPatterning}},1,0), IF({{Bio_HasProductivity}},1,0), IF({{Bio_HasDisplacement}},1,0), IF({{Bio_HasCulturalTransmission}},1,0), IF({{Bio_HasInterchangeability}},1,0), IF({{Bio_HasFeedback}},1,0), IF({{Bio_HasBroadcastTransmission}},1,0), IF({{Bio_HasRapidFading}},1,0))
func (tc *LanguageCandidate) CalcBio_HockettScore() int {
	return (func() int { if boolVal(tc.Bio_HasSemanticity) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasArbitrariness) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasDiscreteness) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasDualityOfPatterning) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasProductivity) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasDisplacement) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasCulturalTransmission) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasInterchangeability) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasFeedback) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasBroadcastTransmission) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasRapidFading) { return 1 }; return 0 }())
}

// CalcPredictionPredicates computes the PredictionPredicates calculated field
// Formula: =IF({{HasSyntax}}, "Has Syntax", "No Syntax") & " & " & IF({{IsParsed}}, "Requires Parsing", "No Parsing Neede") & " & " & IF({{IsDescriptionOf}}, "Describes the thing", "Is the Thing") & " & " & IF({{HasLinearDecodingPressure}}, "Has Linear Decoding Pressure", "No Decoding Pressure") & " & " & IF({{ResolvesToAnAST}}, "Resolves to AST", "No AST") & ", " & IF({{IsStableOntologyReference}}, "Is Stable Ontology", "Not 'Ontology'") & " AND " & IF({{CanBeHeld}}, "Can Be Held", "Can't Be Held") & ", " &IF({{HasIdentity}}, "Has Identity", "Has no Identity")
func (tc *LanguageCandidate) CalcPredictionPredicates() string {
	return func() string { if boolVal(tc.HasSyntax) { return "Has Syntax" }; return "No Syntax" }() + " & " + func() string { if boolVal(tc.IsParsed) { return "Requires Parsing" }; return "No Parsing Neede" }() + " & " + func() string { if boolVal(tc.IsDescriptionOf) { return "Describes the thing" }; return "Is the Thing" }() + " & " + func() string { if boolVal(tc.HasLinearDecodingPressure) { return "Has Linear Decoding Pressure" }; return "No Decoding Pressure" }() + " & " + func() string { if boolVal(tc.ResolvesToAnAST) { return "Resolves to AST" }; return "No AST" }() + ", " + func() string { if boolVal(tc.IsStableOntologyReference) { return "Is Stable Ontology" }; return "Not 'Ontology'" }() + " AND " + func() string { if boolVal(tc.CanBeHeld) { return "Can Be Held" }; return "Can't Be Held" }() + ", " + func() string { if boolVal(tc.HasIdentity) { return "Has Identity" }; return "Has no Identity" }()
}

// CalcPredictionFail computes the PredictionFail calculated field
// Formula: =IF(NOT({{PredictedAnswer}} = {{IsLanguage}}),   {{Name}} & " " & IF({{PredictedAnswer}}, "Is", "Isn't") & " a Family Feud Language, but " &    IF({{IsLanguage}}, "Is", "Is Not") & " marked as a 'Language Candidate.'", "") & IF({{IsOpenClosedWorldConflicted}}, " - Open World vs. Closed World Conflict.", "")
func (tc *LanguageCandidate) CalcPredictionFail() string {
	return func() string { if !((boolVal(tc.PredictedAnswer) == boolVal(tc.IsLanguage))) { return stringVal(tc.Name) + " " + func() string { if boolVal(tc.PredictedAnswer) { return "Is" }; return "Isn't" }() + " a Family Feud Language, but " + func() string { if boolVal(tc.IsLanguage) { return "Is" }; return "Is Not" }() + " marked as a 'Language Candidate.'" }; return "" }() + func() string { if boolVal(tc.IsOpenClosedWorldConflicted) { return " - Open World vs. Closed World Conflict." }; return "" }()
}

// CalcIsDescriptionOf computes the IsDescriptionOf calculated field
// Formula: ={{DistanceFromConcept}} > 1
func (tc *LanguageCandidate) CalcIsDescriptionOf() bool {
	return (tc.DistanceFromConcept != nil && *tc.DistanceFromConcept > 1)
}

// CalcIsOpenClosedWorldConflicted computes the IsOpenClosedWorldConflicted calculated field
// Formula: =AND({{IsOpenWorld}}, {{IsClosedWorld}})
func (tc *LanguageCandidate) CalcIsOpenClosedWorldConflicted() bool {
	return (boolVal(tc.IsOpenWorld) && boolVal(tc.IsClosedWorld))
}

// CalcRelationshipToConcept computes the RelationshipToConcept calculated field
// Formula: =IF({{DistanceFromConcept}} = 1, "IsMirrorOf", "IsDescriptionOf")
func (tc *LanguageCandidate) CalcRelationshipToConcept() string {
	return func() string { if (tc.DistanceFromConcept != nil && *tc.DistanceFromConcept == 1) { return "IsMirrorOf" }; return "IsDescriptionOf" }()
}

// --- Compute All Calculated Fields ---

// ComputeAll computes all calculated fields and returns an updated struct
func (tc *LanguageCandidate) ComputeAll() *LanguageCandidate {
	// Level 1 calculations
	hasGrammar := (boolVal(tc.HasSyntax) == true)
	question := "Is " + stringVal(tc.Name) + " a language?"
	predictedBiologicalLanguage_Core := (boolVal(tc.Bio_IsEvolvedCommunicationSystem) && boolVal(tc.Bio_HasSemanticity) && boolVal(tc.Bio_HasArbitrariness) && boolVal(tc.Bio_HasDiscreteness) && boolVal(tc.Bio_HasDualityOfPatterning) && boolVal(tc.Bio_HasProductivity) && boolVal(tc.Bio_HasDisplacement) && boolVal(tc.Bio_HasCulturalTransmission))
	bio_HockettScore := (func() int { if boolVal(tc.Bio_HasSemanticity) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasArbitrariness) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasDiscreteness) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasDualityOfPatterning) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasProductivity) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasDisplacement) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasCulturalTransmission) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasInterchangeability) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasFeedback) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasBroadcastTransmission) { return 1 }; return 0 }() + func() int { if boolVal(tc.Bio_HasRapidFading) { return 1 }; return 0 }())
	isDescriptionOf := (tc.DistanceFromConcept != nil && *tc.DistanceFromConcept > 1)
	isOpenClosedWorldConflicted := (boolVal(tc.IsOpenWorld) && boolVal(tc.IsClosedWorld))
	relationshipToConcept := func() string { if (tc.DistanceFromConcept != nil && *tc.DistanceFromConcept == 1) { return "IsMirrorOf" }; return "IsDescriptionOf" }()

	// Level 2 calculations
	predictedAnswer := ((boolVal(tc.HasSyntax) && boolVal(tc.IsParsed) && isDescriptionOf && boolVal(tc.HasLinearDecodingPressure) && boolVal(tc.ResolvesToAnAST) && boolVal(tc.IsStableOntologyReference) && !boolVal(tc.CanBeHeld) && !boolVal(tc.HasIdentity)) || (bio_HockettScore > 0))
	predictedBiologicalLanguage_Strict := (predictedBiologicalLanguage_Core && boolVal(tc.Bio_HasInterchangeability) && boolVal(tc.Bio_HasFeedback))
	predictionPredicates := func() string { if boolVal(tc.HasSyntax) { return "Has Syntax" }; return "No Syntax" }() + " & " + func() string { if boolVal(tc.IsParsed) { return "Requires Parsing" }; return "No Parsing Neede" }() + " & " + func() string { if isDescriptionOf { return "Describes the thing" }; return "Is the Thing" }() + " & " + func() string { if boolVal(tc.HasLinearDecodingPressure) { return "Has Linear Decoding Pressure" }; return "No Decoding Pressure" }() + " & " + func() string { if boolVal(tc.ResolvesToAnAST) { return "Resolves to AST" }; return "No AST" }() + ", " + func() string { if boolVal(tc.IsStableOntologyReference) { return "Is Stable Ontology" }; return "Not 'Ontology'" }() + " AND " + func() string { if boolVal(tc.CanBeHeld) { return "Can Be Held" }; return "Can't Be Held" }() + ", " + func() string { if boolVal(tc.HasIdentity) { return "Has Identity" }; return "Has no Identity" }()

	// Level 3 calculations
	predictionFail := func() string { if !((predictedAnswer == boolVal(tc.IsLanguage))) { return stringVal(tc.Name) + " " + func() string { if predictedAnswer { return "Is" }; return "Isn't" }() + " a Family Feud Language, but " + func() string { if boolVal(tc.IsLanguage) { return "Is" }; return "Is Not" }() + " marked as a 'Language Candidate.'" }; return "" }() + func() string { if isOpenClosedWorldConflicted { return " - Open World vs. Closed World Conflict." }; return "" }()

	return &LanguageCandidate{
		LanguageCandidateId: tc.LanguageCandidateId,
		Name: tc.Name,
		IsLanguage: tc.IsLanguage,
		HasSyntax: tc.HasSyntax,
		CanBeHeld: tc.CanBeHeld,
		Category: tc.Category,
		HasIdentity: tc.HasIdentity,
		IsParsed: tc.IsParsed,
		ResolvesToAnAST: tc.ResolvesToAnAST,
		HasLinearDecodingPressure: tc.HasLinearDecodingPressure,
		IsStableOntologyReference: tc.IsStableOntologyReference,
		IsLiveOntologyEditor: tc.IsLiveOntologyEditor,
		IsOpenWorld: tc.IsOpenWorld,
		IsClosedWorld: tc.IsClosedWorld,
		DistanceFromConcept: tc.DistanceFromConcept,
		DimensionalityWhileEditing: tc.DimensionalityWhileEditing,
		ModelObjectFacilityLayer: tc.ModelObjectFacilityLayer,
		SortOrder: tc.SortOrder,
		Bio_HasSemanticity: tc.Bio_HasSemanticity,
		Bio_HasArbitrariness: tc.Bio_HasArbitrariness,
		Bio_HasDiscreteness: tc.Bio_HasDiscreteness,
		Bio_HasDualityOfPatterning: tc.Bio_HasDualityOfPatterning,
		Bio_HasProductivity: tc.Bio_HasProductivity,
		Bio_HasDisplacement: tc.Bio_HasDisplacement,
		Bio_HasCulturalTransmission: tc.Bio_HasCulturalTransmission,
		Bio_HasInterchangeability: tc.Bio_HasInterchangeability,
		Bio_HasFeedback: tc.Bio_HasFeedback,
		Bio_HasBroadcastTransmission: tc.Bio_HasBroadcastTransmission,
		Bio_HasRapidFading: tc.Bio_HasRapidFading,
		Bio_IsEvolvedCommunicationSystem: tc.Bio_IsEvolvedCommunicationSystem,
		Bio_PrimaryModality: tc.Bio_PrimaryModality,
		HasGrammar: &hasGrammar,
		Question: nilIfEmpty(question),
		PredictedAnswer: &predictedAnswer,
		PredictedBiologicalLanguage_Core: &predictedBiologicalLanguage_Core,
		PredictedBiologicalLanguage_Strict: &predictedBiologicalLanguage_Strict,
		Bio_HockettScore: &bio_HockettScore,
		PredictionPredicates: nilIfEmpty(predictionPredicates),
		PredictionFail: nilIfEmpty(predictionFail),
		IsDescriptionOf: &isDescriptionOf,
		IsOpenClosedWorldConflicted: &isOpenClosedWorldConflicted,
		RelationshipToConcept: nilIfEmpty(relationshipToConcept),
	}
}

// =============================================================================
// ISEVERYTHINGALANGUAGE TABLE
// =============================================================================

// IsEverythingALanguage represents a row in the IsEverythingALanguage table
type IsEverythingALanguage struct {
	IsEverythingALanguageId string `json:"is_everything_a_language_id"`
	Name *string `json:"name"`
	ArgumentName *string `json:"argument_name"`
	ArgumentCategory *string `json:"argument_category"`
	StepType *string `json:"step_type"`
	Statement *string `json:"statement"`
	Formalization *string `json:"formalization"`
	RelatedCandidateName *string `json:"related_candidate_name"`
	RelatedCandidateId *string `json:"related_candidate_id"`
	EvidenceFromRulebook *string `json:"evidence_from_rulebook"`
	Notes *string `json:"notes"`
}

// =============================================================================
// ERBCUSTOMIZATIONS TABLE
// =============================================================================

// ERBCustomization represents a row in the ERBCustomizations table
type ERBCustomization struct {
	ERBCustomizationId string `json:"erb_customization_id"`
	Name *string `json:"name"`
	Title *string `json:"title"`
	SQLCode *string `json:"sql_code"`
	SQLTarget *string `json:"sql_target"`
	CustomizationType *string `json:"customization_type"`
}

// =============================================================================
// FILE I/O FUNCTIONS (for all tables with calculated fields)
// =============================================================================

// LoadLanguageCandidateRecords loads LanguageCandidates records from a JSON file
func LoadLanguageCandidateRecords(path string) ([]LanguageCandidate, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("failed to read file: %w", err)
	}

	var records []LanguageCandidate
	if err := json.Unmarshal(data, &records); err != nil {
		return nil, fmt.Errorf("failed to parse file: %w", err)
	}

	return records, nil
}

// SaveLanguageCandidateRecords saves computed LanguageCandidates records to a JSON file
func SaveLanguageCandidateRecords(path string, records []LanguageCandidate) error {
	data, err := json.MarshalIndent(records, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal records: %w", err)
	}

	if err := os.WriteFile(path, data, 0644); err != nil {
		return fmt.Errorf("failed to write records: %w", err)
	}

	return nil
}
