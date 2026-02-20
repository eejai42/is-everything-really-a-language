# ERB Specification - Language Classification Rulebook

---

## Overview

This formal rulebook system is designed to establish a clear and precise definition of what constitutes a "language." In an era where the term is often applied too broadly, leading to the notion that "everything is a language," the system aims to delineate the boundaries of language in a way that is both inclusive and exclusive. By doing so, it seeks to provide a framework for understanding the essential characteristics that define a language, helping researchers, linguists, and theorists navigate the complexities of communication systems without diluting the term through overextension.

At the heart of this system lies a core thesis that operationalizes the concept of language through specific criteria and properties. These criteria are informed by an understanding of the fundamental aspects that differentiate language from other forms of communication. The operational definition will encompass elements such as grammar, syntax, semantics, and the capacity for abstraction and creativity, allowing for a nuanced classification of various communication systems while avoiding the pitfalls of overly broad interpretations.

The model structure of this system is predicated on a systematic evaluation of raw predicates—input properties that describe the essential features of a given communication system. These predicates are processed to yield calculated fields, or derived properties, which are then used to classify the subject as either a language or not. This structured approach ensures that the evaluation process is rigorous and consistent, providing a clear pathway from initial observation to final classification. By employing this systematic methodology, the system can effectively discern the defining traits of linguistic systems from those of mere sign vehicles or semiotic processes.

The importance of this framework cannot be overstated, as it offers critical insights into how we understand and categorize communication. By distinguishing between true language systems and other forms of signification, the system fosters a deeper appreciation for the intricacies of human communication and cognition. This clarity not only aids in academic discourse but also has practical implications in fields such as artificial intelligence, cognitive science, and anthropology, where the definition of language can significantly influence research and applications. Ultimately, this rulebook system serves as a foundational tool for advancing our understanding of what it means to communicate meaningfully.

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
