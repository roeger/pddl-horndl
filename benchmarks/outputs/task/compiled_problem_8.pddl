(define (problem taskAssigment_problem)
(:domain taskAssigment)
(:init
       (engineer a)
       (designer f)
       (engineer g)
       (engineer h))
(:goal (and (AUX239) (not (incompatible_update))))
)