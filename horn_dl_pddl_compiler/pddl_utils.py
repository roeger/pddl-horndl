#!/usr/bin/env python

import argparse
import itertools

import pddl


def get_assignments(init, name, handle_expression = lambda x: int(x.expression)):
    res = {}
    for x in init:
        if isinstance(x, pddl.Assignment) and x.fhead.predicate == name:
            res[tuple(x.fhead.parameters)] = handle_expression(x.expression)
    return res


def get_facts(init, name):
    res = []
    for x in init:
        if isinstance(x, pddl.Fact) and x.predicate == name:
            res.append(tuple(x.parameters))
    return res


def generate_facts(predicate_name, args):
    for arg in args:
        yield pddl.Fact(predicate_name, list(arg))


def get_objects_of_type(problem, t):
    res = []
    for tl in problem.objects:
        if tl.type.lower() == t:
            res.extend(tl.elements)
    return res


def get_type_to_object_map(domain, problem):
    type_relation = domain.get_type_relation()
    objects = domain.get_type_to_constant_map(type_relation)
    for (t, objs) in problem.get_type_to_object_map(type_relation).items():
        objects[t].extend(objs)
    return objects


def get_object_to_type_map(domain, problem):
    tr = domain.get_type_relation()
    object_to_types = {}
    for (t, objs) in domain.get_type_to_constant_map(tr).items():
        for obj in objs:
            old = object_to_types.get(obj, list())
            old.append(t)
            object_to_types[obj] =old
    for (t, objs) in problem.get_type_to_object_map(tr).items():
        for obj in objs:
            old = object_to_types.get(obj, list())
            old.append(t)
            object_to_types[obj] =old
    return object_to_types


def ground_quantifiers(formula, objects):
    class _grounder:
        def __call__(self, phi):
            os = [ objects[tl.type] for tl in phi.parameters for x in tl.elements ]
            vars = [ x for tl in phi.parameters for x in tl.elements ]
            enumed = []
            for selection in itertools.product(*os):
                subst = { x: selection[i] for (i, x) in enumerate(vars) }
                enumed.append(phi.formula.instantiate(subst).apply(set([pddl.Forall, pddl.Exists]), self))
            if isinstance(phi, pddl.Exists):
                return pddl.Or(enumed).simplified()
            else:
                return pddl.And(enumed).simplified()
    g = _grounder()
    return formula.apply(set([pddl.Forall, pddl.Exists]), g)


def get_static_facts(domain, problem):
    fluent_predicates = set()
    if domain.derived_predicates != None:
        fluent_predicates = set([dp.predicate.name for dp in domain.derived_predicates])
    for action in domain.actions:
        fluent_predicates = fluent_predicates | action.effect.get_fluent_predicates()
    static_predicates = set([p.name for p in domain.predicates if not p.name in fluent_predicates])
    static_facts = set([f for f in problem.initial_state if isinstance(f, pddl.Fact) and f.predicate in static_predicates])
    return static_predicates, static_facts


def simplify_with_static_predicates(condition, static_predicates, static_facts):
    def simplify(fact):
        if not fact.predicate in static_predicates:
            return fact
        if any([p.startswith('?') for p in fact.parameters]):
            return fact
        return pddl.Truth() if fact in static_facts else pddl.Falsity()
    return condition.apply(pddl.Fact, simplify)


def parse_condition_string(content):
    tokens = pddl.TokenList(content)
    return pddl.parse_condition(tokens)


def _parse_pddl_atom(tokens):
    t = tokens.pop()
    assert t == '('
    op_name = tokens.pop()
    arg = tokens.pop()
    params = []
    while arg != ')':
        params.append(arg)
        arg = tokens.pop()
    return (op_name, tuple(params))

def parse_pddl_atom(content):
    return _parse_pddl_atom(pddl.TokenList(content))

def parse_atom_sequence(content):
    tokens = pddl.TokenList(content)
    sequence = []
    while True:
        try:
            op_name, params = _parse_pddl_atom(tokens)
            sequence.append((op_name, params))
        except IndexError:
            break
    return sequence

def parse_ground_action(domain, problem, object_to_types, op_name, params = None):
    if params is None:
        op_name, params = parse_pddl_atom(op_name)
    assert all([obj in object_to_types for obj in params]), "objects %r not found" % [obj for obj in params if not obj in object_to_types]
    ground = None
    for action in domain.actions:
        if action.name != op_name:
            continue
        i = 0
        match = True
        kwargs = {}
        for tl in action.parameters:
            if i + len(tl.elements) > len(params):
                match = False
                break
            for var_name in tl.elements:
                if not tl.type in object_to_types[params[i]]:
                    match = False
                    break
                kwargs[var_name] = params[i]
                i += 1
            if not match:
                break
        if match:
            return action.instantiate(kwargs)
    return None


def parse_action_sequence(domain, problem, content):
    object_to_types = get_object_to_type_map(domain, problem)
    sequence = []
    for (op_name, params) in parse_atom_sequence(content):
        ground = parse_ground_action(domain, problem, op_name, params)
        assert ground != None
        sequence.append(ground)
    return sequence


def execute_action_sequence(domain, problem, action_sequence, state = None, objects = None):
    assert domain.derived_predicates is None or len(domain.derived_predicates) == 0, "Derived predicates are not yet supported."
    objects = objects or get_type_to_object_map(domain, problem)
    if state is None:
        state = set([p for p in problem.initial_state if isinstance(p, pddl.Fact)])
    sequence = [ state ]
    for (step, action) in enumerate(action_sequence):
        assert action.precondition.is_satisfied_by_state(objects, state), "Precondition of %s at step %d violated." % (action.get_full_name(), step)
        state = action.get_successor_state(objects, state)
        sequence.append(state)
    return sequence


def verify_plan(domain, problem, plan):
    objects = get_type_to_object_map(domain, problem)
    states = execute_action_sequence(domain, problem, plan, objects=objects)
    assert problem.goal.is_satisfied_by_state(objects, states[-1]), "Goal is not satisfied"
    return states


class EnumerateForallUpToPreference:
    def __init__(self, objects, static_predicates, static_facts):
        self.depth = 0
        self.preference = False
        self._objects = objects
        self._static_predicates = static_predicates
        self._static_facts = static_facts
    def __call__(self, phi):
        if isinstance(phi, pddl.Preference):
            self.preference = True
            return phi
        else:
            self.depth += 1
            formula = phi.formula.apply(set([pddl.Preference, pddl.Forall]), self)
            self.depth -= 1
            if self.preference:
                if isinstance(formula, pddl.Truth):
                    return pddl.Truth()
                os = [ self._objects[tl.type] for tl in phi.parameters for x in tl.elements ]
                vars = [ x for tl in phi.parameters for x in tl.elements ]
                enumed = set()
                for selection in itertools.product(*os):
                    subst = { x: selection[i] for (i, x) in enumerate(vars) }
                    instance = simplify_with_static_predicates(
                            formula.instantiate(subst).simplified(),
                            self._static_predicates,
                            self._static_facts)
                    assert isinstance(instance, pddl.And) or isinstance(instance, pddl.Preference)
                    elements = [instance] if isinstance(instance, pddl.Preference) else instance.elements
                    assert all([isinstance(e, pddl.Preference) for e in elements])
                    enumed = enumed | set([e for e in elements if not isinstance(e.condition, pddl.Falsity)])
                self.preference = self.depth > 0
                return pddl.And(list(enumed)).simplified()
            # no preference found
            return phi


def collect_preferences_from_condition(
        condition,
        objects,
        static_predicates,
        static_facts,
        filter_fn = lambda x: True):
    prefs = []
    def store(pref):
        if filter_fn(pref):
            prefs.append(pref)
        return pref
    enumf = EnumerateForallUpToPreference(objects, static_predicates, static_facts)
    condition.apply(set([pddl.Preference, pddl.Forall]), enumf).apply(pddl.Preference, store)
    return sorted(prefs, key = lambda pref: pref.name)


def collect_all_preferences_from_problem(domain, problem, leave_out_trivially_satisfied = False):
    filter_fn = lambda x: True
    if leave_out_trivially_satisfied:
        filter_fn = lambda x: not isinstance(x.condition, pddl.Truth)
    objects = get_type_to_object_map(domain, problem)
    static_predicates, static_facts = get_static_facts(domain, problem)
    return collect_preferences_from_condition(problem.goal, objects, static_predicates, static_facts, filter_fn), \
            [] if problem.constraints is None \
            else collect_preferences_from_condition(problem.constraints, objects, static_predicates, static_facts, filter_fn)


def collect_satisfied_preferences(domain, problem, plan, state_sequence = None, leave_out_trivially_satisfied = False, invert = False):
    objects = get_type_to_object_map(domain, problem)
    state_sequence = state_sequence or execute_action_sequence(domain, problem, plan, objects=objects)
    static_predicates, static_facts = get_static_facts(domain, problem)

    def ignore(pref):
        return isinstance(pref.condition, pddl.Truth) and leave_out_trivially_satisfied

    invert = (lambda x: not x) if invert else (lambda x: x)

    class is_sat_in_state:
        def __init__(self, state):
            self.state = state
        def __call__(self, pref):
            return not ignore(pref) and invert(pref.condition.is_satisfied_by_state(objects, self.state))

    def is_sat_in_sequence(pref):
        return not ignore(pref) and invert(pref.condition.is_satisfied_by_state_sequence(objects, state_sequence))

    # collected satisfied precondition preferences
    precondition_preferences = []
    for i in range(len(plan)):
        action = plan[i]
        precondition_preferences.extend([(i, preference) for preference in collect_preferences_from_condition(
            action.precondition,
            objects,
            static_predicates,
            static_facts,
            is_sat_in_state(state_sequence[i]))])

    # collect satisfied goal preferences
    goal_preferences = collect_preferences_from_condition(
        problem.goal,
        objects,
        static_predicates,
        static_facts,
        is_sat_in_state(state_sequence[-1]))

    # collect satisfied trajectory preferences
    trajectory_preferences = []
    if problem.constraints != None:
        trajectory_preferences = collect_preferences_from_condition(
            problem.constraints,
            objects,
            static_predicates,
            static_facts,
            is_sat_in_sequence)

    return precondition_preferences, goal_preferences, trajectory_preferences


class integers:
    default_object_name = "int-{}"

    def generate_objects(n, type_name = "integer", object_name = None):
        object_name = object_name or integers.default_object_name
        return pddl.TypedList([object_name.format(i) for i in range(n+1)], type_name)

    def generate_greater_facts(n, predicate_name = "GREATER", object_name = None):
        object_name = object_name or integers.default_object_name
        return generate_facts(predicate_name, [(object_name.format(x), object_name.format(y)) for x in range(1, n+1) for y in range(x)])

    def generate_next_facts(n, predicate_name = "NEXT", object_name = None, wrap_around = False):
        object_name = object_name or integers.default_object_name
        return generate_facts(predicate_name, [(object_name.format(x), object_name.format((x+1) % (n+1))) for x in range(n + wrap_around)])


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("domain")
    p.add_argument("problem")
    p.add_argument("plan")
    args = p.parse_args()

    with open(args.domain) as f:
        domain = pddl.parse_domain(f.read().lower())

    with open(args.problem) as f:
        problem = pddl.parse_problem(f.read().lower())

    with open(args.plan) as f:
        plan = parse_action_sequence(domain, problem, f.read().lower())

    pp, gp, tp = collect_satisfied_preferences(domain, problem, plan)

    print("Precondition preferences:")
    for (i, p) in pp:
        print(i, plan[i].get_full_name(), p)

    print("")
    print("Goal preferences:")
    for p in gp:
        print(p)

    print("")
    print("Trajectory preferences:")
    for p in tp:
        print(p)

