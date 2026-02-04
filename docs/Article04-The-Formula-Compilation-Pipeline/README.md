# Article 4: The Formula Compilation Pipeline — One Formula, Twelve Targets

The magic of ERB lies in its formula parser. An Excel-dialect formula like `=IF(AND(HasNativeSpeakers,HasWritingSystem),"Yes","No")` gets parsed into an Abstract Syntax Tree, then compiled to Python, JavaScript, Go, SQL, SPARQL, OCL, and x86-64 assembly. This article dissects the `formula_parser.py`, shows how each target compiler works, and demonstrates that the same business logic executes identically across radically different runtime environments.

---

## Detailed Table of Contents

### 1. The Core Challenge
- **The Problem**: One formula, twelve radically different syntaxes
- **The Insight**: Formulas are language-agnostic; only the syntax varies
- **The Solution**: Parse once, compile many times
- **The Proof**: Same formula → Same results across Python, Go, SQL, Assembly

### 2. The Formula Language — Excel Dialect
ERB uses Excel-style formulas as the source notation:

#### 2.1 Supported Constructs
| Construct | Syntax | Example |
|-----------|--------|---------|
| Field Reference | `{{FieldName}}` | `{{HasSyntax}}` |
| String Literal | `"text"` | `"Is a language"` |
| Integer Literal | `123` | `2` |
| Boolean Literal | `TRUE()` / `FALSE()` | `TRUE()` |
| Concatenation | `&` | `"Is " & {{Name}} & " a language?"` |
| Equality | `=` | `{{DistanceFromConcept}} = 1` |
| Comparison | `>`, `<`, `>=`, `<=`, `<>` | `{{Distance}} > 1` |

#### 2.2 Supported Functions
| Function | Signature | Description |
|----------|-----------|-------------|
| `AND` | `AND(a, b, ...)` | All arguments must be true |
| `OR` | `OR(a, b, ...)` | At least one argument true |
| `NOT` | `NOT(a)` | Boolean negation |
| `IF` | `IF(cond, then, else)` | Conditional expression |
| `LOWER` | `LOWER(s)` | Lowercase string |
| `FIND` | `FIND(needle, haystack)` | Substring search |

### 3. The AST (Abstract Syntax Tree) — `formula_parser.py`

The 26KB `formula_parser.py` defines the intermediate representation:

#### 3.1 AST Node Types
```python
@dataclass
class LiteralBool(ASTNode):
    value: bool

@dataclass
class LiteralInt(ASTNode):
    value: int

@dataclass
class LiteralString(ASTNode):
    value: str

@dataclass
class FieldRef(ASTNode):
    name: str  # Field name without {{ }}

@dataclass
class BinaryOp(ASTNode):
    op: str  # '=', '<>', '<', '<=', '>', '>='
    left: ASTNode
    right: ASTNode

@dataclass
class UnaryOp(ASTNode):
    op: str  # 'NOT'
    operand: ASTNode

@dataclass
class FuncCall(ASTNode):
    name: str  # 'AND', 'OR', 'IF', 'LOWER', 'FIND'
    args: List[ASTNode]

@dataclass
class Concat(ASTNode):
    parts: List[ASTNode]
```

#### 3.2 Example: `TopFamilyFeudAnswer` Formula → AST
Input:
```
=AND(
  {{HasSyntax}},
  {{RequiresParsing}},
  {{IsDescriptionOf}},
  NOT({{CanBeHeld}}),
  NOT({{HasIdentity}})
)
```

AST:
```python
FuncCall(
    name='AND',
    args=[
        FieldRef(name='HasSyntax'),
        FieldRef(name='RequiresParsing'),
        FieldRef(name='IsDescriptionOf'),
        UnaryOp(op='NOT', operand=FieldRef(name='CanBeHeld')),
        UnaryOp(op='NOT', operand=FieldRef(name='HasIdentity'))
    ]
)
```

### 4. The Lexer — Tokenization

The first stage converts formula text to tokens:

```python
class TokenType(Enum):
    STRING = auto()       # "text"
    NUMBER = auto()       # 123
    FIELD_REF = auto()    # {{Name}}
    FUNC_NAME = auto()    # AND, OR, IF
    LPAREN = auto()       # (
    RPAREN = auto()       # )
    COMMA = auto()        # ,
    AMPERSAND = auto()    # &
    EQUALS = auto()       # =
    NOT_EQUALS = auto()   # <>
    LT = auto()           # <
    LE = auto()           # <=
    GT = auto()           # >
    GE = auto()           # >=
    EOF = auto()
```

#### 4.1 Tokenization Example
Input: `={{HasSyntax}} = TRUE()`

Tokens:
```
[FIELD_REF:'HasSyntax', EQUALS:'=', FUNC_NAME:'TRUE', LPAREN, RPAREN, EOF]
```

### 5. The Parser — Recursive Descent

The parser builds the AST using recursive descent:

```python
def parse_formula(formula: str) -> ASTNode:
    tokens = tokenize(formula)
    parser = Parser(tokens)
    return parser.parse_expression()
```

#### 5.1 Precedence Levels
1. **Concatenation** (`&`) — lowest
2. **Comparison** (`=`, `<>`, `<`, `>`, etc.)
3. **Unary** (`NOT`)
4. **Function calls** (`AND`, `OR`, `IF`)
5. **Literals and field refs** — highest

### 6. Target Compilers — One AST, Many Outputs

Each target language has a compiler that walks the AST:

#### 6.1 Python Compiler
```python
def compile_to_python(ast: ASTNode) -> str:
    if isinstance(ast, FieldRef):
        return f"self.{to_snake_case(ast.name)}"
    if isinstance(ast, LiteralBool):
        return "True" if ast.value else "False"
    if isinstance(ast, FuncCall):
        if ast.name == 'AND':
            return " and ".join(compile_to_python(a) for a in ast.args)
        # ...
```

**Output for TopFamilyFeudAnswer**:
```python
(self.has_syntax is True) and (self.requires_parsing is True) and \
(self.is_description_of is True) and not (self.can_be_held is True) and \
not (self.has_identity is True)
```

#### 6.2 Go Compiler
```python
def compile_to_go(ast: ASTNode) -> str:
    if isinstance(ast, FieldRef):
        return f"c.{toPascalCase(ast.name)}"
    if isinstance(ast, LiteralBool):
        return "true" if ast.value else "false"
    if isinstance(ast, FuncCall):
        if ast.name == 'AND':
            return " && ".join(compile_to_go(a) for a in ast.args)
        # ...
```

**Output**:
```go
c.HasSyntax && c.RequiresParsing && c.IsDescriptionOf &&
!c.CanBeHeld && !c.HasIdentity
```

#### 6.3 SQL Compiler
```python
def compile_to_sql(ast: ASTNode, table_alias: str) -> str:
    if isinstance(ast, FieldRef):
        return f"COALESCE({table_alias}.{to_snake_case(ast.name)}, FALSE)"
    if isinstance(ast, FuncCall):
        if ast.name == 'AND':
            return " AND ".join(f"({compile_to_sql(a, table_alias)})" for a in ast.args)
        # ...
```

**Output**:
```sql
COALESCE(lc.has_syntax, FALSE)
AND COALESCE(lc.requires_parsing, FALSE)
AND COALESCE(lc.is_description_of, FALSE)
AND NOT COALESCE(lc.can_be_held, FALSE)
AND NOT COALESCE(lc.has_identity, FALSE)
```

#### 6.4 SPARQL Compiler
```python
def compile_to_sparql(ast: ASTNode) -> str:
    if isinstance(ast, FieldRef):
        return f"?s erb:{toCamelCase(ast.name)} ?{toCamelCase(ast.name)}"
    if isinstance(ast, FuncCall):
        if ast.name == 'AND':
            patterns = [compile_to_sparql(a) for a in ast.args]
            return " . ".join(patterns)
        # ...
```

**Output**:
```sparql
?s erb:hasSyntax true .
?s erb:requiresParsing true .
?s erb:isDescriptionOf true .
FILTER NOT EXISTS { ?s erb:canBeHeld true }
FILTER NOT EXISTS { ?s erb:hasIdentity true }
```

#### 6.5 x86-64 Assembly Compiler
```python
def compile_to_assembly(ast: ASTNode) -> str:
    if isinstance(ast, FieldRef):
        return f"movzbl {FIELD_OFFSETS[ast.name]}(%rdi), %eax"
    if isinstance(ast, FuncCall):
        if ast.name == 'AND':
            # Chain of test/jz instructions
            # ...
```

**Output**:
```asm
    movzbl OFFSET_HAS_SYNTAX(%rdi), %eax
    test %al, %al
    jz .return_false
    movzbl OFFSET_REQUIRES_PARSING(%rdi), %eax
    test %al, %al
    jz .return_false
    ; ... continues for all conditions
```

### 7. The Compilation Matrix

| Formula | Python | Go | SQL | SPARQL | Assembly |
|---------|--------|----|----|--------|----------|
| `{{X}} = TRUE()` | `self.x is True` | `c.X` | `COALESCE(lc.x, FALSE)` | `?s erb:x true` | `movzbl OFF_X(%rdi), %eax` |
| `NOT({{X}})` | `not (self.x is True)` | `!c.X` | `NOT COALESCE(lc.x, FALSE)` | `FILTER NOT EXISTS {...}` | `test %al, %al; sete %al` |
| `AND(A, B)` | `a and b` | `a && b` | `(a) AND (b)` | `a . b` | `test; jz; test; jz` |
| `"str" & {{X}}` | `"str" + self.x` | `"str" + c.X` | `'str' \|\| lc.x` | `CONCAT("str", ?x)` | `call _string_concat` |

### 8. Dependency Extraction

The parser also extracts field dependencies for DAG ordering:

```python
def extract_dependencies(ast: ASTNode) -> Set[str]:
    if isinstance(ast, FieldRef):
        return {ast.name}
    if isinstance(ast, FuncCall):
        deps = set()
        for arg in ast.args:
            deps |= extract_dependencies(arg)
        return deps
    # ... recursively walk all nodes
```

**Example**:
```
TopFamilyFeudAnswer depends on: {HasSyntax, RequiresParsing, IsDescriptionOf, ...}
FamilyFeudMismatch depends on: {TopFamilyFeudAnswer, ChosenLanguageCandidate, ...}
```

### 9. The NULL Handling Problem

Different targets handle NULL differently:

| Target | NULL Strategy |
|--------|---------------|
| Python | `field or False` — coerce to False |
| Go | Pointer types `*bool`, explicit nil checks |
| SQL | `COALESCE(field, FALSE)` |
| SPARQL | `OPTIONAL { }` with `BOUND()` checks |
| Assembly | Sentinel byte values |

### 10. String Concatenation — The Hardest Part

The `FamilyFeudMismatch` formula is the most complex:
```
=IF(NOT({{TopFamilyFeudAnswer}} = {{ChosenLanguageCandidate}}),
  {{Name}} & " " & IF(...) & " a Family Feud Language..."
)
```

#### 10.1 Python (easy)
```python
f"{self.name} {('Is' if self.top_family_feud_answer else 'Isn\\'t')} a Family Feud Language..."
```

#### 10.2 SQL (medium)
```sql
name || ' ' || CASE WHEN top_family_feud_answer THEN 'Is' ELSE 'Isn''t' END || '...'
```

#### 10.3 x86 Assembly (hard!)
```asm
; String concatenation requires dynamic memory management
; Current binary substrate: 69.6% pass rate due to string edge cases
```

### 11. Testing Formula Compilation

The test suite verifies that all compilers produce equivalent results:

```
For each formula F:
    ast = parse(F)
    for each target T in {python, go, sql, sparql, asm}:
        code = compile_to_T(ast)
        result = execute_T(code, test_data)
        assert result == answer_key[field]
```

### 12. Adding a New Target

To add a new compilation target:

1. Define `compile_to_<target>(ast: ASTNode) -> str`
2. Handle each AST node type
3. Map field names to target naming convention
4. Handle NULL semantics for the target
5. Test against the answer key

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [formula_parser.py](../../orchestration/formula_parser.py) | Core parser and compilers |
| [effortless-rulebook.json](../../effortless-rulebook/effortless-rulebook.json) | Source formulas |

---

*Article content to be written...*
