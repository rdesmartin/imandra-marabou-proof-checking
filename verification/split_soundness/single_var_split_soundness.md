Lemma 1: soundness_valid_single_var_split tableau upper_bounds lower_bounds constraints x 
        tightening_left tightening_right =
    let (ub_left, lb_left) = update_bounds tightening_left upper_bounds lower_bounds in
    let (ub_right, lb_right) = update_bounds tightening_right upper_bounds lower_bounds in
    check_single_var_split tightening_left tightening_right &&
    sat tableau upper_bounds lower_bounds constraints x
    ==>
    sat tableau ub_left lb_left constraints x ||
    sat tableau ub_right lb_right constraints x

(relu constraints don't change so we can ignore them)

We proved that SAT in the tableau world implies SAT in poly systems world:
sat tableau upper_bounds lower_bounds constraints x
==>
eval_system (mk_system tableau, ub, lb) x

We now prove Lemma 2:
Soundness of SV split in the poly system world  
eval_system (mk_system tableau, ub, lb) x
==>
eval_system (mk_system tableau ub_left lb_left) || eval_system (mk_system tableau ub_right lb_right)

Lemma 2.1.: Completeness of SV split at expression level
By previouly proven arithmetic lemmas,
for all x, a, c: eval_exp (Geq -a c) x || eval_exp (Geq a -c) x

Lemma 2.2.: General property of evaluation and concatenation/insertion
(eval_exp e1 x || eval_exp e2 x) &&
eval_system s x
==> 
eval_system (concat s e1) x || eval_system (concat s e2) x 

Lemma 2.3: Prove soundness of splits in general poly system setting 
by L2.1. and L2.2:
eval_system (mk_system tableau, ub, lb) x
==>
eval_system (concat (mk_system tableau ub lb) (Geq -a c)) x || 
    eval_system (concat (mk_system tableau ub lb) (Geq a -c)) x

Lemma 2.4.: Link update_bounds function and expression of updated bounds in L2.3 
** Hard part, might need to redefine update_bounds to act on a single bound (i.e. update_upper_bounds, update_lower_bounds) **
by recursion on update_bounds and definition of single_var_split,
let (ub_left, lb_left) = update_bounds tightening_left upper_bounds lower_bounds in
let (ub_right, lb_right) = update_bounds tightening_right upper_bounds lower_bounds in
check_single_var_split tightening_left tightening_right &&
==>
eval_system (mk_system tableau ub_left lb_left) x = 
    eval_system (concat (mk_system tableau ub lb) (Geq -a c)) x

alternatively:
eval_system (mk_system tableau ub_right lb_right) x = 
    eval_system (concat (mk_system tableau ub lb) (Geq a -c)) x

In other words:
mk_geq_constraints lb[lb_i := c] = (mk_geq_constraints lb)[ith constraint := mk_geq_constraint i -c]
proof by recursion on

Lemma 3: Conversion back from poly systems to tableaus  
By L3.1
eval_system (mk_system tableau ub_left lb_left) x || eval_system (mk_system tableau ub_right lb_right) x
==>
sat tableau ub_left lb_left constraints x ||
sat tableau ub_right lb_right constraints x

Lemma 3.1: What we proved earlier
eval_system (mk_system tableau, ub, lb) x
==>
sat tableau upper_bounds lower_bounds constraints x
