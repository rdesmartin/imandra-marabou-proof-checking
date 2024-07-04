Lemma 1: soundness_valid_single_var_split tableau upper_bounds lower_bounds constraints x 
        tightening_left tightening_right =
    let (ub_left, lb_left) = update_bounds tightening_left upper_bounds lower_bounds in
    let (ub_right, lb_right) = update_bounds tightening_right upper_bounds lower_bounds in
    check_single_var_split tightening_left tightening_right &&
    sat tableau upper_bounds lower_bounds constraints x
    ==>
    sat tableau ub_left lb_left constraints x ||
    sat tableau ub_right lb_right constraints x

We proved that:
sat tableau upper_bounds lower_bounds constraints x
==>
eval_system (mk_system tableau, ub, lb) x

We now try to prove Lemma 2:
eval_system (mk_system tableau, ub, lb) x
==>
eval_system (mk_system tableau ub_left lb_left) || eval_system (mk_system tableau ub_right lb_right) 

Lemma 2.1.: by previouly proven arithmetic lemmas,
for all x, a, c: eval_exp (Geq -a c) x || eval_exp (Geq a -c) x

Lemma 2.2.: by previously proven lemmas about eval_system, 
(eval_exp e1 x || eval_exp e2 x) &&
eval_system s x
==> 
eval_system (e1 :: s) || eval_system (e2 :: s) 

Lemma 2.3: by L2.1. and L2.2:
eval_system (mk_system tableau, ub, lb) x
==>
eval_system ((Geq -a c)::(mk_system tableau ub lb)) || eval_system ((Geq a -c) :: (mk_system tableau ub lb))

Lemma 2.4.: By ??
eval_system ((Geq -a c)::(mk_system tableau ub' lb')) x || eval_system ((Geq a -c) :: (mk_system tableau ub'' lb'')) x
==>
eval_system (mk_system tableau ub_left lb_left) x || eval_system (mk_system tableau ub_right lb_right) x

Lemma 2.4.1: can we prove that? This would allow us to prove 2.4.
eval_system (mk_system tableau, ub, lb) x
==>
sat tableau upper_bounds lower_bounds constraints x

Lemma 3: By ???
eval_system (mk_system tableau ub_left lb_left) x || eval_system (mk_system tableau ub_right lb_right) x
==>
sat tableau ub_left lb_left constraints x ||
sat tableau ub_right lb_right constraints x


