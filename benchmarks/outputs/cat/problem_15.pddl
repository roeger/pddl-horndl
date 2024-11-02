(define (problem BTcat_problem)
(:domain BTcat)
(:init
       (cat ac)
       (contains ao ac)
       )
(:goal (and (forall (?x - object) (or (disarmed ?x) (not (DATALOG_PACKAGE ?x))))))
)
