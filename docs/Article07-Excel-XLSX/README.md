# Article 7: Excel/XLSX — The Universal Interface

Business users live in spreadsheets. This article shows how ERB generates fully-functional Excel workbooks where formulas are preserved—not just values. Users can email these spreadsheets, modify data, and see computed fields update in real-time. We examine the xlsxwriter generation code, the formula translation layer, and why this "low-tech" output might be the most valuable substrate for organizational adoption.

---

## Detailed Table of Contents

### 1. Why Excel Matters Most
- **The Universal Language**: Everyone knows Excel
- **No Installation Required**: Works on any computer
- **Live Formulas**: Not static values—real computation
- **Organizational Adoption**: The path of least resistance
- **Download**: [rulebook.xlsx](../../execution-substratrates/xlsx/rulebook.xlsx)

### 2. What Gets Generated

```
execution-substratrates/xlsx/
├── rulebook.xlsx          # The Excel workbook (with live formulas)
├── inject-into-xlsx.py    # Injector script
├── take-test.py           # Test runner (reads computed values)
├── take-test.sh           # Shell wrapper
├── test-answers.json      # Output for grading
└── README.md
```

### 3. The Workbook Structure

#### Sheet: `LanguageCandidates`
| Column | Type | Source |
|--------|------|--------|
| A: `language_candidate_id` | Raw | Direct from rulebook |
| B: `name` | Raw | Direct from rulebook |
| C: `category` | Raw | Direct from rulebook |
| D: `has_syntax` | Raw (boolean) | TRUE/FALSE |
| ... | ... | ... |
| T: `family_fued_question` | **Formula** | `="Is " & B2 & " a language?"` |
| U: `top_family_feud_answer` | **Formula** | `=AND(D2, E2, V2, ...)` |
| V: `is_description_of` | **Formula** | `=P2 > 1` |
| W: `family_feud_mismatch` | **Formula** | `=IF(...)` |

### 4. Formula Translation — Airtable to Excel

| Airtable | Excel |
|----------|-------|
| `{{FieldName}}` | Cell reference (e.g., `B2`) |
| `AND(...)` | `=AND(...)` |
| `OR(...)` | `=OR(...)` |
| `IF(cond, then, else)` | `=IF(cond, then, else)` |
| `NOT(...)` | `=NOT(...)` |
| `"text" & {{Name}}` | `="text" & B2` |

### 5. The Core Formulas in Excel Syntax

#### 5.1 `family_fued_question` (Level 1)
```excel
="Is " & B2 & " a language?"
```

#### 5.2 `is_description_of` (Level 1)
```excel
=P2 > 1
```
Where P2 = `distance_from_concept`

#### 5.3 `is_open_closed_world_conflicted` (Level 1)
```excel
=AND(Q2, R2)
```
Where Q2 = `is_open_world`, R2 = `is_closed_world`

#### 5.4 `top_family_feud_answer` (Level 2)
```excel
=AND(D2, E2, V2, F2, G2, H2, NOT(I2), NOT(J2))
```
Where:
- D2 = `has_syntax`
- E2 = `requires_parsing`
- V2 = `is_description_of` (Level 1 formula result)
- F2 = `has_linear_decoding_pressure`
- G2 = `resolves_to_an_ast`
- H2 = `is_stable_ontology_reference`
- I2 = `can_be_held`
- J2 = `has_identity`

#### 5.5 `family_feud_mismatch` (Level 3)
```excel
=IF(NOT(U2 = K2),
    B2 & " " & IF(U2, "Is", "Isn't") & " a Family Feud Language, but " &
    IF(K2, "Is", "Is Not") & " marked as a 'Language Candidate.'", "") &
  IF(X2, " - Open World vs. Closed World Conflict.", "")
```

### 6. The Injection Process

```python
def inject_into_xlsx():
    # 1. Load rulebook
    rulebook = load_rulebook()

    # 2. Create workbook
    workbook = xlsxwriter.Workbook('rulebook.xlsx')

    # 3. For each table:
    worksheet = workbook.add_worksheet('LanguageCandidates')

    # 4. Write headers (column A-Z)
    for col, field in enumerate(schema):
        worksheet.write(0, col, field.name)

    # 5. For each row:
    for row, record in enumerate(data, start=1):
        for col, field in enumerate(schema):
            if field.type == 'calculated':
                # Write formula, not value!
                formula = translate_to_excel(field.formula, row)
                worksheet.write_formula(row, col, formula)
            else:
                # Write raw value
                worksheet.write(row, col, record[field.name])

    workbook.close()
```

### 7. Column Mapping Strategy

The injector builds a mapping of field names to column letters:
```python
column_map = {
    'language_candidate_id': 'A',
    'name': 'B',
    'category': 'C',
    'has_syntax': 'D',
    # ...
    'is_description_of': 'V',
    'top_family_feud_answer': 'U',
}
```

Formula translation replaces `{{FieldName}}` with `{column}{row}`:
```python
def translate_field_ref(formula, row):
    # "{{HasSyntax}}" → "D{row}" → "D2"
    return formula.replace('{{HasSyntax}}', f'D{row}')
```

### 8. Why Live Formulas Matter

| Static Export | Live Formulas |
|--------------|---------------|
| Values copied at export time | Formulas recalculate in real-time |
| Change data → values stale | Change data → see new results |
| Can't debug classification | Can inspect each formula |
| Single point-in-time snapshot | Living, editable model |

### 9. User Workflow

1. **Download** `rulebook.xlsx`
2. **Open** in Excel (or Google Sheets, LibreOffice)
3. **Edit** a raw field (e.g., change `has_syntax` from TRUE to FALSE)
4. **Watch** `top_family_feud_answer` recalculate automatically
5. **Experiment** with "what if" scenarios
6. **Share** via email—recipient sees same calculations

### 10. Test Runner — Reading Computed Values

```python
def take_test():
    # 1. Open workbook
    wb = openpyxl.load_workbook('rulebook.xlsx', data_only=True)
    ws = wb['LanguageCandidates']

    # 2. Read computed values (not formulas)
    results = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        record = {
            'language_candidate_id': row[0],
            'top_family_feud_answer': row[20],  # Column U
            # ...
        }
        results.append(record)

    # 3. Write test-answers.json
    with open('test-answers.json', 'w') as f:
        json.dump(results, f)
```

**Note**: `data_only=True` tells openpyxl to read computed values, not formula strings.

### 11. Test Results

- **Pass Rate**: 100% (0 failures)
- **Execution Time**: 336ms
- **Why Slower?**: Opening/parsing XLSX is more expensive than pure Python

### 12. Edge Cases and Limitations

| Challenge | Solution |
|-----------|----------|
| Boolean display | Excel shows TRUE/FALSE (not 1/0) |
| Empty cells | COALESCE pattern with IF(ISBLANK()) |
| String concatenation | Works natively with `&` |
| NULL handling | Empty string "" for missing values |

### 13. The Business Value Proposition

- **No Training Required**: Everyone knows Excel
- **Audit Trail**: Formulas are visible and inspectable
- **What-If Analysis**: Change inputs, see outputs
- **Offline Capable**: No internet connection needed
- **Printable**: Generate reports directly

### 14. Google Sheets Compatibility

The generated XLSX imports into Google Sheets with formulas intact:
1. Upload `rulebook.xlsx` to Google Drive
2. Open with Google Sheets
3. Formulas translate automatically
4. Share with collaborators

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [rulebook.xlsx](../../execution-substratrates/xlsx/rulebook.xlsx) | Generated Excel workbook |
| [inject-into-xlsx.py](../../execution-substratrates/xlsx/inject-into-xlsx.py) | Code generator |
| [take-test.py](../../execution-substratrates/xlsx/take-test.py) | Test runner |

---

*Article content to be written...*
