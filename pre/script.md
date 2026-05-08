## Script
@KA1SEN-KK

### Page 7
Phase one is the lexer. It scans each line and produces named tokens using a buffer-based strategy: characters accumulate in a buffer and flush once encountering a parenthesis, so spacing around them is optional. Reserved words hit a dictionary lookup; single-lowercase-letter variables become VAR_P, VAR_Q, and so on. Any unrecognized sequence raises a LexicalError immediately with the line number, preventing errors from propagating downstream.

### Page 8
Phase two is a recursive descent parser whose structure mirrors the grammar directly — one function per rule. parse_statement dispatches to the let, if, or print handler; expressions recurse through parse_expression and parse_parenthesized_expression. A ParseError always names the exact construct that failed and its line. The output is a list of nested Python lists — compact, recursive, and directly usable by the optimizer.

### Page 9 & 10
Phase three applies eleven Boolean rewrite rules in a bottom-up fixed-point loop. Children are simplified before parents, so sub-expressions are already optimized when a compound node is reached. Rules run in priority order: implication elimination goes first, converting IMPLIES to OR-NOT and unlocking later rules; De Morgan and double negation follow; the remaining eight run until a full pass produces no change — the fixed-point condition. A cap of sixty-four iterations guards against cycles.

On line three, De Morgan fires on NOT of an AND, rewriting to OR of two negations; double negation then eliminates the redundant NOT on p, yielding p OR NOT-q — three nodes instead of six. The consensus theorem goes further: in any OR expression where two AND-terms share a complementary literal, the third term is redundant and removed. The dual form handles AND expressions.

### Page 11 & 12
Phase four starts with equivalence verification. For each optimized line, the verifier enumerates all 2-to-the-n truth assignments over the combined variable set, evaluates both ASTs on each row, and marks the result is_equivalent TRUE only if every row matches — a bug in the optimizer would surface here.

Execution then processes optimized statements line by line: LET stores results in a state dictionary, IF evaluates its condition and recurses if TRUE, PRINT looks up and records the variable's value. All errors share a unified hierarchy — CompilerError base with Lexical, Parse, and Execution subtypes — each carrying a phase and line number for precise reporting.