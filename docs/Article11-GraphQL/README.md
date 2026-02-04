# Article 11: GraphQL — Schema and Resolvers from Rules

Modern APIs speak GraphQL. This article shows how ERB generates both the SDL schema (with strong typing) and JavaScript resolver functions for computed fields. We examine how the calculation DAG maps to resolver dependencies, and demonstrate deployment with Apollo Server. The result: a type-safe API that implements your business rules without writing resolver code by hand.

---

## Detailed Table of Contents

### 1. Why GraphQL?
- **Type-Safe APIs**: Schema defines what's queryable
- **Single Endpoint**: One URL, flexible queries
- **Computed Fields**: Resolvers calculate values on demand
- **Test Time**: 139ms — one of the fastest substrates

### 2. The Generated Files

```
execution-substratrates/graphql/
├── schema.graphql         # Type definitions (SDL)
├── resolvers.js           # JavaScript resolver functions
├── inject-into-graphql.py # Code generator
├── take-test.py           # Test runner
├── take-test.sh           # Shell wrapper
├── test-answers.json      # Output for grading
└── README.md
```

### 3. The Schema — `schema.graphql`

```graphql
type Query {
    languageCandidates: [LanguageCandidate!]!
    languageCandidate(id: ID!): LanguageCandidate
}

type LanguageCandidate {
    # Raw fields (stored data)
    language_candidate_id: ID!
    name: String
    category: String
    has_syntax: Boolean
    has_identity: Boolean
    can_be_held: Boolean
    requires_parsing: Boolean
    resolves_to_an_ast: Boolean
    has_linear_decoding_pressure: Boolean
    is_stable_ontology_reference: Boolean
    is_live_ontology_editor: Boolean
    is_open_world: Boolean
    is_closed_world: Boolean
    distance_from_concept: Int
    dimensionality_while_editing: String
    model_object_facility_layer: String
    chosen_language_candidate: Boolean
    sort_order: Int

    # Computed fields (resolved on query)
    family_fued_question: String
    has_grammar: Boolean
    is_description_of: Boolean
    is_open_closed_world_conflicted: Boolean
    relationship_to_concept: String
    top_family_feud_answer: Boolean
    family_feud_mismatch: String
}
```

### 4. The Resolvers — `resolvers.js`

#### 4.1 Resolver Structure
```javascript
const resolvers = {
    Query: {
        languageCandidates: (_, __, { dataSources }) => {
            return dataSources.languageCandiatesAPI.getAll();
        },
        languageCandidate: (_, { id }, { dataSources }) => {
            return dataSources.languageCandiatesAPI.getById(id);
        }
    },

    LanguageCandidate: {
        // Level 1 computed fields
        family_fued_question: (parent) => {
            return `Is ${parent.name} a language?`;
        },

        has_grammar: (parent) => {
            return parent.has_syntax === true;
        },

        is_description_of: (parent) => {
            return (parent.distance_from_concept || 0) > 1;
        },

        is_open_closed_world_conflicted: (parent) => {
            return (parent.is_open_world === true) &&
                   (parent.is_closed_world === true);
        },

        relationship_to_concept: (parent) => {
            return parent.distance_from_concept === 1
                ? "IsMirrorOf"
                : "IsDescriptionOf";
        },

        // Level 2 computed field (depends on Level 1)
        top_family_feud_answer: (parent, _, __, info) => {
            // Note: is_description_of must be resolved first
            const isDescriptionOf = (parent.distance_from_concept || 0) > 1;

            return (
                (parent.has_syntax === true) &&
                (parent.requires_parsing === true) &&
                isDescriptionOf &&
                (parent.has_linear_decoding_pressure === true) &&
                (parent.resolves_to_an_ast === true) &&
                (parent.is_stable_ontology_reference === true) &&
                !(parent.can_be_held === true) &&
                !(parent.has_identity === true)
            );
        },

        // Level 3 computed field (depends on Level 2)
        family_feud_mismatch: (parent) => {
            const topAnswer = /* compute top_family_feud_answer */;
            const isConflicted = /* compute is_open_closed_world_conflicted */;

            let result = "";
            if (topAnswer !== parent.chosen_language_candidate) {
                const isWord = topAnswer ? "Is" : "Isn't";
                const markedWord = parent.chosen_language_candidate ? "Is" : "Is Not";
                result = `${parent.name} ${isWord} a Family Feud Language, but ${markedWord} marked as a 'Language Candidate.'`;
            }
            if (isConflicted) {
                result += " - Open World vs. Closed World Conflict.";
            }
            return result || null;
        }
    }
};
```

### 5. DAG Mapping to Resolver Dependencies

```
GraphQL Query:
{
    languageCandidate(id: "english") {
        name
        top_family_feud_answer    # Needs is_description_of
        family_feud_mismatch      # Needs top_family_feud_answer
    }
}

Resolver Execution Order:
1. Query.languageCandidate → returns raw record
2. LanguageCandidate.name → returns stored value
3. LanguageCandidate.top_family_feud_answer → computes from raw + is_description_of
4. LanguageCandidate.family_feud_mismatch → computes from top_family_feud_answer
```

### 6. The Test Runner

```javascript
// take-test.js
const { ApolloServer } = require('apollo-server');
const typeDefs = require('./schema.graphql');
const resolvers = require('./resolvers.js');

const server = new ApolloServer({
    typeDefs,
    resolvers,
    dataSources: () => ({
        languageCandiatesAPI: new LanguageCandidatesAPI()
    })
});

// Query all candidates with computed fields
const query = `{
    languageCandidates {
        language_candidate_id
        top_family_feud_answer
        family_feud_mismatch
        is_open_closed_world_conflicted
        relationship_to_concept
        family_fued_question
    }
}`;

const result = await server.executeOperation({ query });
// Write to test-answers.json
```

### 7. Schema Generation from Rulebook

```python
def inject_into_graphql():
    # 1. Load rulebook
    rulebook = load_rulebook()

    # 2. Generate SDL
    sdl = "type Query {\n"
    sdl += "    languageCandidates: [LanguageCandidate!]!\n"
    sdl += "    languageCandidate(id: ID!): LanguageCandidate\n"
    sdl += "}\n\n"
    sdl += "type LanguageCandidate {\n"

    for field in schema:
        graphql_type = map_to_graphql_type(field.datatype)
        sdl += f"    {to_snake_case(field.name)}: {graphql_type}\n"

    sdl += "}\n"

    # 3. Generate resolvers
    resolvers = "const resolvers = {\n"
    resolvers += "    Query: { ... },\n"
    resolvers += "    LanguageCandidate: {\n"

    for field in schema:
        if field.type == 'calculated':
            resolver_code = compile_to_javascript(field.formula)
            resolvers += f"        {field.name}: (parent) => {resolver_code},\n"

    resolvers += "    }\n};\n"
```

### 8. Type Mapping

| Rulebook Type | GraphQL Type |
|---------------|--------------|
| `string` | `String` |
| `boolean` | `Boolean` |
| `integer` | `Int` |
| `number` | `Float` |
| Primary key | `ID!` |

### 9. The NULL Handling Strategy

GraphQL distinguishes nullable vs non-nullable:
- `String` — can be null
- `String!` — cannot be null
- `[String!]!` — non-null array of non-null strings

Resolvers use JavaScript truthy checks:
```javascript
// parent.has_syntax might be null/undefined
(parent.has_syntax === true)  // Explicit true check
```

### 10. Test Results

- **Pass Rate**: 100% (0 failures)
- **Execution Time**: 139ms
- **Why Fast?**: JavaScript is fast; no network overhead in test

### 11. Deployment Options

#### 11.1 Apollo Server (Node.js)
```javascript
const { ApolloServer } = require('apollo-server');
const server = new ApolloServer({ typeDefs, resolvers });
server.listen().then(({ url }) => {
    console.log(`Server ready at ${url}`);
});
```

#### 11.2 AWS AppSync
Upload `schema.graphql` and attach resolvers to Lambda functions.

#### 11.3 Hasura
Generate Hasura metadata from the schema; use computed fields.

### 12. Sample Queries

#### 12.1 Get All Languages
```graphql
{
    languageCandidates {
        name
        category
        top_family_feud_answer
    }
}
```

#### 12.2 Filter by Classification
```graphql
{
    languageCandidates {
        name
        top_family_feud_answer
    }
}
# Client-side filter: result.filter(c => c.top_family_feud_answer)
```

#### 12.3 Get Single Candidate with All Computed Fields
```graphql
{
    languageCandidate(id: "english") {
        name
        category
        top_family_feud_answer
        family_feud_mismatch
        is_open_closed_world_conflicted
        relationship_to_concept
        family_fued_question
    }
}
```

### 13. The Value Proposition

- **No Manual Resolver Code**: Generated from formulas
- **Type Safety**: Schema enforces contracts
- **Self-Documenting**: Schema is the API documentation
- **Extensible**: Add custom resolvers alongside generated ones

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [schema.graphql](../../execution-substratrates/graphql/schema.graphql) | Type definitions |
| [resolvers.js](../../execution-substratrates/graphql/resolvers.js) | Resolver functions |
| [inject-into-graphql.py](../../execution-substratrates/graphql/inject-into-graphql.py) | Generator |
| [take-test.py](../../execution-substratrates/graphql/take-test.py) | Test runner |

---

*Article content to be written...*
