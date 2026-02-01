// ERB SDK - Go Demo and Test Runner
package main

import (
	"fmt"
	"os"
	"path/filepath"
	"sort"
)

func main() {
	// Check if running as test runner
	if len(os.Args) > 1 && os.Args[1] == "take-test" {
		runTest()
		return
	}

	// Demo mode: load from rulebook
	runDemo()
}

func runDemo() {
	// Load from rulebook
	rulebookPath := filepath.Join("..", "..", "effortless-rulebook", "effortless-rulebook.json")

	rulebook, err := LoadFromRulebook(rulebookPath)
	if err != nil {
		fmt.Printf("Failed to load rulebook: %v\n", err)
		return
	}

	fmt.Printf("Loaded %d language candidates\n", len(rulebook.LanguageCandidates.Data))
	fmt.Printf("Loaded %d argument steps\n", len(rulebook.IsEverythingALanguage.Data))
	fmt.Println()

	// Sort by sort_order
	candidates := rulebook.LanguageCandidates.Data
	sort.Slice(candidates, func(i, j int) bool {
		iOrder := 999
		jOrder := 999
		if candidates[i].SortOrder != nil {
			iOrder = *candidates[i].SortOrder
		}
		if candidates[j].SortOrder != nil {
			jOrder = *candidates[j].SortOrder
		}
		return iOrder < jOrder
	})

	// Show first candidate with all calculated fields
	if len(candidates) > 0 {
		c := candidates[0]
		name := ""
		if c.Name != nil {
			name = *c.Name
		}
		fmt.Printf("First candidate: %s\n", name)

		view := c.ToView()
		fmt.Printf("  language_candidate_id: %s\n", view.LanguageCandidateID)
		if view.Name != nil {
			fmt.Printf("  name: %s\n", *view.Name)
		}
		if view.Category != nil {
			fmt.Printf("  category: %s\n", *view.Category)
		}
		fmt.Printf("  category_contains_language: %v\n", view.CategoryContainsLanguage)
		fmt.Printf("  has_grammar: %s\n", view.HasGrammar)
		fmt.Printf("  relationship_to_concept: %s\n", view.RelationshipToConcept)
		fmt.Printf("  family_fued_question: %s\n", view.FamilyFuedQuestion)
		fmt.Printf("  is_a_family_feud_top_answer: %v\n", view.IsAFamilyFeudTopAnswer)
		if view.FamilyFeudMismatch != nil {
			fmt.Printf("  family_feud_mismatch: %s\n", *view.FamilyFeudMismatch)
		} else {
			fmt.Printf("  family_feud_mismatch: null\n")
		}
	}
}

func runTest() {
	scriptDir, err := os.Getwd()
	if err != nil {
		fmt.Printf("Failed to get working directory: %v\n", err)
		os.Exit(1)
	}

	// Paths
	blankTestPath := filepath.Join(scriptDir, "..", "..", "testing", "blank-test.json")
	answersPath := filepath.Join(scriptDir, "test-answers.json")

	// Step 1: Load blank test data
	candidates, err := LoadTestCandidates(blankTestPath)
	if err != nil {
		fmt.Printf("Failed to load blank test: %v\n", err)
		os.Exit(1)
	}

	// Step 2: Compute all calculated fields
	var computed []TestCandidate
	for _, c := range candidates {
		computed = append(computed, *c.ComputeAnswers())
	}

	// Step 3: Save test answers
	if err := SaveTestCandidates(answersPath, computed); err != nil {
		fmt.Printf("Failed to save test answers: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("golang: Computed %d test answers -> test-answers.json\n", len(computed))
}
