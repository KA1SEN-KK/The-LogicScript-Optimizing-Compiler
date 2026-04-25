# The LogicScript Optimizing Compiler

## 1. Project Overview

This project implements a four-phase optimizing compiler for a custom micro-language called **LogicScript**.

The compiler is designed to:

1. read a LogicScript source file,
2. perform lexical analysis,
3. validate syntax and generate an Abstract Syntax Tree (AST),
4. optimize logical expressions,
5. verify optimization correctness,
6. execute the optimized program,
7. export the full pipeline trace as a JSON file.

The project is based on the specification in **Project 1: The LogicScript Optimizing Compiler**.

---

## 2. Final Submission Format

The final submission is centered on **one main Python file**:

logic_compiler.py

---

## 3. Execution Guide

If your input file and output file are input.txt and ouput.json.
You can run this compiler using this command:
`python3 logic_compiler.py input.txt output.json`

## 4.Implementation Pipeline

### (1) Phase 1: Lexical Analysis

This phase will tokenize the LogicScript into formatted tokens line by line. Using the defined Token map.

Examples:

let p = T → ["LET", "VAR_P", "EQ", "TRUE"]

let q = F → ["LET", "VAR_Q", "EQ", "FALSE"]

let r = (NOT ((NOT p) AND q)) → ["LET", "VAR_R", "EQ", "L_PAREN", "NOT", "L_PAREN", "L_PAREN", "NOT", "VAR_P", "R_PAREN", "AND", "VAR_Q", "R_PAREN", "R_PAREN"]

if r then print p → ["IF", "VAR_R", "THEN", "PRINT", "VAR_P"]

The lexer uses a small character buffer while scanning each word. When it sees a parenthesis, it first flushes the buffered fragment into a keyword/variable token, then emits the parenthesis token itself. This is why nested expressions can be tokenized correctly even when parentheses are attached to words.

### (2) Phase 2: Syntax Validation and AST Generation

This phase checks whether the token sequence follows the recursive grammar rules and converts each statement into a nested-list AST.

Examples:

(NOT p) → ["NOT", "VAR_P"]  <br>
(p AND q) → ["AND", "VAR_P", "VAR_Q"] <br>
let x = (p OR T) → ["LET", "VAR_X", ["OR", "VAR_P", "TRUE"]]

If the token order is invalid, if parentheses are mismatched, or if required structure is missing, the compiler stops and records a Phase 2 error.

The parser is divided into several focused functions:
* **is_variable**: Return whether a token is a valid variable token.
* **run_parser_phase**: Parse tokenized lines into AST records.
* **parse_line**: Parse one full line and ensure no extra tokens remain.
* **parse_statement**: Parse a statement starting at index.
* **parse_let_statement**:Parse: LET VAR_X EQ expression
* **parse_if_statement**:Parse: IF expression THEN statement
* **parse_print_statement**: Parse: PRINT VAR_X
* **parse_expression**: Parse an expression
* **parse_parenthesized_expression**: Parse a parenthesized recursive expression.

This decomposition makes each function responsible for one syntactic rule, reducing ambiguity and helping isolate bugs.

When the function capture any error in the parser phase, it will raise a ParseError which includes the num of error line and a message "phase_2_parser" showing
the stopped phase.

### (3) Phase 3: The Optimization Pass

This phase simplifies the parsed AST by repeatedly applying Boolean rewrite rules while preserving logical equivalence.

Examples:

(NOT (NOT p)) → p

(p IMPLIES q) → ((NOT p) OR q)

((a AND b) OR ((NOT a) AND c) OR (b AND c)) → ((a AND b) OR ((NOT a) AND c))

((a OR b) AND ((NOT a) OR c) AND (b OR c)) → ((a OR b) AND ((NOT a) OR c))

The optimizer applies rules in an iterative loop until no further change is found.

Basic optimization rules include:
* implication elimination
* De Morgan law
* double negative law
* idempotent law
* identity law
* negation law
* universal bound law
* absorption law
* negation of TRUE/FALSE

The optimizer is divided into several focused functions:
* **run_optimizer_phase**: Optimize each parsed line and collect verification seeds.
* **optimize_ast**: Entry point for one AST node.
* **_optimize_node**: Distinguish statement nodes (LET/IF/PRINT) from expression nodes.
* **_optimize_expression_recursively**: Optimize nested subexpressions bottom-up.
* **_optimize_expression**: Apply all optimization rules until fixed-point.

Beyond the basic rules taught in class, this implementation also includes two exploratory optimizations:
* **normalization optimization**: Flatten nested AND/OR chains and remove duplicate terms.
* **consensus theorem optimization**: Remove consensus terms in SOP/POS patterns to simplify expressions further.

If optimization changes an AST, Phase 3 records the original and optimized forms in a verification seed. Phase 4 then uses this seed to run equivalence checking on the optimized results.
