(define (problem KitCat_problem)
(:domain KitCat)
(:init
       (animal hanzo)
       (animal genji)
       (kitten hanzo)
       (kitten genji))
(:goal (and (forall (?x - object) (not (kitten ?x))) (not (incompatible_update))))
)