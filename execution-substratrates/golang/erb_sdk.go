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

// =============================================================================
// CUSTOMERS TABLE
// =============================================================================

// Customer represents a row in the Customers table
type Customer struct {
	CustomerId string `json:"customer_id"`
	Customer *string `json:"customer"`
	EmailAddress *string `json:"email_address"`
	FirstName *string `json:"first_name"`
	LastName *string `json:"last_name"`
	FullName *string `json:"full_name"`
}

// --- Individual Calculation Functions ---

// CalcFullName computes the FullName calculated field
// Formula: ={{FirstName}} & " " & {{LastName}}
func (tc *Customer) CalcFullName() string {
	return stringVal(tc.FirstName) + " " + stringVal(tc.LastName)
}

// --- Compute All Calculated Fields ---

// ComputeAll computes all calculated fields and returns an updated struct
func (tc *Customer) ComputeAll() *Customer {
	// Level 1 calculations
	fullName := stringVal(tc.FirstName) + " " + stringVal(tc.LastName)

	return &Customer{
		CustomerId: tc.CustomerId,
		Customer: tc.Customer,
		EmailAddress: tc.EmailAddress,
		FirstName: tc.FirstName,
		LastName: tc.LastName,
		FullName: nilIfEmpty(fullName),
	}
}

// =============================================================================
// ORDERS TABLE
// =============================================================================

// Order represents a row in the Orders table
type Order struct {
	OrderId string `json:"order_id"`
	OrderNumber *int `json:"order_number"`
	Name *string `json:"name"`
}

// --- Individual Calculation Functions ---

// CalcName computes the Name calculated field
// Formula: ="ORD" & {{OrderNumber}}
func (tc *Order) CalcName() string {
	return "ORD" + stringVal(tc.OrderNumber)
}

// --- Compute All Calculated Fields ---

// ComputeAll computes all calculated fields and returns an updated struct
func (tc *Order) ComputeAll() *Order {
	// Level 1 calculations
	name := "ORD" + stringVal(tc.OrderNumber)

	return &Order{
		OrderId: tc.OrderId,
		OrderNumber: tc.OrderNumber,
		Name: nilIfEmpty(name),
	}
}

// =============================================================================
// FILE I/O (for Customers)
// =============================================================================

// LoadRecords loads records from a JSON file
func LoadRecords(path string) ([]Customer, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("failed to read file: %w", err)
	}

	var records []Customer
	if err := json.Unmarshal(data, &records); err != nil {
		return nil, fmt.Errorf("failed to parse file: %w", err)
	}

	return records, nil
}

// SaveRecords saves computed records to a JSON file
func SaveRecords(path string, records []Customer) error {
	data, err := json.MarshalIndent(records, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal records: %w", err)
	}

	if err := os.WriteFile(path, data, 0644); err != nil {
		return fmt.Errorf("failed to write records: %w", err)
	}

	return nil
}