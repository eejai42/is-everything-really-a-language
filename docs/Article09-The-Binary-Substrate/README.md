# Article 9: The Binary Substrate — From Spreadsheet to Machine Code

The most audacious claim of ERB: the same business rules that live in an Airtable spreadsheet can be compiled to native machine code. This article dissects the ARM64/x86-64 assembly generation, explains the minimal ABI with tagged unions, and shows how the generated `.dylib` is loaded via ctypes. We examine the assembly output line-by-line, proving that declarative formulas can become raw CPU instructions without losing semantic fidelity.

---

## Detailed Table of Contents

### 1. The Audacious Claim
- **From Spreadsheet to Assembler**: The same formula in Airtable becomes x86-64 instructions
- **Why This Matters**: Proves the abstraction is truly language-independent
- **Current State**: 69.6% pass rate (38 failures due to string handling)
- **The Lesson**: String concatenation in assembly is hard

### 2. The Generated Artifacts

```
execution-substrates/binary/
├── erb_calc.s             # Assembly source (12.8KB)
├── erb_calc.o             # Object file (4.1KB)
├── erb_calc.dylib         # Dynamic library (35.5KB)
├── inject-into-binary.py  # Code generator
├── take-test.py           # Test runner (uses ctypes)
├── test-answers.json      # Output for grading
└── README.md
```

### 3. The ABI (Application Binary Interface)

#### 3.1 Data Structure Layout
```c
// Conceptual C representation of the generated struct
typedef struct {
    char* language_candidate_id;  // offset 0
    char* name;                   // offset 8
    char* category;               // offset 16
    uint8_t has_syntax;           // offset 24 (boolean as byte)
    uint8_t has_identity;         // offset 25
    uint8_t can_be_held;          // offset 26
    uint8_t requires_parsing;     // offset 27
    // ... more fields
    int32_t distance_from_concept; // offset 40
    // ...
} LanguageCandidate;
```

#### 3.2 Boolean Representation
- `0x00` = false
- `0x01` = true
- `0xFF` = NULL/unknown

#### 3.3 String Representation
- Pointer to null-terminated C string
- NULL pointer = missing value

### 4. The Assembly Structure — `erb_calc.s`

#### 4.1 File Sections
```asm
    .section __TEXT,__text,regular,pure_instructions
    .globl _calc_has_grammar
    .globl _calc_is_description_of
    .globl _calc_top_family_feud_answer
    .globl _calc_family_feud_mismatch

    .section __DATA,__data
    ; Static string literals
_str_is: .asciz "Is"
_str_isnt: .asciz "Isn't"
_str_language: .asciz " a language?"
```

#### 4.2 Function Prologue Pattern
```asm
_calc_top_family_feud_answer:
    push rbp                    ; Save frame pointer
    mov rbp, rsp                ; Set up stack frame
    sub rsp, 32                 ; Reserve local variables
    mov [rbp-8], rdi            ; Save struct pointer
```

### 5. Boolean Formula → Assembly

#### 5.1 Field Offsets
```asm
; Generated offset constants
.equ OFFSET_HAS_SYNTAX, 24
.equ OFFSET_HAS_IDENTITY, 25
.equ OFFSET_CAN_BE_HELD, 26
.equ OFFSET_REQUIRES_PARSING, 27
.equ OFFSET_DISTANCE_FROM_CONCEPT, 40
```

#### 5.2 `calc_is_description_of` — Simple Comparison
```asm
_calc_is_description_of:
    push rbp
    mov rbp, rsp
    mov rdi, [rbp+16]               ; Load struct pointer

    ; distance_from_concept > 1
    mov eax, [rdi + OFFSET_DISTANCE_FROM_CONCEPT]
    cmp eax, 1
    setg al                         ; Set AL to 1 if greater
    movzx eax, al                   ; Zero-extend to 32 bits

    pop rbp
    ret
```

#### 5.3 `calc_top_family_feud_answer` — AND Chain
```asm
_calc_top_family_feud_answer:
    push rbp
    mov rbp, rsp
    mov rdi, [rbp+16]               ; Struct pointer

    ; Check has_syntax
    movzbl [rdi + OFFSET_HAS_SYNTAX], eax
    test al, al
    jz .return_false

    ; Check requires_parsing
    movzbl [rdi + OFFSET_REQUIRES_PARSING], eax
    test al, al
    jz .return_false

    ; Check is_description_of (calls Level 1 function)
    push rdi
    call _calc_is_description_of
    pop rdi
    test al, al
    jz .return_false

    ; Check has_linear_decoding_pressure
    movzbl [rdi + OFFSET_HAS_LINEAR_DECODING_PRESSURE], eax
    test al, al
    jz .return_false

    ; Check resolves_to_an_ast
    movzbl [rdi + OFFSET_RESOLVES_TO_AN_AST], eax
    test al, al
    jz .return_false

    ; Check is_stable_ontology_reference
    movzbl [rdi + OFFSET_IS_STABLE_ONTOLOGY_REFERENCE], eax
    test al, al
    jz .return_false

    ; Check NOT(can_be_held)
    movzbl [rdi + OFFSET_CAN_BE_HELD], eax
    test al, al
    jnz .return_false               ; Jump if TRUE (we want FALSE)

    ; Check NOT(has_identity)
    movzbl [rdi + OFFSET_HAS_IDENTITY], eax
    test al, al
    jnz .return_false               ; Jump if TRUE (we want FALSE)

    ; All conditions passed
    mov eax, 1
    jmp .return

.return_false:
    xor eax, eax                    ; Return 0 (false)

.return:
    pop rbp
    ret
```

### 6. String Concatenation — The Hard Part

#### 6.1 The Challenge
`FamilyFeudMismatch` requires dynamic string building:
```
"Falsifier A Is a Family Feud Language, but Is Not marked as a 'Language Candidate.'"
```

#### 6.2 Runtime Functions
```asm
; String concatenation helper
_string_concat:
    ; Input: rdi = dest buffer, rsi = string 1, rdx = string 2
    ; Output: concatenated string at rdi
    push rbp
    mov rbp, rsp
    ; ... strlen, memcpy, null termination
    pop rbp
    ret

; String equality comparison
_string_equals:
    ; Input: rdi = string 1, rsi = string 2
    ; Output: eax = 1 if equal, 0 otherwise
    push rbp
    mov rbp, rsp
    ; ... byte-by-byte comparison
    pop rbp
    ret
```

#### 6.3 The Current Limitation
The binary substrate achieves 69.6% pass rate because:
- Boolean formulas work perfectly
- String concatenation has edge cases with NULL handling
- Buffer management for dynamic strings is complex

### 7. Building the Dynamic Library

#### 7.1 Assembly → Object File
```bash
as -arch x86_64 erb_calc.s -o erb_calc.o
```

#### 7.2 Object → Shared Library
```bash
ld -dylib -arch x86_64 -o erb_calc.dylib erb_calc.o -lSystem
```

### 8. Loading via Python ctypes

```python
import ctypes

# Load the dynamic library
lib = ctypes.CDLL('./erb_calc.dylib')

# Define the struct
class LanguageCandidate(ctypes.Structure):
    _fields_ = [
        ('language_candidate_id', ctypes.c_char_p),
        ('name', ctypes.c_char_p),
        ('category', ctypes.c_char_p),
        ('has_syntax', ctypes.c_uint8),
        ('has_identity', ctypes.c_uint8),
        ('can_be_held', ctypes.c_uint8),
        # ...
    ]

# Set function signatures
lib.calc_top_family_feud_answer.argtypes = [ctypes.POINTER(LanguageCandidate)]
lib.calc_top_family_feud_answer.restype = ctypes.c_uint8

# Call the function
candidate = LanguageCandidate(
    language_candidate_id=b'english',
    name=b'English',
    has_syntax=1,
    requires_parsing=1,
    # ...
)
result = lib.calc_top_family_feud_answer(ctypes.byref(candidate))
print(f"Is English a language? {bool(result)}")  # True
```

### 9. ARM64 vs x86-64

The generator detects architecture and produces appropriate assembly:

| Architecture | Platform | Registers | Calling Convention |
|--------------|----------|-----------|-------------------|
| x86-64 | macOS Intel, Linux | rdi, rsi, rdx, rcx | System V AMD64 ABI |
| ARM64 | macOS M1/M2 | x0-x7 | AAPCS64 |

### 10. Test Results

- **Pass Rate**: 69.6% (38 failures out of 125)
- **Passing Tests**: All boolean-only formulas
- **Failing Tests**: Formulas with complex string concatenation
- **Execution Time**: 434ms

### 11. What Works vs. What's Hard

| Formula Type | Status | Notes |
|--------------|--------|-------|
| Boolean AND/OR/NOT | Working | `calc_top_family_feud_answer` |
| Integer comparison | Working | `calc_is_description_of` |
| Simple string concat | Partial | `calc_family_fued_question` |
| Complex IF + concat | Failing | `calc_family_feud_mismatch` |

### 12. Why This Matters

Even at 69.6%, this substrate proves:
- **Formulas are truly abstract**: Same logic, wildly different representation
- **The compilation chain works**: Airtable → JSON → AST → Assembly
- **No magic required**: Just careful code generation

### 13. Future Improvements

- Better NULL/empty string handling in assembly
- Use LLVM IR as intermediate representation
- Link against libc for string functions
- Consider WebAssembly as an alternative binary target

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [erb_calc.s](../../execution-substrates/binary/erb_calc.s) | Generated assembly source |
| [erb_calc.dylib](../../execution-substrates/binary/erb_calc.dylib) | Compiled dynamic library |
| [inject-into-binary.py](../../execution-substrates/binary/inject-into-binary.py) | Code generator |
| [take-test.py](../../execution-substrates/binary/take-test.py) | Test runner |

---

*Article content to be written...*
