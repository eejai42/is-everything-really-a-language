# Article 10: SPARQL — Queries as Computation

Most developers think of SPARQL as a query language. ERB proves it's a computation language. This article shows how formulas compile to SPARQL CONSTRUCT queries that compute derived RDF triples. We walk through the generated queries, run them against rdflib, and demonstrate 100% test accuracy. The insight: if your data is in a triplestore, you don't need a separate application layer for business logic.

---

## Detailed Table of Contents

### 1. SPARQL: More Than SELECT
- **Common View**: SPARQL = SQL for graphs (query only)
- **ERB View**: SPARQL = computation engine (CONSTRUCT creates new triples)
- **The Achievement**: 100% test accuracy with pure SPARQL
- **Test Time**: 270ms

### 2. The Generated Files

```
execution-substratrates/rdf/
├── schema.ttl           # RDFS schema (classes and properties)
├── data.ttl             # RDF instance data (125 candidates)
├── queries.sparql       # SPARQL CONSTRUCT queries
├── inject-into-rdf.py   # Code generator
├── take-test.py         # Test runner (uses rdflib)
├── test-answers.json    # Output for grading
└── README.md
```

### 3. The RDF Schema — `schema.ttl`

```turtle
@prefix erb: <http://example.org/erb#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

erb:LanguageCandidate a rdfs:Class ;
    rdfs:label "Language Candidate" .

erb:hasSyntax a rdfs:Property ;
    rdfs:domain erb:LanguageCandidate ;
    rdfs:range xsd:boolean .

erb:distanceFromConcept a rdfs:Property ;
    rdfs:domain erb:LanguageCandidate ;
    rdfs:range xsd:integer .

erb:topFamilyFeudAnswer a rdfs:Property ;
    rdfs:domain erb:LanguageCandidate ;
    rdfs:range xsd:boolean ;
    rdfs:comment "Computed via SPARQL CONSTRUCT" .
```

### 4. The Instance Data — `data.ttl`

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
```

### 5. SPARQL CONSTRUCT — The Key Insight

CONSTRUCT queries create new triples from existing data:

```sparql
PREFIX erb: <http://example.org/erb#>

CONSTRUCT {
    ?s erb:isDescriptionOf ?result .
}
WHERE {
    ?s erb:distanceFromConcept ?dist .
    BIND(IF(?dist > 1, true, false) AS ?result)
}
```

**Input**: Triples with `erb:distanceFromConcept`
**Output**: New triples with `erb:isDescriptionOf`

### 6. The Generated Queries — `queries.sparql`

#### 6.1 Level 1: `isDescriptionOf`
```sparql
# CONSTRUCT query for isDescriptionOf
PREFIX erb: <http://example.org/erb#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

CONSTRUCT {
    ?s erb:isDescriptionOf ?result .
}
WHERE {
    ?s a erb:LanguageCandidate .
    ?s erb:distanceFromConcept ?dist .
    BIND(IF(?dist > 1, true, false) AS ?result)
}
```

#### 6.2 Level 1: `isOpenClosedWorldConflicted`
```sparql
CONSTRUCT {
    ?s erb:isOpenClosedWorldConflicted ?result .
}
WHERE {
    ?s a erb:LanguageCandidate .
    OPTIONAL { ?s erb:isOpenWorld ?ow }
    OPTIONAL { ?s erb:isClosedWorld ?cw }
    BIND(COALESCE(?ow, false) AS ?openWorld)
    BIND(COALESCE(?cw, false) AS ?closedWorld)
    BIND(IF(?openWorld && ?closedWorld, true, false) AS ?result)
}
```

#### 6.3 Level 1: `familyFuedQuestion`
```sparql
CONSTRUCT {
    ?s erb:familyFuedQuestion ?result .
}
WHERE {
    ?s a erb:LanguageCandidate .
    ?s erb:name ?name .
    BIND(CONCAT("Is ", ?name, " a language?") AS ?result)
}
```

#### 6.4 Level 2: `topFamilyFeudAnswer`
```sparql
CONSTRUCT {
    ?s erb:topFamilyFeudAnswer ?result .
}
WHERE {
    ?s a erb:LanguageCandidate .
    OPTIONAL { ?s erb:hasSyntax ?hs }
    OPTIONAL { ?s erb:requiresParsing ?rp }
    OPTIONAL { ?s erb:isDescriptionOf ?ido }    # From Level 1!
    OPTIONAL { ?s erb:hasLinearDecodingPressure ?hldp }
    OPTIONAL { ?s erb:resolvesToAnAST ?raa }
    OPTIONAL { ?s erb:isStableOntologyReference ?isor }
    OPTIONAL { ?s erb:canBeHeld ?cbh }
    OPTIONAL { ?s erb:hasIdentity ?hi }

    BIND(COALESCE(?hs, false) AS ?hasSyntax)
    BIND(COALESCE(?rp, false) AS ?requiresParsing)
    BIND(COALESCE(?ido, false) AS ?isDescriptionOf)
    BIND(COALESCE(?hldp, false) AS ?hasLinearDecodingPressure)
    BIND(COALESCE(?raa, false) AS ?resolvesToAnAST)
    BIND(COALESCE(?isor, false) AS ?isStableOntologyReference)
    BIND(COALESCE(?cbh, false) AS ?canBeHeld)
    BIND(COALESCE(?hi, false) AS ?hasIdentity)

    BIND(
        IF(
            ?hasSyntax && ?requiresParsing && ?isDescriptionOf &&
            ?hasLinearDecodingPressure && ?resolvesToAnAST &&
            ?isStableOntologyReference && !?canBeHeld && !?hasIdentity,
            true, false
        ) AS ?result
    )
}
```

### 7. Query Execution Order

Queries must run in DAG order:
```
1. Run Level 1 queries (isDescriptionOf, familyFuedQuestion, etc.)
   → Add inferred triples to graph

2. Run Level 2 queries (topFamilyFeudAnswer)
   → Uses Level 1 results as input

3. Run Level 3 queries (familyFeudMismatch)
   → Uses Level 2 results as input
```

### 8. The Test Runner — Using rdflib

```python
#!/usr/bin/env python3
from rdflib import Graph, Namespace

def take_test():
    # 1. Load data graph
    g = Graph()
    g.parse('data.ttl', format='turtle')
    g.parse('schema.ttl', format='turtle')

    # 2. Load and execute queries in order
    with open('queries.sparql') as f:
        queries = parse_queries(f.read())

    for query in sorted(queries, key=lambda q: q['level']):
        # CONSTRUCT adds new triples to the graph
        result = g.query(query['sparql'])
        for triple in result:
            g.add(triple)

    # 3. Extract computed values
    ERB = Namespace("http://example.org/erb#")
    results = []
    for s in g.subjects(RDF.type, ERB.LanguageCandidate):
        record = {
            'language_candidate_id': str(s).split('#')[1],
            'top_family_feud_answer': bool(g.value(s, ERB.topFamilyFeudAnswer)),
            # ...
        }
        results.append(record)

    # 4. Write test-answers.json
    with open('test-answers.json', 'w') as f:
        json.dump(results, f)
```

### 9. SPARQL vs. Application Code

| Approach | Where Logic Lives | Pros | Cons |
|----------|------------------|------|------|
| **Application Code** | Python/Go/etc. | Familiar, debuggable | Logic duplicated |
| **SPARQL CONSTRUCT** | In the triplestore | Single source, portable | Learning curve |

### 10. The NULL Handling Pattern

SPARQL uses OPTIONAL + COALESCE for NULL-safe evaluation:

```sparql
OPTIONAL { ?s erb:hasSyntax ?hs }
BIND(COALESCE(?hs, false) AS ?hasSyntax)
```

- **OPTIONAL**: Don't fail if triple missing
- **COALESCE**: Replace NULL with default

### 11. Test Results

- **Pass Rate**: 100% (0 failures)
- **Execution Time**: 270ms
- **Records Processed**: 125
- **Triples Generated**: ~625 inferred triples

### 12. The Insight: Triplestore as Application Server

Traditional architecture:
```
Triplestore → Query → Application → Business Logic → Response
```

With SPARQL CONSTRUCT:
```
Triplestore → CONSTRUCT → Inferred Triples → Query → Response
```

The business logic lives in the database, not the application.

### 13. Comparison: SPARQL vs. SQL

| Feature | SQL | SPARQL |
|---------|-----|--------|
| **Schema** | Fixed tables | Flexible triples |
| **Computation** | Views + functions | CONSTRUCT queries |
| **NULL handling** | COALESCE | OPTIONAL + COALESCE |
| **Inference** | Limited | Native (with reasoners) |

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [schema.ttl](../../execution-substratrates/rdf/schema.ttl) | RDFS schema |
| [data.ttl](../../execution-substratrates/rdf/data.ttl) | Instance data |
| [queries.sparql](../../execution-substratrates/rdf/queries.sparql) | CONSTRUCT queries |
| [inject-into-rdf.py](../../execution-substratrates/rdf/inject-into-rdf.py) | Generator |
| [take-test.py](../../execution-substratrates/rdf/take-test.py) | Test runner |

---

*Article content to be written...*
