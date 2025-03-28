open Util
open Iter_map
open Constraint
open Tightening
open Proof_tree
open Result
open Constraint

module JSON_decoder = struct
  module Basic = Decoders_yojson.Basic;;
  module D = Basic.Decode;;

  module M = Iter_map;;

  let int_decoder: Z.t D.decoder =
    let open D in
    let+ i = int in
    Z.of_int i

  let float_decoder: Real.t D.decoder =
    let open D in
    let+ f = float in
    Real.of_float f


  (* Tableau decoder *)

  let sparse_matrix_element_decoder: (int * Real.t) D.decoder =
    let open D in
    let* var = field "var" int_decoder in
    let* value = field "val" float_decoder in
    succeed (var, value)

  let sparse_row_decoder: ((int, Real.t) M.t) D.decoder =
    let open D in
    list_fold_left (fun x ->
        (* pattern match directly here? *)
        let+ el = sparse_matrix_element_decoder in
        el |> (fun (k, v) -> M.add k v x)
      ) M.empty

  let sparse_matrix_decoder (matrix_width: int): ((Real.t list list) D.decoder) =
    let open D in
    list @@ map (M.to_list (matrix_width - (Z.of_int 1))) sparse_row_decoder
  
  (** Constraints decoder *)
 
  (** Constraints decoder *)
  let constraint_type_decoder: constraint_type D.decoder =
    let open D in
    int_decoder >>= (fun x -> succeed @@ Constraint.constraint_type_of_int x)

  let constraint_decoder: Constraint.t D.decoder =
    let open D in
    let* t = field "constraintType" int_decoder in
    let* vars = field "vars" (list int_decoder) in
    match (Constraint.parse_constraint t vars) with
      | Some c -> succeed c 
      | None -> fail "Parsing error: unknown constraint type"

  (* let constraint_decoder: Constraint.t_old D.decoder =
    let open D in
    let* t = field "constraintType" constraint_type_decoder in
    let* vars = field "vars" (list int_decoder) in
    succeed (t, vars) *)

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

  let split_decoder: Tightening.t D.decoder =
    let open D in
    let* var = field "var" int_decoder in
    let* value = field "val" float_decoder in
    let* bound_type = field "bound" bound_decoder in
    succeed (var, value, bound_type)

  let explanation_decoder (proof_size: int): Real.t list D.decoder =
    let open D in
    map (M.to_list (proof_size - (Z.of_int 1))) sparse_row_decoder
 
  let rec proof_node_decoder (proof_size: int): Proof_tree.MT.t D.decoder =
    let open D in
    (* fix (fun proof_node_decoder -> *)
        one_of [
          ( "node",
            let* splits = field "split" (list split_decoder) in
            let* children = field "children" (list (proof_node_decoder proof_size)) in
            let left_child = List.hd children in
            let right_child = List.hd (List.tl children) in
            succeed (Proof_tree.MT.Node (splits, left_child, right_child))
          );
          ( "leaf",
            let* splits = field "split" (list split_decoder) in
            let* contradiction = field "contradiction" (explanation_decoder proof_size) in
            succeed (Proof_tree.MT.Leaf (splits, contradiction))
          )
        ]
      (* ) *)

let proof_root_decoder (proof_size: int): Proof_tree.MT.t D.decoder =
    let open D in
    one_of [
      ( "node",
        let* children = field "children" (list (proof_node_decoder proof_size)) in
        succeed (Proof_tree.MT.Node ([], List.hd children, List.hd (List.tl children)))
      );
      ( "leaf",
        let* contradiction = field "contradiction" (explanation_decoder proof_size) in
        succeed (Proof_tree.MT.Leaf ([], contradiction))
      )
    ]

  (* Top-level decoder *)
  let proof_decoder : ('a D.decoder) =
    let open D in
    let* upper_bounds = field "upperBounds" @@ list (map Real.of_float float) in
    let* lower_bounds = field "lowerBounds" @@ list (map Real.of_float float) in
    let* tableau_width = succeed @@ List.length upper_bounds in
    let* tableau = field "tableau" (sparse_matrix_decoder tableau_width) in
    let* proof_size = succeed @@ List.length tableau in
    let* constraints = field "constraints" (list constraint_decoder) in
    let* proof_tree = field "proof" (proof_root_decoder proof_size) in
    succeed (tableau, upper_bounds, lower_bounds, constraints, proof_tree)

  let decode_proof_file file_name= D.decode_file proof_decoder file_name 
  [@@program]

  let decode_proof_file_refl file_name = 
    match D.decode_file proof_decoder file_name with
    | Ok res -> Ok res
    | Error e -> Error e
  [@@program]

end 
[@@program]