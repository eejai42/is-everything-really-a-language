# ERB Specification - Language Classification Rulebook

---

## Overview

The primary objective of this formal rulebook system is to establish a clear and rigorous definition of "language" that addresses the often-debated question of whether everything can be classified as a language. In contemporary discourse, the term "language" is frequently applied too broadly, leading to ambiguity and confusion about its true essence. This system aims to delineate the boundaries of what constitutes a language, thereby providing a framework that avoids the pitfalls of overgeneralization while still recognizing the complexities inherent in diverse linguistic forms.

At the core of this system lies a well-defined operational thesis that articulates language as a structured system of communication characterized by specific rules and conventions. This definition emphasizes the necessity of systematic organization and functional coherence, which distinguishes genuine languages from mere collections of signs or informal communication methods. By anchoring the concept of language in concrete criteria, the system seeks to clarify what qualifies as a language and what does not, ultimately contributing to a more precise understanding of linguistic phenomena.

The model structure of this system is designed to process a set of raw predicates—definable properties that can be evaluated against potential language candidates. These raw inputs feed into a series of calculated fields that derive essential properties necessary for classification. The culmination of this process is a systematic classification that determines whether a given candidate qualifies as a language or is better categorized as something else, such as a sign vehicle or a semiotic process. This structured approach not only organizes the evaluation but also ensures that the classification is grounded in a coherent and consistent rationale.

This endeavor is significant because it fosters a clearer distinction between true language systems and other forms of communication that may lack the necessary structure or rules to be considered languages in the formal sense. By refining our understanding of language, we can better appreciate the nuances of human communication, the evolution of linguistic systems, and the cognitive processes involved in language use. Ultimately, this system contributes to a more informed discourse around language, enhancing both academic inquiry and practical applications in fields such as linguistics, cognitive science, and communication studies.

---

## Model Structure

The model operates on a set of raw predicates (input properties) that are evaluated for each candidate,
which then feed into calculated fields that derive the final classification.

### Raw Predicates (Inputs)

These are the fundamental properties evaluated for each candidate:


### Calculated Fields (Derived)

These fields are computed from the raw predicates:


---

## Core Language Definition

An item qualifies as a **Language** if and only if ALL of these are true:

1. HasSyntax = true
2. RequiresParsing = true
3. HasLinearDecodingPressure = true
4. StableOntologyReference = true
5. CanBeHeld = false
6. HasIdentity = false
7. DistanceFromConcept = 2

---

## Calculated Field Instructions
