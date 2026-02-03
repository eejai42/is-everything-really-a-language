# Planned Documentation Series: ERB WikiData

A 20-part article/video series exploring the EffortlessAPI Rulebook (ERB) architecture through the WikiData "Is It a Natural Language?" demonstration project.

---

## [Article 1: The Single Source of Truth Problem](Article01-The-Single-Source-of-Truth-Problem/README.md)

*Abstract:* Most software projects suffer from the same disease: business logic scattered across databases, APIs, frontends, documentation, and spreadsheets. When rules change, teams play whack-a-mole updating dozens of files—and inevitably miss some. This article introduces the ERB philosophy: what if you could define your business rules exactly once, in a format humans can read and edit, and have every other representation generated automatically? We examine why this matters, what makes it hard, and preview how ERB solves it through a working example: determining whether something qualifies as a "natural language."

---

## [Article 2: The Airtable Rulebook — Where Truth Lives](Article02-The-Airtable-Rulebook/README.md)

*Abstract:* The entire system begins in Airtable—a spreadsheet-like interface that non-programmers can understand and edit. This article walks through every table, column, and relationship in the ERB_WikiData rulebook. We examine how language candidates are defined, how evaluation criteria become formula columns, and how the DAG (Directed Acyclic Graph) of calculations is implicitly encoded in cell references. By the end, you'll understand that this "simple spreadsheet" contains everything needed to generate a dozen different implementations.

---

## [Article 3: The Orchestration Layer — Conducting the Symphony](Article03-The-Orchestration-Layer/README.md)

*Abstract:* Between the Airtable source and the 12 execution substrates sits the orchestration layer. This article explains how `ssotme.json` defines the transpilation pipeline, how the test orchestrator validates every substrate against a unified answer key, and how the three-phase contract (Inject → Execute → Grade) ensures consistency. We'll trace a single change from Airtable through the entire build process, watching it propagate to Postgres, Python, Go, Excel, RDF, and even x86 assembly.

---

## [Article 4: The Formula Compilation Pipeline — One Formula, Twelve Targets](Article04-The-Formula-Compilation-Pipeline/README.md)

*Abstract:* The magic of ERB lies in its formula parser. An Excel-dialect formula like `=IF(AND(HasNativeSpeakers,HasWritingSystem),"Yes","No")` gets parsed into an Abstract Syntax Tree, then compiled to Python, JavaScript, Go, SQL, SPARQL, OCL, and x86-64 assembly. This article dissects the `formula_parser.py`, shows how each target compiler works, and demonstrates that the same business logic executes identically across radically different runtime environments.

---

## [Article 5: PostgreSQL — The Canonical Computation Engine](Article05-PostgreSQL/README.md)

*Abstract:* PostgreSQL isn't just another substrate—it's the source of truth for computed values. This article shows how ERB generates DDL tables, `calc_*` functions, materialized views, and Row Level Security policies from the rulebook. We examine how the function composition enforces DAG execution order, and why other substrates are graded against what Postgres computes. If you understand this substrate, you understand how ERB thinks about data.

---

## [Article 6: The Python Substrate — Readable, Testable, Shareable](Article06-The-Python-Substrate/README.md)

*Abstract:* Python serves as the most accessible execution substrate—readable code that matches the formulas almost 1:1. This article walks through the generated `erb_calc.py` module, shows how it implements the calculation DAG, and demonstrates the test harness. We also explore how other substrates (like YAML) can import and reuse Python calculations, proving that substrates can collaborate rather than exist in isolation.

---

## [Article 7: Excel/XLSX — The Universal Interface](Article07-Excel-XLSX/README.md)

*Abstract:* Business users live in spreadsheets. This article shows how ERB generates fully-functional Excel workbooks where formulas are preserved—not just values. Users can email these spreadsheets, modify data, and see computed fields update in real-time. We examine the xlsxwriter generation code, the formula translation layer, and why this "low-tech" output might be the most valuable substrate for organizational adoption.

---

## [Article 8: OWL, RDF, and SHACL — Semantic Web as Computation Platform](Article08-OWL-RDF-and-SHACL/README.md)

*Abstract:* The Semantic Web isn't just for knowledge graphs—it's a complete computation environment. This article shows how ERB generates OWL ontologies, RDF instance data, and SHACL-SPARQL rules that compute derived values through reasoning. We trace how a classification formula becomes a SHACL constraint, and demonstrate that pyshacl achieves 100% test accuracy. For anyone who thought RDF was "just data modeling," this is a revelation.

---

## [Article 9: The Binary Substrate — From Spreadsheet to Machine Code](Article09-The-Binary-Substrate/README.md)

*Abstract:* The most audacious claim of ERB: the same business rules that live in an Airtable spreadsheet can be compiled to native machine code. This article dissects the ARM64/x86-64 assembly generation, explains the minimal ABI with tagged unions, and shows how the generated `.dylib` is loaded via ctypes. We examine the assembly output line-by-line, proving that declarative formulas can become raw CPU instructions without losing semantic fidelity.

---

## [Article 10: SPARQL — Queries as Computation](Article10-SPARQL/README.md)

*Abstract:* Most developers think of SPARQL as a query language. ERB proves it's a computation language. This article shows how formulas compile to SPARQL CONSTRUCT queries that compute derived RDF triples. We walk through the generated queries, run them against rdflib, and demonstrate 100% test accuracy. The insight: if your data is in a triplestore, you don't need a separate application layer for business logic.

---

## [Article 11: GraphQL — Schema and Resolvers from Rules](Article11-GraphQL/README.md)

*Abstract:* Modern APIs speak GraphQL. This article shows how ERB generates both the SDL schema (with strong typing) and JavaScript resolver functions for computed fields. We examine how the calculation DAG maps to resolver dependencies, and demonstrate deployment with Apollo Server. The result: a type-safe API that implements your business rules without writing resolver code by hand.

---

## [Article 12: Go and Golang — Compiled Performance, Generated Safety](Article12-Go-and-Golang/README.md)

*Abstract:* For production systems that need speed, ERB generates Go code. This article examines the generated structs, calculation functions, and test harness. We explore how Go's type system catches errors that dynamic languages miss, and benchmark the performance difference. Special attention to the conditional `main.go` generation that preserves custom code while regenerating business logic.

---

## [Article 13: UML and PlantUML — Executable Diagrams with OCL](Article13-UML-and-PlantUML/README.md)

*Abstract:* UML diagrams are usually documentation that drifts from reality. ERB generates PlantUML class diagrams and object diagrams that are always current—plus OCL (Object Constraint Language) derive expressions for computed fields. This article shows how the visual model stays synchronized with the executable code, and how `model.json` enables programmatic OCL evaluation.

---

## [Article 14: The English Substrate — LLM-Validated Documentation](Article14-The-English-Substrate/README.md)

*Abstract:* What if your documentation was so precise that an AI could read it and correctly compute every derived value? The English substrate generates `specification.md`, `glossary.md`, and candidate profiles—then validates them by having an LLM read the prose and infer the answers. This article explores deterministic structure with stochastic content, pluggable LLM providers, and cost tier optimization. If the LLM gets the wrong answer, your documentation isn't clear enough.

---

## [Article 15: The Invariant System — Empirically Testable Claims](Article15-The-Invariant-System/README.md)

*Abstract:* ERB makes two bold operational claims: (1) rename an entity once in Airtable, and the change propagates deterministically to all 12 substrates; (2) the rulebook is semantically complete before any projection—no human interpretation needed. This article demonstrates both invariants with concrete examples, explains why they matter for system reliability, and shows how to verify them yourself.

---

## [Article 16: Falsifiers and the Scientific Method](Article16-Falsifiers-and-the-Scientific-Method/README.md)

*Abstract:* Good specifications aren't just true for valid cases—they correctly reject invalid ones. This article examines the "Falsifier A/B/C" test candidates designed to fail specific conditions. We explore how falsifiability strengthens the classification predicate, why edge cases reveal specification gaps, and how ERB's test harness catches both false positives and false negatives. The conclusion: business rules should be as rigorously testable as scientific hypotheses.

---

## [Article 17: The CMCC Conjecture](Article17-The-CMCC-Conjecture/README.md)

*Abstract:* The CMCC (Conditions, Mutability, Calculations, and Constraints) Conjecture proposes a fundamental classification of all business logic into four orthogonal categories. This article explores the theoretical foundations of CMCC, how it maps to the ERB architecture, and why separating these concerns enables the multi-substrate projection that powers this system. We examine how each category manifests differently across execution environments—from spreadsheet formulas to SQL constraints to SHACL shapes—while preserving semantic equivalence.

---

## [Article 18: Flatland vs Spaceland — Serial Time vs Parallel Projection](Article18-Flatland-vs-Spaceland/README.md)

*Abstract:* All deterministic substrates (Postgres, Python, Go, Excel, RDF, GraphQL, x86 assembly) complete their transformations in under one second. The English substrate takes 2+ minutes. Why? Because LLM inference must process tokens serially—real clock time passes while the model "thinks." Scale the rulebook 10x, and English takes 10x longer. The deterministic substrates? Still under a second. This article explores the profound implications: like Abbott's Flatland, LLM-based systems experience time as a constraining dimension that deterministic systems transcend entirely. We examine what this means for system design, cost modeling, and the future of hybrid architectures.

---

## [Article 19: The M4 Layer — Airtable as Meta-Meta-Meta-Model](Article19-The-M4-Layer/README.md)

*Abstract:* The OMG's four-layer metamodel architecture (M0-M3) defines how models relate to their instances: M0 is runtime data, M1 is the model, M2 is the metamodel (like UML), and M3 is the meta-metamodel (MOF). But where does the Airtable rulebook fit? This article argues it operates at an implicit M4 layer—a specification so abstract it can project downward into multiple M2/M3 formalisms simultaneously (UML, OWL, SQL DDL, GraphQL SDL). We explore how this perspective explains ERB's power: it's not just code generation, it's metamodel generation. The rulebook doesn't describe a system; it describes the language for describing systems.

---

## [Article 20: Past, Present, and Future Languages](Article20-Past-Present-and-Future-Languages/README.md)

*Abstract:* The WikiData "Is It a Natural Language?" example isn't arbitrary—it's a meditation on time and classification. Some candidates (Latin, Sanskrit) were once living languages but are now "dead." Others (English, Mandarin) are vibrant today. Still others (constructed languages, emerging creoles) represent possible futures. This article explores how ERB handles temporal predicates: can a classification change over time? How do we model historical truth vs. current truth vs. projected truth? We examine how the rulebook's formula system can encode time-aware logic, and what this means for business rules that must reason about past states, present conditions, and future possibilities.

---

## Appendix: Suggested Reading Order

**For Executives/Decision-Makers:** Articles 1, 7, 9, 15, 18
**For Developers:** Articles 1-6, then any substrates relevant to your stack
**For Data Architects:** Articles 1, 2, 5, 8, 10, 19
**For AI/ML Engineers:** Articles 14, 4, 16, 18
**For Theorists/Academics:** Articles 17, 19, 16, 20
**For the Deeply Curious:** All 20 in order

---

## Production Notes

- Each article should include runnable code examples from the repository
- Video versions should show live terminal output from the test orchestrator
- Consider interactive demos where viewers can modify Airtable and watch propagation
- The binary/assembly article will need careful explanation for non-systems programmers
