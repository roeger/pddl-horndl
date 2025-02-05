(define (domain KitCat)

(:predicates
	(cat ?x)
	(kitten ?x)
  (animal ?x)
  (mouse ?x)
)

(:action grow_up
  :parameters (?x)
  :precondition (kitten ?x)
  :effect (when (kitten ?x)
                  (and (not (kitten ?x))))
            )

)

