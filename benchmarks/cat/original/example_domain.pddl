(define (domain Cat)

(:predicates
	(cat ?x)
	(kitten ?x)
  (animal ?x)
  (mouse ?x)
)

(:action grow_up
  :parameters (?x)
  :precondition (and (animal ?x))
  :effect (when (kitten ?x)
                  (and (not (kitten ?x))))
            )

)

