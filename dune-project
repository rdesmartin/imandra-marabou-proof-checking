(lang dune 2.2)
(name imandra-marabou)


(dialect
 (name imandra)
 (implementation
  (extension iml)
  (preprocess (system "imandra-extract %{input-file}"))
  (format (system "ocamlformat %{input-file}")))
 (interface (extension "imli")))
