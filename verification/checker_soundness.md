1. lemma check_node_soundness (tableau: real list list) (upper_bounds: real list) (lower_bounds: real list) 
        (relu_constraints: Constraint.t list) (proof_tree: ProofTree.t) =
    check_node (mk_eq_constraints tableau) upper_bounds lower_bounds relu_constraints proof_tree
    ==>
    for all x, unsat tableau upper_bounds lower_bounds relu_constraints x

Induction over the proof tree:
1.a. axiom Leaf case, proof_tree = Leaf contradiction: axiom soundness_leaf tableau upper_bounds lower_bounds relu_constraints (Leaf contradiction):
        check_node (mk_eq_constraints tableau) upper_bounds lower_bounds relu_constraints (Leaf contradiction)
        ==> 
        for all x, unsat tableau upper_bounds lower_bounds relu_constraints x

1.b. lemma Node case, proof_tree = Node (left_child, right_child) 
lemma soundness_node tableau upper_bounds lower_bounds relu_constraints (Node (left_child, right_child))
        check_node (mk_eq_constraints tableau) upper_bounds lower_bounds relu_constraints (Node (left_child, right_child))
        ==>
        for all x, unsat tableau upper_bounds lower_bounds relu_constraints x
<!-- todo: ensure that not sat = unsat -->


Inductive hypothesis: soundness_node holds for left_child and right_child. i.e.
<!-- ub_left, lb_left, ub_right, lb_right are a valid split because if not valid split, check_node (Node (left_child, right_child)) = false -->
check_node (mk_eq_constraints tableau) ub_left lb_left relu_constraints left_child.ptr
==>
for all x, unsat tableau ub_left lb_left relu_constraints x

and

check_node (mk_eq_constraints tableau) ub_right lb_right relu_constraints left_child.ptr
==>
for all x, unsat tableau ub_right lb_right relu_constraints x



Prove 1.b. by contrapositive and the IH:
        there exists x s.t. sat tableau upper_bounds lower_bounds relu_constraints x 
        ==>
        not (check_node (mk_eq_constraints tableau) upper_bounds lower_bounds relu_constraints (Node (left_child, right_child)))


<!-- unfolding the previous VG -->
let valid_children_splits = check_children_splits left.tightenings right.tightenings constraints in
let (valid_bounds_l, ub_left, lb_left) = update_child_bounds left tableau upper_bounds lower_bounds constraints in
let (valid_bounds_r, ub_right, lb_right) = update_child_bounds right tableau upper_bounds lower_bounds constraints in
<!-- assuming that the parent's system is satisfiable -->
(there exists x s.t. sat tableau upper_bounds lower_bounds relu_constraints x) && 
<!-- that the bound tightenings are valid (todo: prove that bound tightening preserve satisfiability) -->
valid_bounds_l && valid_bounds_r &&
<!-- and that the split between the children is correct, -->
valid_children_splits
==>
<!-- then one of the children's systems is satisfiable too -->
not (check_node tableau ub_left lb_left constraints left.ptr) ||
not (check_node tableau ub_right lb_right constraints right.ptr)


by the IH this is equivalent to 
<!-- Inductive hypothesis that sat child_left && sat child_right ==> sat Node(child_left, child_right)  -->

let valid_children_splits = check_children_splits left.tightenings right.tightenings constraints in
let (valid_bounds_l, ub_left, lb_left) = update_child_bounds left tableau upper_bounds lower_bounds constraints in
let (valid_bounds_r, ub_right, lb_right) = update_child_bounds right tableau upper_bounds lower_bounds constraints in
<!-- assuming that the parent's system is satisfiable -->
(there exists x s.t. sat tableau upper_bounds lower_bounds relu_constraints x) && 
<!-- that the bound tightenings are valid (todo: prove that bound tightening preserve satisfiability) -->
valid_bounds_l && valid_bounds_r &&
<!-- and that the split between the children is correct, -->
valid_children_splits
==>
<!-- then one of the children's systems is satisfiable too -->
(there exists x s.t. sat tableau ub_left lb_left relu_constraints x) ||
(there exists x s.t. sat tableau ub_right lb_right relu_constraints x)

let sat tableau upper_bounds lower_bounds relu_constraints x =
    (is_in_kernel tableau x &&
    is_bounded upper_bounds lower_bounds x &&
    check_relu_constraints relu_constraints x)


let valid_children_splits = check_children_splits left.tightenings right.tightenings constraints
let (ub_left, lb_left) = Tightening.update_bounds left.tightening upper_bounds lower_bounds in
let (ub_right, lb_right) = Tightening.update_bounds right.tightening upper_bounds lower_bounds in
(there exists x s.t. sat tableau upper_bounds lower_bounds relu_constraints x) && 
valid_children_splits
==>
(there exists x s.t. sat tableau ub_left lb_left relu_constraints x) ||
(there exists x s.t. sat tableau ub_right lb_right relu_constraints x)

let update_child_bounds (child_info: ProofTree.child_info) tableau upper_bounds lower_bounds constraints =
    let (ub', lb') = Tightening.update_bounds child_info.tightenings upper_bounds lower_bounds in
    let (valid_bounds, ub'', lb'') = BoundLemma.check_bound_lemmas child_info.bound_lemmas tableau ub' lb' constraints in
    (valid_bounds, ub'', lb'')
<!-- sat tableau ub' lb' constraints x ==> sat tableau ub'' lb'' constraints x  -->

