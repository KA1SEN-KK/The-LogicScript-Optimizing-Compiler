# Pre-definitions for the compiler pipeline, including error classes and the main compile function.

from typing import Optional


class CompilerError(Exception):
	"""Base class for all compiler pipeline errors."""

	def __init__(self, phase: str, line: int) -> None:
		super().__init__()
		self.phase = phase
		self.line = line


class LexicalError(CompilerError):
	"""Raised when lexical analysis fails."""

	def __init__(self, line: int) -> None:
		super().__init__("phase_1_lexer", line)


class ParseError(CompilerError):
	"""Raised when syntax validation fails."""

	def __init__(self, line: int) -> None:
		super().__init__("phase_2_parser", line)


class OptimizationError(CompilerError):
	"""Raised when optimization fails unexpectedly."""

	def __init__(self, line: int) -> None:
		super().__init__("phase_3_optimizer", line)


class ExecutionError(CompilerError):
	"""Raised when execution or verification fails."""

	def __init__(self, line: int) -> None:
		super().__init__("phase_4_execution", line)

# Phase 1: Tokenizer

# Example input
# let p = T
# let q = F
# let r = (NOT ((NOT p) AND q))
# if r then print p

token_map = {
	"let": "LET",
	"if": "IF",
	"then": "THEN",
	"print": "PRINT",
	"T": "TRUE",
	"F": "FALSE",
	"AND": "AND",
	"OR": "OR",
	"NOT": "NOT",
	"IMPLIES": "IMPLIES",
	"=": "EQ",
	"(": "L_PAREN",
	")": "R_PAREN"
}

def process_variable_name(name: str) -> Optional[str]:
	"""Used for mapping variable names to tokens.
	Only single-letter variables are allowed."""
	if len(name) == 1 and name.isalpha():
		return "VAR_" + name.upper()
	else:
		return None

def tokenize(codes: list[str]) -> list[dict]:
	"""Tokenizes the input code lines into a list of dictionaries containing line numbers and tokens.
	If a lexical error is encountered, raise a LexicalError."""
	output = []
	for i, line in enumerate(codes):
		cur = [] # Token list for the current line
		for word in line.split():
			buf = "" # Buffer to hold the current word being processed
			for ch in word:
				if ch in ("(", ")"):
					if buf:
						if buf in token_map:
							cur.append(token_map[buf])
						else:
							var_token = process_variable_name(buf)
							if var_token:
								cur.append(var_token)
							else:
								raise LexicalError(i + 1)
						buf = ""
					cur.append(token_map[ch])
				else:
					buf += ch
			if buf:
				if buf in token_map:
					cur.append(token_map[buf])
				else:
					var_token = process_variable_name(buf)
					if var_token:
						cur.append(var_token)
					else:
						raise LexicalError(i + 1)
		output.append({"line": i+1, "token": cur})
	return output

if __name__ == "__main__":
	codes = [
		"let p = T",
		"let q = F",
		"let r = (NOT ((NOT p) AND q))",
		"if r then print p"
	]
	try:
		result = tokenize(codes)
		for item in result:
			print(item)
	except LexicalError as e:
		print(f"Lexical error at line {e.line}")

# Example output
# {'line': 1, 'token': ['LET', 'VAR_P', 'EQ', 'TRUE']}
# {'line': 2, 'token': ['LET', 'VAR_Q', 'EQ', 'FALSE']}
# {'line': 3, 'token': ['LET', 'VAR_R', 'EQ', 'L_PAREN', 'NOT', 'L_PAREN', 'L_PAREN', 'NOT', 'VAR_P', 'R_PAREN', 'AND', 'VAR_Q', 'R_PAREN', 'R_PAREN']}
# {'line': 4, 'token': ['IF', 'VAR_R', 'THEN', 'PRINT', 'VAR_P']}

# Phase 2: Syntax Validation & AST Generation

# Phase 3: The Optimization Pass

# Phase 4: Verification & Execution





# Compiler
def compile_pipeline(codes: list[str]) -> dict:
    """Runs the entire compilation pipeline on the input code lines."""
    try:
        tokens = tokenize(codes)              # phase_1_lexer
        ast = parse(tokens)                   # phase_2_parser
        optimized_ast = optimize(ast)         # phase_3_optimizer
        outputs = verify_and_execute(optimized_ast)  # phase_4_execution
        return {"result": outputs}
    except CompilerError as e:
        return {
            "error": {
                "phase": e.phase,
                "line": e.line
            }
        }


