# Article 8: OWL, RDF, and SHACL — Semantic Web as Computation Platform

The Semantic Web isn't just for knowledge graphs—it's a complete computation environment. This article shows how ERB generates OWL ontologies, RDF instance data, and SHACL-SPARQL rules that compute derived values through reasoning. We trace how a classification formula becomes a SHACL constraint, and demonstrate that pyshacl achieves 100% test accuracy. For anyone who thought RDF was "just data modeling," this is a revelation.

---

## Detailed Table of Contents

### 1. The Semantic Web Surprise
- **Common Misconception**: RDF/OWL is for data modeling, not computation
- **The Reality**: With SHACL-SPARQL rules, it's a complete inference engine
- **The Achievement**: 100% test accuracy through reasoning alone
- **Test Time**: 2.41s (includes reasoning)

### 2. The Three Generated Files

```
execution-substrates/owl/
├── ontology.owl           # OWL 2 class definitions + properties
├── individuals.ttl        # RDF instance data (125 candidates)
├── rules.shacl.ttl        # SHACL-SPARQL rules for computed fields
├── inject-into-owl.py     # Injector script
├── take-test.py           # Test runner (uses pyshacl)
├── test-answers.json      # Output for grading
└── README.md
```

### 3. The OWL Ontology — `ontology.owl`

#### 3.1 Namespace Declarations
```turtle
@prefix erb: <http://example.org/erb#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
```

#### 3.2 Class Definition
```turtle
erb:LanguageCandidate a owl:Class ;
    rdfs:label "Language Candidate" ;
    rdfs:comment "An entity being evaluated for language classification." .
```

#### 3.3 Data Properties (Raw Fields)
```turtle
erb:hasSyntax a owl:DatatypeProperty ;
    rdfs:domain erb:LanguageCandidate ;
    rdfs:range xsd:boolean ;
    rdfs:label "Has Syntax" .

erb:requiresParsing a owl:DatatypeProperty ;
    rdfs:domain erb:LanguageCandidate ;
    rdfs:range xsd:boolean ;
    rdfs:label "Requires Parsing" .

erb:distanceFromConcept a owl:DatatypeProperty ;
    rdfs:domain erb:LanguageCandidate ;
    rdfs:range xsd:integer ;
    rdfs:label "Distance From Concept" .

# ... 15+ more properties
```

#### 3.4 Computed Properties (Derived via SHACL)
```turtle
erb:topFamilyFeudAnswer a owl:DatatypeProperty ;
    rdfs:domain erb:LanguageCandidate ;
    rdfs:range xsd:boolean ;
    rdfs:label "Top Family Feud Answer" ;
    rdfs:comment "Computed via SHACL-SPARQL rule." .
```

### 4. The RDF Instance Data — `individuals.ttl`

```turtle
erb:english a erb:LanguageCandidate ;
    erb:name "English" ;
    erb:category "Natural Language" ;
    erb:hasSyntax true ;
    erb:requiresParsing true ;
    erb:canBeHeld false ;
    erb:hasIdentity false ;
    erb:hasLinearDecodingPressure true ;
    erb:isStableOntologyReference true ;
    erb:distanceFromConcept 2 ;
    erb:chosenLanguageCandidate true .

erb:a-coffee-mug a erb:LanguageCandidate ;
    erb:name "A Coffee Mug" ;
    erb:category "Physical Object" ;
    erb:hasSyntax false ;
    erb:canBeHeld true ;
    erb:hasIdentity true ;
    erb:distanceFromConcept 1 ;
    erb:chosenLanguageCandidate false .

# ... 123 more individuals
```

### 5. The SHACL-SPARQL Rules — `rules.shacl.ttl`

#### 5.1 What is SHACL-SPARQL?
- **SHACL**: Shapes Constraint Language for RDF validation
- **SHACL-SPARQL**: Extension that allows SPARQL queries in rules
- **Key Feature**: Can derive new triples (not just validate)

#### 5.2 Level 1 Rule: `isDescriptionOf`
```turtle
erb:IsDescriptionOfRule a sh:NodeShape ;
    sh:target [
        a sh:SPARQLTarget ;
        sh:select """
            SELECT ?this WHERE {
                ?this a erb:LanguageCandidate .
            }
        """
    ] ;
    sh:rule [
        a sh:SPARQLRule ;
        sh:construct """
            CONSTRUCT {
                $this erb:isDescriptionOf ?result .
            }
            WHERE {
                $this erb:distanceFromConcept ?dist .
                BIND(IF(?dist > 1, true, false) AS ?result)
            }
        """
    ] .
```

#### 5.3 Level 2 Rule: `topFamilyFeudAnswer`
```turtle
erb:TopFamilyFeudAnswerRule a sh:NodeShape ;
    sh:target [
        a sh:SPARQLTarget ;
        sh:select """
            SELECT ?this WHERE {
                ?this a erb:LanguageCandidate .
            }
        """
    ] ;
    sh:rule [
        a sh:SPARQLRule ;
        sh:construct """
            CONSTRUCT {
                $this erb:topFamilyFeudAnswer ?result .
            }
            WHERE {
                $this erb:hasSyntax ?hasSyntax .
                $this erb:requiresParsing ?requiresParsing .
                $this erb:isDescriptionOf ?isDescriptionOf .
                $this erb:hasLinearDecodingPressure ?hasLinearDecodingPressure .
                $this erb:resolvesToAnAST ?resolvesToAnAST .
                $this erb:isStableOntologyReference ?isStableOntologyReference .
                $this erb:canBeHeld ?canBeHeld .
                $this erb:hasIdentity ?hasIdentity .

                BIND(
                    IF(
                        ?hasSyntax = true &&
                        ?requiresParsing = true &&
                        ?isDescriptionOf = true &&
                        ?hasLinearDecodingPressure = true &&
                        ?resolvesToAnAST = true &&
                        ?isStableOntologyReference = true &&
                        ?canBeHeld = false &&
                        ?hasIdentity = false,
                        true, false
                    ) AS ?result
                )
            }
        """
    ] .
```

### 6. The Reasoning Process

```
┌─────────────────────────────────────────────────────────────┐
│                    PYSHACL INFERENCE                         │
└─────────────────────────────────────────────────────────────┘

Input:
├── ontology.owl (schema)
├── individuals.ttl (instance data - raw fields only)
└── rules.shacl.ttl (computation rules)

Processing:
1. Load all graphs into memory
2. Execute SHACL rules in order:
   └── Level 1 rules (isDescriptionOf, etc.)
   └── Level 2 rules (topFamilyFeudAnswer)
   └── Level 3 rules (familyFeudMismatch)
3. CONSTRUCT queries add new triples

Output:
└── Inferred triples (computed fields)
    erb:english erb:topFamilyFeudAnswer true .
    erb:english erb:isDescriptionOf true .
    erb:a-coffee-mug erb:topFamilyFeudAnswer false .
```

### 7. The Test Runner — Using pyshacl

```python
#!/usr/bin/env python3
from pyshacl import validate
from rdflib import Graph, Namespace

def take_test():
    # 1. Load graphs
    data_graph = Graph()
    data_graph.parse('individuals.ttl', format='turtle')

    shacl_graph = Graph()
    shacl_graph.parse('rules.shacl.ttl', format='turtle')

    ont_graph = Graph()
    ont_graph.parse('ontology.owl', format='turtle')

    # 2. Run inference (key: inference='rdfs')
    conforms, results_graph, results_text = validate(
        data_graph,
        shacl_graph=shacl_graph,
        ont_graph=ont_graph,
        inference='rdfs',
        inplace=True  # Modify data_graph with inferred triples
    )

    # 3. Query inferred values
    ERB = Namespace("http://example.org/erb#")
    results = []
    for s, p, o in data_graph:
        if p == ERB.topFamilyFeudAnswer:
            # Extract language_candidate_id and computed value
            ...

    # 4. Write test-answers.json
    with open('test-answers.json', 'w') as f:
        json.dump(results, f)
```

### 8. OWL vs. RDF vs. SHACL — Role Comparison

| Technology | Role in ERB | File |
|------------|-------------|------|
| **OWL** | Schema definition (classes, properties) | ontology.owl |
| **RDF** | Instance data (individuals, raw values) | individuals.ttl |
| **SHACL** | Computation rules (derived values) | rules.shacl.ttl |

### 9. Why SHACL-SPARQL Works for ERB

| Feature | Benefit |
|---------|---------|
| **Declarative** | Rules describe "what" not "how" |
| **Graph-based** | Natural fit for entity relationships |
| **Incremental** | Can rerun rules after data changes |
| **Standard** | W3C recommendation, portable |

### 10. The NULL/Open-World Challenge

RDF uses open-world assumption (OWA):
- Missing triple doesn't mean "false"
- Missing triple means "unknown"

ERB handles this with explicit false values:
```turtle
# Instead of omitting canBeHeld for non-physical objects:
erb:english erb:canBeHeld false .  # Explicitly false
```

### 11. Test Results

- **Pass Rate**: 100% (0 failures)
- **Execution Time**: 2.41s (includes reasoning)
- **Why Slower?**: Graph traversal + SPARQL evaluation overhead

### 12. Querying the Inferred Graph

After inference, you can query with standard SPARQL:

```sparql
# Find all languages
SELECT ?name WHERE {
    ?s erb:topFamilyFeudAnswer true .
    ?s erb:name ?name .
}

# Find mismatches
SELECT ?name ?computed ?marked WHERE {
    ?s erb:topFamilyFeudAnswer ?computed .
    ?s erb:chosenLanguageCandidate ?marked .
    ?s erb:name ?name .
    FILTER(?computed != ?marked)
}
```

### 13. The Revelation: RDF as Computation Platform

Traditional view:
```
RDF = data storage + queries
```

ERB view:
```
RDF + SHACL-SPARQL = data storage + queries + inference + computation
```

The same business logic that runs in Python, SQL, and assembly also runs in a triplestore.

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [ontology.owl](../../execution-substrates/owl/ontology.owl) | OWL schema |
| [individuals.ttl](../../execution-substrates/owl/individuals.ttl) | RDF instance data |
| [rules.shacl.ttl](../../execution-substrates/owl/rules.shacl.ttl) | SHACL-SPARQL rules |
| [inject-into-owl.py](../../execution-substrates/owl/inject-into-owl.py) | Generator |
| [take-test.py](../../execution-substrates/owl/take-test.py) | Test runner |

---

*Article content to be written...*
