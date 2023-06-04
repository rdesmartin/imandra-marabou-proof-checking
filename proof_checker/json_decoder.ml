open Iter_map
open Utils
open Constraint
open Split
open Bound_lemma
open Proof_tree
open Result

module JSON_decoder = struct
  module Basic = Decoders_yojson.Basic;;
  module D = Basic.Decode;;

  module M = Iter_map;;

  let int_decoder: Z.t D.decoder =
    let open D in
    let+ i = int in
    Z.of_int i

  let float_decoder: Q.t D.decoder =
    let open D in
    let+ f = float in
    Q.of_float f


  (* Tableau decoder *)

  let sparse_matrix_element_decoder: (int * real) D.decoder =
    let open D in
    let* var = field "var" int_decoder in
    let* value = field "val" float_decoder in
    succeed (var, value)

  let sparse_row_decoder: ((int, real) M.t) D.decoder =
    let open D in
    list_fold_left (fun x ->
        (* pattern match directly here? *)
        let+ el = sparse_matrix_element_decoder in
        el |> (fun (k, v) -> M.add k v x)
      ) M.empty

  let sparse_matrix_decoder (matrix_width: int): ((real list list) D.decoder) =
    let open D in
    list @@ map (M.to_list (matrix_width - (Z.of_int 1))) sparse_row_decoder
  (* Constraints decoder *)

  let constraint_type_decoder: constraint_type D.decoder =
    let open D in
    int_decoder >>= (fun x -> succeed @@ Constraint.constraint_type_of_int x)

  let constraint_decoder: Constraint.t D.decoder =
    let open D in
    let* t = field "constraintType" constraint_type_decoder in
    let* vars = field "vars" (list int_decoder) in
    succeed (t, vars)

  let constraints_decoder: (Constraint.t list) D.decoder =
    let open D in
    list constraint_decoder

  (* Proof Tree decoder *)
  let bound_decoder: bound_type D.decoder =
    let open D in
    string >>= (function
        | "U" -> succeed UPPER
        | "L" -> succeed LOWER
        | _ -> fail "invalid bound type"
      )

  let split_decoder: Split.t D.decoder =
    let open D in
    let* var = field "var" int_decoder in
    let* value = field "val" float_decoder in
    let* bound_type = field "bound" bound_decoder in
    succeed (var, value, bound_type)

  let lemma_decoder: BoundLemma.t D.decoder =
    let open D in
    one_of [
      ( "full_lemma",
        let* aff_var = field "affVar" int_decoder in
        let* aff_bound = field "affBound" bound_decoder in
        let* bound = field "bound" float_decoder in
        let* caus_var = field "causVar" int_decoder in
        let* caus_bound = field "causBound" bound_decoder in
        let* constrnt = field "constraint" constraint_type_decoder in
        let* expl = field "expl" (list float_decoder) in
        succeed @@ BoundLemma.Full (aff_var, aff_bound, bound, caus_var, caus_bound, constrnt, expl)
      );
      ( "short_lemma",
        let* aff_var = field "affVar" int_decoder in
        let* aff_bound = field "affBound" bound_decoder in
        let* bound = field "bound" float_decoder in
        succeed @@ BoundLemma.Short (aff_var, aff_bound, bound)
      )
    ]

  let proof_node_decoder: ProofTree.t D.decoder =
    let open D in
    fix (fun proof_node_decoder ->
        one_of [
          ( "node",
            let* splits = field "split" (list split_decoder) in
            let* lemmas = field_opt_or ~default:[] "lemmas" (list lemma_decoder) in
            let* children = field "children" (list proof_node_decoder) in
            succeed (ProofTree.Node (splits, lemmas, children))
          );
          ( "leaf",
            let* splits = field "split" (list split_decoder) in
            let* lemmas = field_opt_or ~default:[] "lemmas" (list lemma_decoder) in
            let* contradiction = field "contradiction" (list float_decoder) in
            succeed (ProofTree.Leaf (splits, lemmas, contradiction))
          )
        ]
      )

  let proof_root_decoder: ProofTree.t D.decoder =
    let open D in
    one_of [
      ( "node",
        let* lemmas = field_opt_or ~default:[] "lemmas" (list lemma_decoder) in
        let* children = field "children" (list proof_node_decoder) in
        succeed (ProofTree.Node ([], lemmas, children))
      );
      ( "leaf",
        let* lemmas = field_opt_or ~default:[] "lemmas" (list lemma_decoder) in
        let* contradiction = field "contradiction" (list float_decoder) in
        succeed (ProofTree.Leaf ([], lemmas, contradiction))
      )
    ]

  (* Top-level decoder *)

  let proof_decoder : ('a D.decoder) =
    let open D in
    let* upper_bounds = field "upperBounds" @@ list (map Q.of_float float) in
    let* lower_bounds = field "lowerBounds" @@ list (map Q.of_float float) in
    let* tableau_width = succeed @@ List.length upper_bounds in
    let* tableau = field "tableau" (sparse_matrix_decoder tableau_width) in
    let* constraints = field "constraints" (list constraint_decoder) in
    let* proof_tree = field "proof" proof_root_decoder in
    succeed (tableau, upper_bounds, lower_bounds, constraints, proof_tree)

  let decode_proof_file file_name= D.decode_file proof_decoder file_name 
  [@@program]

  let decode_proof_file_refl file_name = 
    match D.decode_file proof_decoder file_name with
    | Ok res -> Result.return res
    | Error e -> Result.fail @@ "error"
  [@@program]

end 
[@@program]