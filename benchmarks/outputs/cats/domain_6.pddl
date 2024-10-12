(define (domain BTcat)
(:constants
  a b c d e f g h i j k l - object)
(:predicates
  (cat ?x - object)
  (bomb ?x - object)
  (contains ?x ?y - object)
  (package ?x - object)
  (disarmed ?x - object)
  (object ?x - object))
(:action dunk
  :parameters (?x ?y - object)
  :precondition (package ?x)
  :effect (when (or ) (and (disarmed ?x))))
(:action let_the_cats_out
  :parameters (?x ?y - object)
  :precondition (package ?x)
  :effect (when (contains ?x ?y) (and (not (contains ?x ?y)) (cat ?y))))
)