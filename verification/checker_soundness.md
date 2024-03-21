1. lemma check_node_soundness (tableau: real list list) (upper_bounds: real list) (lower_bounds: real list) 
        (relu_constraints: Constraint.t list) (proof_tree: ProofTree.t) (x: real list) =
    check_node (mk_eq_constraints tableau) upper_bounds lower_bounds relu_constraints proof_tree
    ==>
    unsat tableau upper_bounds lower_bounds relu_constraints x

Induction over the proof tree:
1.a. axiom Leaf case, proof_tree = Leaf contradiction: axiom soundness_leaf tableau upper_bounds lower_bounds relu_constraints x (Leaf contradiction):
        check_node (mk_eq_constraints tableau) upper_bounds lower_bounds relu_constraints (Leaf contradiction)
        ==> 
        unsat tableau upper_bounds lower_bounds relu_constraints x

1.b. lemma Node case, proof_tree = Node (left_child, right_child) 
lemma soundness_node tableau upper_bounds lower_bounds relu_constraints x (Node (left_child, right_child))
        check_node (mk_eq_constraints tableau) upper_bounds lower_bounds relu_constraints (Node (left_child, right_child))
        ==>
        not (sat tableau upper_bounds lower_bounds relu_constraints x)
<!-- todo: ensure that not sat = unsat -->
Inductive hypothesis: soundness_node holds for left_child and right_child. i.e.
let (_, ub_left, lb_left) = update_child_bounds left tableau upper_bounds lower_bounds constraints,
let (_, ub_right, lb_right) = update_child_bounds right tableau upper_bounds lower_bounds constraints in

check_node (mk_eq_constraints tableau) ub_left lb_left relu_constraints left_child.ptr
==>
not (sat tableau ub_left lb_left relu_constraints x)

and

check_node (mk_eq_constraints tableau) ub_right lb_right relu_constraints left_child.ptr
==>
not (sat tableau ub_right lb_right relu_constraints x)



Prove 1.b. by contrapositive:
        sat tableau upper_bounds lower_bounds relu_constraints x 
        ==>
        not (check_node (mk_eq_constraints tableau) upper_bounds lower_bounds relu_constraints (Node (left_child, right_child)))


let valid_children_splits = check_children_splits left.tightenings right.tightenings constraints in
let (valid_bounds_l, ub_left, lb_left) = update_child_bounds left tableau upper_bounds lower_bounds constraints in
let (valid_bounds_r, ub_right, lb_right) = update_child_bounds right tableau upper_bounds lower_bounds constraints in
<!-- assuming that the parent's system is satisfiable -->
sat tableau upper_bounds lower_bounds relu_constraints x && 
<!-- that the bound tightenings are valid (todo: prove that bound tightening preserve satisfiability) -->
valid_bounds_l && valid_bounds_r && 
<!-- and that the split between the children is correct, -->
valid_children_splits
==>
<!-- then one of the children's systems is satisfiable too -->
sat tableau ub_left lb_left relu_constraints x ||
sat tableau ub_right lb_right relu_constraints x

<!-- Inductive hypothesis that sat child_left && sat child_right ==> sat Node(child_left, child_right)  -->
sat tableau ub_left lb_left relu_constraints x ||
sat tableau ub_right lb_right relu_constraints x
==>
not (check_node tableau ub_left lb_left constraints left.ptr) ||
not (check_node tableau ub_right lb_right constraints right.ptr)
        
