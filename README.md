# Sentinel Programming Language

Sentinel programming language is a statically typed, compiled programming language designed to lower the language to C, compile to a native executable using the global `cc`. You can change the compiler used to `gcc`, `clang`, anything, by simply editing `compile.sh`. (`compile.ps1` on Windows). 

Windows users, don't worry. You'll never have to look at the source code because I've made `compile.ps1` a CRLF file in the `.gitattributes`. 

## Quick Start

```bash
$ gh repo clone naad1-max/sentinel-compiler
$ cd sentinel-compiler
# On macOS/Linux
$ ./compile.sh examples/test_math_eval.txt
# On Windows
$ .\\compile.ps1 .\\examples\\test_math_eval.txt
# Running the file: universal
$ ./output
```

## To-Do List

* [x] Build a compiler for a small add-subtract language.
* [x] Add multiplication, division and modulus.
* [x] Add printing to the terminal.
* [x] Add exit.
* [x] Add variables.
* [ ] Add if/else if/else/while/for.
* [ ] Add data types.
* [ ] Add type checking.
* [ ] Add functions.
* [ ] Add a mandatory `main` function.
* [ ] Add return.
* [ ] Add string methods.
* [ ] Add classes.
* [ ] Add importing modules: `import <modulename>`
* [ ] Bootstrap a compiler using multiple files and a single build file.
* [ ] Keep adding features (see listing).

### Build a compiler for a small add-subtract language

* [x] Build a lexer.
* [x] Add AST definitions.
* [x] Build a parser.
* [x] Build a code generator that generates the C code.

### Add multiplication, division and modulus

* [x] Modify the lexer to support `*`, `/` and `%`.
* [x] Modify the parser to update the operator precedence.
* [x] Update the code generator to be able to write the new expressions.

### Add printing to the terminal

* [x] Improve the lexer to be able to peek at the next token without advancing the cursor, and add support for string literals, integers and floating points. With this, check if after the `puts` token there are parentheses and if those parentheses contain anything that can be written to standard output.
* [x] Modify the parser to include the new expression and a few new literal types.
* [x] Update the code generator to include the `printf` keyword.

### Add exit

* [x] Modify the lexer to check parentheses after `exit` keyword and use default code `0` or whatever integer is given in the parentheses. Make sure to throw errors if the data type is not recognised. Also make sure that after `exit(<int>)`, there is nothing, otherwise throw an error.
* [x] Modify the parser to include another expression.
* [x] Modify the code generator to include the C keyword for exit.

### Add variables

* [x] Modify the lexer. 
* [x] Modify the parser. 
* [x] Modify the code generator to use the variables.

### Add if/else if/else/while/for

* [ ] Modify the lexer to support the keywords.
* [ ] Modify the parser to include generic `condition, body` blocks and use them to make the mini-AST in the AST.
* [ ] Modify the code generator to produce the loops and control flow.

### Add data types

* [ ] Modify the lexer to support the keywords.
* [ ] Modify the parser to include them in the variable declarations.
* [ ] Simplify the code generator, because no need to infer the type, the user already defines it.

### Add type checking

* [ ] Modify the lexer to add safeguards for the types.

### Add functions

* [ ] Modify the lexer and the parser.
* [ ] Modify the code generator to find the `main` function and define its body using the parser, and then add other functions as necessary.

### Add a mandatory `main` function

* [ ] Simplify the code generator.

### Add return

* [ ] Add the keyword in the lexer, and add a new node in the AST.
* [ ] Modify the code generator to use the integer after `return` keyword instead of default 0.

### Add string methods

* [ ] Build a basic standard library of various methods for different data types.
* [ ] Be able to use the standard library.

### Add classes

* [ ] Modify the lexer to support the new keyword.
* [ ] Modify the parser to have a recursive `body` node.
* [ ] Modify the code generator: have a few pre-codegen things in a runtime so that the code gets easier to generate.

### Add importing modules

* [ ] Modify the lexer to process the imported file into the current file and continue normally.

### Bootstrap the compiler

* [ ] Make sure that there is enough functionality to build a copy of the compiler.
* [ ] Get coding.

### Add new features

* More data type methods.
* Better object oriented programming. 
* Addition of user-defined types and symbols.
* Adding a VSCode extension for Sentinel.
* Adding tooling and a full-on dev environment.
