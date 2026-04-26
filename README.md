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

---

## 4. Example input & output

**input.txt**:
```
let p = T
let q = F
let r = (NOT ((NOT p) AND q))
if r then print p
```

**output.json**:
```
{
  "phase_1_lexer": [
    {
      "line": 1,
      "token": [
        "LET",
        "VAR_P",
        "EQ",
        "TRUE"
      ]
    },
    {
      "line": 2,
      "token": [
        "LET",
        "VAR_Q",
        "EQ",
        "FALSE"
      ]
    },
    {
      "line": 3,
      "token": [
        "LET",
        "VAR_R",
        "EQ",
        "L_PAREN",
        "NOT",
        "L_PAREN",
        "L_PAREN",
        "NOT",
        "VAR_P",
        "R_PAREN",
        "AND",
        "VAR_Q",
        "R_PAREN",
        "R_PAREN"
      ]
    },
    {
      "line": 4,
      "token": [
        "IF",
        "VAR_R",
        "THEN",
        "PRINT",
        "VAR_P"
      ]
    }
  ],
  "phase_2_parser": [
    {
      "line": 1,
      "ast": [
        "LET",
        "VAR_P",
        "TRUE"
      ]
    },
    {
      "line": 2,
      "ast": [
        "LET",
        "VAR_Q",
        "FALSE"
      ]
    },
    {
      "line": 3,
      "ast": [
        "LET",
        "VAR_R",
        [
          "NOT",
          [
            "AND",
            [
              "NOT",
              "VAR_P"
            ],
            "VAR_Q"
          ]
        ]
      ]
    },
    {
      "line": 4,
      "ast": [
        "IF",
        "VAR_R",
        [
          "PRINT",
          "VAR_P"
        ]
      ]
    }
  ],
  "phase_3_optimizer": [
    {
      "line": 1,
      "ast": [
        "LET",
        "VAR_P",
        "TRUE"
      ]
    },
    {
      "line": 2,
      "ast": [
        "LET",
        "VAR_Q",
        "FALSE"
      ]
    },
    {
      "line": 3,
      "ast": [
        "LET",
        "VAR_R",
        [
          "OR",
          "VAR_P",
          [
            "NOT",
            "VAR_Q"
          ]
        ]
      ]
    },
    {
      "line": 4,
      "ast": [
        "IF",
        "VAR_R",
        [
          "PRINT",
          "VAR_P"
        ]
      ]
    }
  ],
  "phase_4_execution": {
    "verifications": [
      {
        "line": 3,
        "variables_tested": [
          "VAR_P",
          "VAR_Q"
        ],
        "ast_original_column": [
          "TRUE",
          "TRUE",
          "FALSE",
          "TRUE"
        ],
        "ast_optimized_column": [
          "TRUE",
          "TRUE",
          "FALSE",
          "TRUE"
        ],
        "is_equivalent": "TRUE"
      }
    ],
    "final_state_dictionary": {
      "VAR_P": "TRUE",
      "VAR_Q": "FALSE",
      "VAR_R": "TRUE"
    },
    "printed_output": [
      {
        "line": 4,
        "output": "TRUE"
      }
    ]
  }
}
```