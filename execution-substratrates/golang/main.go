// ERB SDK - Go Test Runner (GENERATED - DO NOT EDIT)
package main

import (
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	scriptDir, err := os.Getwd()
	if err != nil {
		fmt.Printf("Failed to get working directory: %v\n", err)
		os.Exit(1)
	}

	// Shared blank-tests directory at project root
	blankTestsDir := filepath.Join(scriptDir, "..", "..", "testing", "blank-tests")
	testAnswersDir := filepath.Join(scriptDir, "test-answers")

	// Ensure output directory exists
	os.MkdirAll(testAnswersDir, 0755)

	fmt.Println("Golang substrate: Processing entities from shared testing/blank-tests/...")

	// Process customers.json
	customersInputPath := filepath.Join(blankTestsDir, "customers.json")
	customersOutputPath := filepath.Join(testAnswersDir, "customers.json")

	customerRecords, err := LoadRecords(customersInputPath)
	if err != nil {
		fmt.Printf("Failed to load customers: %v\n", err)
	} else {
		var computedCustomers []Customer
		for _, r := range customerRecords {
			computedCustomers = append(computedCustomers, *r.ComputeAll())
		}
		if err := SaveRecords(customersOutputPath, computedCustomers); err != nil {
			fmt.Printf("Failed to save customers: %v\n", err)
		} else {
			fmt.Printf("  -> customers: %d records\n", len(computedCustomers))
		}
	}

	fmt.Println("Golang substrate: Test completed")
}
