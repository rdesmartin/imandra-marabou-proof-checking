# Run the proof checker in Imandra

Start Imandra repl:

```
$ imandra core repl
```
import necessary files
```
# use "proof_checker/imports.iml";;
```

## Run in program mode

Define the proof you want to use in `main_program.iml` then import the file:

```ocaml
(* in proof_checker/main_program.iml *)
let current_proof = tiny2
```

```
# use "proof_checker/main_program.iml";;
```

## Run in logic mode

It is currently not possible to run the proof checking algorithm on a specific proof in logic mode(error at the `[@@reflect]` command).
However, it is not important as proof checking should never be conducted in logic mode; we want to reason about the checking algorithm in general, not about checking a specific proof.

# Verification
Start Imandra repl:

```
$ imandra core repl
```
import necessary files
```
# use "proof_checker/imports.iml";;
```

Import relevant verification file:
```
# use "verification/contradiction_verification.iml";;
```


# OCaml extraction
It is possible to extract and run OCaml code using the dune build system:

From the project's root directory:
```
$ dune build ./proof_checker/main_program.exe
```
```
$ dune exec -- ./main_program.exe ./json/tinyJsonProof2.json
```

