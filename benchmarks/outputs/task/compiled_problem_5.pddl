(define (problem taskAssigment_problem)
(:domain taskAssigment)
(:init
       (developer c)
       (designer d))
(:goal (and (AUX239) (not (incompatible_update))))
)