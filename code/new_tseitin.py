#!/usr/bin/env python

import argparse

import pddl
from update_runner import Timer

AUX_PREDICATE_NAME = "AUX"

class Tseitin:
    def __init__(self,
                 domain,
                 problem):
        self.domain = domain
        self.problem = problem

    def __call__(self):
        with Timer("tseitin_transformation", file=args.output_csv):
            self._derived_predicates_count = 0
            self._new_derived_predicates = []
            self._create_shortcuts_conditions()
            # self._replace_subformulas()
            self.domain.derived_predicates.extend(self._new_derived_predicates)

    def _create_shortcuts_conditions(self):
        for deriv in self.domain.derived_predicates:
            formula = deriv.condition
            par = deriv.predicate.parameters
            self._create_shortcuts_and_apply_to_formula(formula, par)

    def _create_shortcuts_and_apply_to_formula(self, formula, par):
        if isinstance(formula, (pddl.Exists, pddl.Or)):
            shortcuts = self._create_shortcuts_disjunction(formula, par)
            self._apply_shortcuts_to_formula(formula, shortcuts)
        if isinstance(formula, (pddl.Forall, pddl.And)):
            shortcuts = self._create_shortcuts_conjunction(formula, par)
            self._apply_shortcuts_to_formula(formula, shortcuts)

    def _create_shortcuts_disjunction(self, formula, par):
        pass

    def _create_shortcuts_conjunction(self, formula, par):
        pass


    def print_information(self):
        print("%% Tseitin transformation for PDDL using derived predicates")
        print("")
        if len(self._new_derived_predicates) > 0:
            print("%% NEW DERIVED PREDICATES:")
            for dp in self._new_derived_predicates:
                print("%% %s" % dp)
            print("")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("domain")
    p.add_argument("problem")
    p.add_argument("--out-domain", "-d", default="domain.pddl")
    p.add_argument("--out-problem", "-p", default="problem.pddl")
    p.add_argument("--verbose", "-v", default=False, action='store_true')
    p.add_argument("--keep-name", "-n", default=False, action='store_true')
    p.add_argument("--output-csv", default="results.csv")
    p.add_argument("--benchmark-name", default="test 1")

    args = p.parse_args()
    preserve_names = args.keep_name
    with open(args.domain) as f:
        d = pddl.parse_domain(f.read(), preserve_predicate_names=preserve_names)
    with open(args.problem) as f:
        p = pddl.parse_problem(f.read())
    tseitin = Tseitin(d, p)
    tseitin()
    with open(args.out_domain, "w") as f:
        f.write(str(d))
    with open(args.out_problem, "w") as f:
        f.write(str(p))
    if args.verbose:
        tseitin.print_information()
