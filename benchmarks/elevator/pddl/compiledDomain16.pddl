(define (domain elevators)
(:constants
  pass_m pass_a pass_n pass_l pass_e pass_b c d f g h i j k o p - object)
(:predicates
  (passenger ?p - object)
  (boarded ?p - object)
  (served ?p - object)
  (floor ?p - object)
  (origin ?p ?f - object)
  (destin ?p ?f - object)
  (liftat ?f - object)
  (next ?f1 ?f2 - object)
  (AUX0 ?x - object))
(:derived (AUX0 ?x - object)
          (or (served ?x) (not (passenger ?x))))
(:action stop
  :parameters (?p ?f - object)
  :precondition (and (liftat ?f) (passenger ?p))
  :effect (and (when (and (origin ?p ?f) (not (boarded ?p)) (not (served ?p))) (boarded ?p)) (when (or ) (and (served ?p) (not (boarded ?p))))))
(:action moveUp
  :parameters (?f1 ?f2 - object)
  :precondition (and (liftat ?f1) (next ?f1 ?f2))
  :effect (when (and (liftat ?f1) (not (= ?f1 ?f2))) (and (liftat ?f2) (not (liftat ?f1)))))
(:action moveDown
  :parameters (?f1 ?f2 - object)
  :precondition (and (liftat ?f1) (next ?f2 ?f1))
  :effect (when (and (liftat ?f1) (not (= ?f1 ?f2))) (and (liftat ?f2) (not (liftat ?f1)))))
)