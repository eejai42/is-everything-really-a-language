# Specification Document for DEMO: Customer FullName Rulebook

## Overview
This rulebook defines the structure and computation methods for customer data within the "DEMO: Customer FullName" dataset. It includes details on how to derive the full name of a customer and determine their VIP status based on total sales. The rulebook is structured to facilitate easy understanding and implementation of the calculations required.

## Customers Entity

### Input Fields
The following input fields are required to compute the calculated fields:

1. **FirstName**
   - **Type:** String (raw)
   - **Description:** The first name of the customer, used to construct the full name.

2. **LastName**
   - **Type:** String (raw)
   - **Description:** The last name of the customer, used to construct the full name.

3. **TotalSales**
   - **Type:** Number (raw)
   - **Description:** The total sales amount associated with the customer, used to determine VIP status.

### Calculated Fields

#### 1. FullName
- **Description:** The full name of the customer is computed by combining the last name and first name.
- **Computation Method:** 
  - To compute the `FullName`, concatenate the `LastName` and `FirstName` fields with a comma and a space in between. 
  - The formula for this computation is:
    ```
    FullName = LastName + ", " + FirstName
    ```
- **Example:**
  - For a customer with:
    - `FirstName`: "Jane"
    - `LastName`: "Smith"
  - The computed `FullName` would be:
    ```
    FullName = "Smith, Jane"
    ```

#### 2. IsVIP
- **Description:** This field indicates whether the customer is considered a VIP based on their total sales.
- **Computation Method:** 
  - To determine if a customer is a VIP, check if the `TotalSales` amount exceeds 500. 
  - The formula for this computation is:
    ```
    IsVIP = TotalSales > 500
    ```
- **Example:**
  - For a customer with:
    - `TotalSales`: 811
  - The computed `IsVIP` value would be:
    ```
    IsVIP = 811 > 500 → true
    ```
  - Conversely, for a customer with:
    - `TotalSales`: 125
  - The computed `IsVIP` value would be:
    ```
    IsVIP = 125 > 500 → false
    ```

### Summary of Examples
- **Customer 1:**
  - `FirstName`: "Jane"
  - `LastName`: "Smith"
  - **Computed FullName:** "Smith, Jane"
  - `TotalSales`: 500
  - **Computed IsVIP:** false

- **Customer 2:**
  - `FirstName`: "John"
  - `LastName`: "Doe"
  - **Computed FullName:** "Doe, John"
  - `TotalSales`: 125
  - **Computed IsVIP:** false

- **Customer 3:**
  - `FirstName`: "Emily"
  - `LastName`: "Jones"
  - **Computed FullName:** "Jones, Emily"
  - `TotalSales`: 811
  - **Computed IsVIP:** true

This specification provides a clear understanding of how to compute the `FullName` and `IsVIP` fields based on the defined input fields. By following the outlined methods and examples, one can accurately derive the necessary values from the customer data.