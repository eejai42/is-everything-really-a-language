// ERB SDK - Go Implementation
// ============================
// Mirrors the PostgreSQL functions from postgres/02-create-functions.sql
// Source: effortless-rulebook/effortless-rulebook.json
//
// DAG Execution Order:
//   Level 0: Raw fields
//   Level 1: CategoryContainsLanguage, HasGrammar, RelationshipToConcept, FamilyFuedQuestion
//   Level 2: IsAFamilyFeudTopAnswer (depends on CategoryContainsLanguage)
//   Level 3: FamilyFeudMismatch (depends on IsAFamilyFeudTopAnswer)

package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

// LanguageCandidate represents a candidate item to evaluate whether it qualifies as a 'language'
type LanguageCandidate struct {
	// Primary Key
	LanguageCandidateID string `json:"LanguageCandidateId"`

	// Raw Fields
	Name                    *string `json:"Name"`
	Category                *string `json:"Category"`
	CanBeHeld               *bool   `json:"CanBeHeld"`
	MeaningIsSerialized     *bool   `json:"MeaningIsSerialized"`
	RequiresParsing         *bool   `json:"RequiresParsing"`
	IsOngologyDescriptor    *bool   `json:"IsOngologyDescriptor"`
	HasSyntax               *bool   `json:"HasSyntax"`
	ChosenLanguageCandidate *bool   `json:"ChosenLanguageCandidate"`
	SortOrder               *int    `json:"SortOrder"`
	HasIdentity             *bool   `json:"HasIdentity"`
	DistanceFromConcept     *int    `json:"DistanceFromConcept"`
}

// =============================================================================
// CALCULATED FIELDS - Mirrors PostgreSQL functions exactly
// =============================================================================

// Level 1: Simple calculations on raw fields only
// ------------------------------------------------

// CalcCategoryContainsLanguage mirrors calc_language_candidates_category_contains_language()
// Formula: FIND("language", LOWER(category)) > 0
func (lc *LanguageCandidate) CalcCategoryContainsLanguage() bool {
	if lc.Category == nil {
		return false
	}
	return strings.Contains(strings.ToLower(*lc.Category), "language")
}

// CalcHasGrammar mirrors calc_language_candidates_has_grammar()
// Formula: CAST(has_syntax AS TEXT)
func (lc *LanguageCandidate) CalcHasGrammar() string {
	if lc.HasSyntax == nil || !*lc.HasSyntax {
		return ""
	}
	return "true"
}

// CalcRelationshipToConcept mirrors calc_language_candidates_relationship_to_concept()
// Formula: IF(distance_from_concept = 1, "IsMirrorOf", "IsDescriptionOf")
func (lc *LanguageCandidate) CalcRelationshipToConcept() string {
	if lc.DistanceFromConcept != nil && *lc.DistanceFromConcept == 1 {
		return "IsMirrorOf"
	}
	return "IsDescriptionOf"
}

// CalcFamilyFuedQuestion mirrors calc_language_candidates_family_fued_question()
// Formula: "Is " & name & " a language?"
func (lc *LanguageCandidate) CalcFamilyFuedQuestion() string {
	name := ""
	if lc.Name != nil {
		name = *lc.Name
	}
	return fmt.Sprintf("Is %s a language?", name)
}

// Level 2: Depends on Level 1 calculations
// ----------------------------------------

// CalcIsAFamilyFeudTopAnswer mirrors calc_language_candidates_is_a_family_feud_top_answer()
// Formula: AND(
//
//	category_contains_language,
//	has_syntax,
//	NOT(can_be_held),
//	meaning_is_serialized,
//	requires_parsing,
//	is_ongology_descriptor,
//	NOT(has_identity),
//	distance_from_concept = 2
//
// )
func (lc *LanguageCandidate) CalcIsAFamilyFeudTopAnswer() bool {
	// Depends on Level 1 calc
	categoryContainsLanguage := lc.CalcCategoryContainsLanguage()

	// Helper to get bool with default false
	boolVal := func(b *bool) bool {
		if b == nil {
			return false
		}
		return *b
	}

	// All conditions must be true
	return categoryContainsLanguage &&
		boolVal(lc.HasSyntax) &&
		!boolVal(lc.CanBeHeld) &&
		boolVal(lc.MeaningIsSerialized) &&
		boolVal(lc.RequiresParsing) &&
		boolVal(lc.IsOngologyDescriptor) &&
		!boolVal(lc.HasIdentity) &&
		(lc.DistanceFromConcept != nil && *lc.DistanceFromConcept == 2)
}

// Level 3: Depends on Level 2 calculations
// ----------------------------------------

// CalcFamilyFeudMismatch mirrors calc_language_candidates_family_feud_mismatch()
// Formula: IF(is_a_family_feud_top_answer != chosen_language_candidate, ...)
func (lc *LanguageCandidate) CalcFamilyFeudMismatch() *string {
	// Depends on Level 2 calc
	isTopAnswer := lc.CalcIsAFamilyFeudTopAnswer()

	chosen := false
	if lc.ChosenLanguageCandidate != nil {
		chosen = *lc.ChosenLanguageCandidate
	}

	if isTopAnswer != chosen {
		isWord := "Isn't"
		if isTopAnswer {
			isWord = "Is"
		}
		markedWord := "Is Not"
		if chosen {
			markedWord = "Is"
		}

		name := ""
		if lc.Name != nil {
			name = *lc.Name
		}

		result := fmt.Sprintf("%s %s a Family Feud Language, but %s marked as a 'Language Candidate.'",
			name, isWord, markedWord)
		return &result
	}
	return nil
}

// =============================================================================
// VIEW - Computed view with all calculated fields
// =============================================================================

// LanguageCandidateView contains all raw + calculated fields (mirrors vw_language_candidates)
type LanguageCandidateView struct {
	// Primary Key
	LanguageCandidateID string `json:"language_candidate_id"`

	// Raw Fields
	Name                    *string `json:"name"`
	Category                *string `json:"category"`
	CanBeHeld               *bool   `json:"can_be_held"`
	MeaningIsSerialized     *bool   `json:"meaning_is_serialized"`
	RequiresParsing         *bool   `json:"requires_parsing"`
	IsOngologyDescriptor    *bool   `json:"is_ongology_descriptor"`
	HasSyntax               *bool   `json:"has_syntax"`
	ChosenLanguageCandidate *bool   `json:"chosen_language_candidate"`
	SortOrder               *int    `json:"sort_order"`
	HasIdentity             *bool   `json:"has_identity"`
	DistanceFromConcept     *int    `json:"distance_from_concept"`

	// Calculated Fields
	CategoryContainsLanguage  bool    `json:"category_contains_language"`
	HasGrammar                string  `json:"has_grammar"`
	RelationshipToConcept     string  `json:"relationship_to_concept"`
	FamilyFuedQuestion        string  `json:"family_fued_question"`
	IsAFamilyFeudTopAnswer    bool    `json:"is_a_family_feud_top_answer"`
	FamilyFeudMismatch        *string `json:"family_feud_mismatch"`
}

// ToView returns all raw + calculated fields (mirrors vw_language_candidates)
func (lc *LanguageCandidate) ToView() LanguageCandidateView {
	return LanguageCandidateView{
		// Primary Key
		LanguageCandidateID: lc.LanguageCandidateID,
		// Raw Fields
		Name:                    lc.Name,
		Category:                lc.Category,
		CanBeHeld:               lc.CanBeHeld,
		MeaningIsSerialized:     lc.MeaningIsSerialized,
		RequiresParsing:         lc.RequiresParsing,
		IsOngologyDescriptor:    lc.IsOngologyDescriptor,
		HasSyntax:               lc.HasSyntax,
		ChosenLanguageCandidate: lc.ChosenLanguageCandidate,
		SortOrder:               lc.SortOrder,
		HasIdentity:             lc.HasIdentity,
		DistanceFromConcept:     lc.DistanceFromConcept,
		// Calculated Fields (DAG order)
		CategoryContainsLanguage:  lc.CalcCategoryContainsLanguage(),
		HasGrammar:                lc.CalcHasGrammar(),
		RelationshipToConcept:     lc.CalcRelationshipToConcept(),
		FamilyFuedQuestion:        lc.CalcFamilyFuedQuestion(),
		IsAFamilyFeudTopAnswer:    lc.CalcIsAFamilyFeudTopAnswer(),
		FamilyFeudMismatch:        lc.CalcFamilyFeudMismatch(),
	}
}

// =============================================================================
// IsEverythingALanguage - Argument steps entity
// =============================================================================

// IsEverythingALanguage represents argument steps in the philosophical debate
type IsEverythingALanguage struct {
	IsEverythingALanguageID string  `json:"IsEverythingALanguageId"`
	Name                    *string `json:"Name"`
	ArgumentName            *string `json:"ArgumentName"`
	ArgumentCategory        *string `json:"ArgumentCategory"`
	StepType                *string `json:"StepType"`
	Statement               *string `json:"Statement"`
	Formalization           *string `json:"Formalization"`
	RelatedCandidateName    *string `json:"RelatedCandidateName"`
	RelatedCandidateID      *string `json:"RelatedCandidateId"`
	EvidenceFromRulebook    *string `json:"EvidenceFromRulebook"`
	Notes                   *string `json:"Notes"`
}

// =============================================================================
// CORE LANGUAGE DEFINITION (from the rulebook)
// =============================================================================

// IsLanguage checks if a candidate satisfies the core language definition
// Language(x) := HasSyntax(x) AND RequiresParsing(x) AND Meaning_Is_Serialized(x) AND IsOngologyDescriptor(x)
func IsLanguage(lc *LanguageCandidate) bool {
	boolVal := func(b *bool) bool {
		if b == nil {
			return false
		}
		return *b
	}
	return boolVal(lc.HasSyntax) &&
		boolVal(lc.RequiresParsing) &&
		boolVal(lc.MeaningIsSerialized) &&
		boolVal(lc.IsOngologyDescriptor)
}

// =============================================================================
// LOADER - Load from JSON rulebook
// =============================================================================

// Rulebook represents the JSON structure of the effortless rulebook
type Rulebook struct {
	LanguageCandidates struct {
		Data []LanguageCandidate `json:"data"`
	} `json:"LanguageCandidates"`
	IsEverythingALanguage struct {
		Data []IsEverythingALanguage `json:"data"`
	} `json:"IsEverythingALanguage"`
}

// LoadFromRulebook loads entities from the effortless-rulebook.json file
func LoadFromRulebook(path string) (*Rulebook, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("failed to read rulebook: %w", err)
	}

	var rulebook Rulebook
	if err := json.Unmarshal(data, &rulebook); err != nil {
		return nil, fmt.Errorf("failed to parse rulebook: %w", err)
	}

	return &rulebook, nil
}

// =============================================================================
// TEST DATA STRUCTURES - For reading/writing test JSON (snake_case format)
// =============================================================================

// TestCandidate represents a language candidate in the test JSON format (snake_case)
type TestCandidate struct {
	LanguageCandidateID     string  `json:"language_candidate_id"`
	Name                    *string `json:"name"`
	Category                *string `json:"category"`
	FamilyFuedQuestion      *string `json:"family_fued_question"`
	TopFamilyFeudAnswer     *bool   `json:"top_family_feud_answer"`
	ChosenLanguageCandidate *bool   `json:"chosen_language_candidate"`
	FamilyFeudMismatch      *string `json:"family_feud_mismatch"`
	HasSyntax               *bool   `json:"has_syntax"`
	HasIdentity             *bool   `json:"has_identity"`
	CanBeHeld               *bool   `json:"can_be_held"`
	HasGrammar              *bool   `json:"has_grammar"`
	RequiresParsing         *bool   `json:"requires_parsing"`
	MeaningIsSerialized     *bool   `json:"meaning_is_serialized"`
	IsOngologyDescriptor    *bool   `json:"is_ongology_descriptor"`
	DistanceFromConcept     *int    `json:"distance_from_concept"`
	RelationshipToConcept   *string `json:"relationship_to_concept"`
	SortOrder               *int    `json:"sort_order"`
}

// ToLanguageCandidate converts TestCandidate to LanguageCandidate for calculation
func (tc *TestCandidate) ToLanguageCandidate() *LanguageCandidate {
	return &LanguageCandidate{
		LanguageCandidateID:     tc.LanguageCandidateID,
		Name:                    tc.Name,
		Category:                tc.Category,
		CanBeHeld:               tc.CanBeHeld,
		MeaningIsSerialized:     tc.MeaningIsSerialized,
		RequiresParsing:         tc.RequiresParsing,
		IsOngologyDescriptor:    tc.IsOngologyDescriptor,
		HasSyntax:               tc.HasSyntax,
		ChosenLanguageCandidate: tc.ChosenLanguageCandidate,
		SortOrder:               tc.SortOrder,
		HasIdentity:             tc.HasIdentity,
		DistanceFromConcept:     tc.DistanceFromConcept,
	}
}

// ComputeAnswers computes all calculated fields and returns an updated TestCandidate
func (tc *TestCandidate) ComputeAnswers() *TestCandidate {
	lc := tc.ToLanguageCandidate()

	// Compute calculated fields
	familyFuedQuestion := lc.CalcFamilyFuedQuestion()
	topAnswer := lc.CalcIsAFamilyFeudTopAnswer()
	hasGrammar := lc.HasSyntax != nil && *lc.HasSyntax
	relationshipToConcept := lc.CalcRelationshipToConcept()
	familyFeudMismatch := lc.CalcFamilyFeudMismatch()

	return &TestCandidate{
		LanguageCandidateID:     tc.LanguageCandidateID,
		Name:                    tc.Name,
		Category:                tc.Category,
		FamilyFuedQuestion:      &familyFuedQuestion,
		TopFamilyFeudAnswer:     &topAnswer,
		ChosenLanguageCandidate: tc.ChosenLanguageCandidate,
		FamilyFeudMismatch:      familyFeudMismatch,
		HasSyntax:               tc.HasSyntax,
		HasIdentity:             tc.HasIdentity,
		CanBeHeld:               tc.CanBeHeld,
		HasGrammar:              &hasGrammar,
		RequiresParsing:         tc.RequiresParsing,
		MeaningIsSerialized:     tc.MeaningIsSerialized,
		IsOngologyDescriptor:    tc.IsOngologyDescriptor,
		DistanceFromConcept:     tc.DistanceFromConcept,
		RelationshipToConcept:   &relationshipToConcept,
		SortOrder:               tc.SortOrder,
	}
}

// LoadTestCandidates loads candidates from a test JSON file (blank-test.json format)
func LoadTestCandidates(path string) ([]TestCandidate, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("failed to read test file: %w", err)
	}

	var candidates []TestCandidate
	if err := json.Unmarshal(data, &candidates); err != nil {
		return nil, fmt.Errorf("failed to parse test file: %w", err)
	}

	return candidates, nil
}

// SaveTestCandidates saves computed candidates to a test JSON file
func SaveTestCandidates(path string, candidates []TestCandidate) error {
	data, err := json.MarshalIndent(candidates, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal test answers: %w", err)
	}

	if err := os.WriteFile(path, data, 0644); err != nil {
		return fmt.Errorf("failed to write test answers: %w", err)
	}

	return nil
}
