(define (problem taskAssigment_problem)
(:domain taskAssigment)
(:init
       (designer a)
       (engineer d))
(:goal (and (AUX239) (not (incompatible_update))))
)