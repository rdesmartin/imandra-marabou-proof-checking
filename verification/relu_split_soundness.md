lemma soundness_valid_relu_var_split tableau upper_bounds lower_bounds constraints x
If:
    * there exists x s.t. x satisfies (tableau, ubs, lbs),
    * C is a valid relu constraint,
    * (ubs', lbs') and (ubs'', lbs'') correspond to the active and inactive phases of C
Then:
    * x satisfies either (tableau, ubs', lbs') or (tableau, ubs'', lbs'')

lemma soundness_valid_relu_var_split tableau upper_bounds lower_bounds constraints x 
        left_tightening right_tightening =
    let (ubs', lbs') = update_bounds left_tightening upper_bounds lower_bounds in
    let (ubs'', lb'') = update_bound right_tightening upper_bounds lower_bounds in
    check_relu_split left_tightening right_tightening constraints &&
    sat tableau upper_bounds lower_bounds constraints x
    ==>
    sat tableau ub_left lb_left constraints x ||
    sat tableau ub_right lb_right constraints x

We prove it by 
