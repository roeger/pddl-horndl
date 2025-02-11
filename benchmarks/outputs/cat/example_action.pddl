(:action update
  :parameters ()
  :precondition (and (updating) (not (incompatible_update)))
  :effect (forall (?x)
  (and
      (when (ins_cat ?x) (cat ?x))
      (when (del_cat ?x) (not (cat ?x)))
      (when (ins_cat_request ?x) (not (ins_cat_request ?x)))
      (when (del_cat_request ?x) (not (del_cat_request ?x)))
  ...
  ))
)

