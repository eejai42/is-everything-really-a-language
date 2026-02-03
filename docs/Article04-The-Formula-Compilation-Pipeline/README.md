# Article 4: The Formula Compilation Pipeline — One Formula, Twelve Targets

The magic of ERB lies in its formula parser. An Excel-dialect formula like `=IF(AND(HasNativeSpeakers,HasWritingSystem),"Yes","No")` gets parsed into an Abstract Syntax Tree, then compiled to Python, JavaScript, Go, SQL, SPARQL, OCL, and x86-64 assembly. This article dissects the `formula_parser.py`, shows how each target compiler works, and demonstrates that the same business logic executes identically across radically different runtime environments.

---

## Content

*Article content to be written...*
