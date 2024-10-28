from planning.logic import Predicate, Fact, Not, And, DelEffect, AddEffect, Action, ConjunctiveEffect, ConditionalEffect

from coherence_update.rules.symbols import INCOMPATIBLE_UPDATE_STR, ACTION_UPDATE_NAME, UPDATE_STR, ADD_PREFIX_STR, DEL_PREFIX_STR, SUFFIX

class Domain:
    def __init__(self):
        self.name = None
        self.requirements = None
        self.types = None
        self.constants = None
        self.predicates = None
        self.functions = None
        self.actions = None
        self.derived_predicates = None

    def __str__(self):
        res = ["(define (domain %s)" % self.name]
        if self.requirements != None:
            res.append("(:requirements %s)" % " ".join(self.requirements))
        if self.types != None:
            res.append("(:types")
            for tl in self.types:
                res.append("  " + str(tl))
            res[-1] += ")"
        if self.constants != None:
            res.append("(:constants")
            for tl in self.constants:
                res.append("  " + str(tl))
            res[-1] += ")"
        if self.predicates != None:
            res.append("(:predicates")
            for p in self.predicates:
                res.append("  " + str(p))
            res[-1] += ")"
        if self.functions != None:
            res.append("(:functions")
            for p in self.functions:
                res.append("  " + str(p))
            res[-1] += ")"
        if self.derived_predicates != None:
            res.extend([str(d) for d in self.derived_predicates])
        if self.actions != None:
            res.extend([str(a) for a in self.actions])
        res.append(")")
        return "\n".join(res)

    def get_type_relation(self):
        type_relation = {}
        if self.types != None:
            for tl in self.types:
                for t in tl.elements:
                    type_relation[t] = tl.type
        closure = {"object": ["object"]}
        for t in type_relation:
            closure[t] = [t]
            st = type_relation[t]
            while True:
                closure[t].append(st)
                if st == "object":
                    break
                assert st in type_relation
                st = type_relation[st]
        return closure

    def get_type_to_constant_map(self, type_relation):
        constants = { t: list() for t in type_relation.keys() }
        constants["object"] = list()
        if self.constants != None:
            for tl in self.constants:
                for super_type in type_relation.get(tl.type, []):
                    constants[super_type].extend(tl.elements)
        return constants

    def extend_for_coherence_update(self):
        def adjust_for_add(fact):
            predicate = fact.predicate
            new_predicate = ADD_PREFIX_STR + predicate + SUFFIX
            fact.predicate = new_predicate
        def adjust_for_del(fact):
            predicate = fact.predicate
            new_predicate = DEL_PREFIX_STR + predicate + SUFFIX
            fact.predicate = new_predicate
        def wrapper(eff):
            if isinstance(eff, AddEffect):
                fn = adjust_for_add
                f = eff.fact
                f.apply(Fact, fn)
            elif isinstance(eff, DelEffect):
                fn = adjust_for_del
                f = eff.fact
                f.apply(Fact, fn)
            elif isinstance(eff, ConditionalEffect):
                wrapper(eff.effect)
            elif isinstance(eff, ConjunctiveEffect):
                for e in eff.elements:
                    wrapper(e)
            else:
                raise ValueError("Unknown effect type: %r" % eff)

        # Adjust actions
        for action in self.actions:
            # Change precondition
            pre = action.precondition
            not_updating = Not(Fact(UPDATE_STR))
            new_pre = And([pre, not_updating])
            action.precondition = new_pre
            # Change effect
            effekt = action.effect
            wrapper(effekt)

        # Construct update action
        a = Action(ACTION_UPDATE_NAME)
        a.parameters = []
        updating = Fact(UPDATE_STR)
        compatible_update = Not(Fact(INCOMPATIBLE_UPDATE_STR))
        a.precondition = And([updating, compatible_update])
        elements = []
        new_preds =[Predicate(UPDATE_STR, []), Predicate(INCOMPATIBLE_UPDATE_STR, [])]
        for predicate in self.predicates:
            # e_addA and e_delA
            p_params = predicate.parameters
            f_params = p_params[0].elements

            ins_a = ADD_PREFIX_STR + predicate.name
            del_a = DEL_PREFIX_STR + predicate.name

            f_add_cond = Fact(ins_a, f_params)
            f_del_cond = Fact(del_a, f_params)

            f = Fact(predicate.name, f_params)
            add_eff = AddEffect(f)
            del_eff = DelEffect(f)

            eff_add = ConditionalEffect(f_add_cond, add_eff)
            eff_del = ConditionalEffect(f_del_cond, del_eff)

            elements.extend([eff_add, eff_del])
            new_preds.append(Predicate(ins_a, p_params))
            new_preds.append(Predicate(del_a, p_params))

            # e_del_ins_a_request and e_del_del_a_request
            ins_a_request = ins_a + SUFFIX
            del_a_request = del_a + SUFFIX

            f_del_ins_cond = Fact(ins_a_request, f_params)
            f_del_del_cond = Fact(del_a_request, f_params)

            del_ins_eff = DelEffect(f_del_ins_cond)
            del_del_eff = DelEffect(f_del_del_cond)

            eff_del_ins = ConditionalEffect(f_del_ins_cond, del_ins_eff)
            eff_del_del = ConditionalEffect(f_del_del_cond, del_del_eff)

            elements.extend([eff_del_ins, eff_del_del])
            new_preds.append(Predicate(ins_a_request, p_params))
            new_preds.append(Predicate(del_a_request, p_params))

        effects = ConjunctiveEffect(elements)
        a.effect = effects
        self.actions.append(a)
        self.predicates.extend(new_preds)
