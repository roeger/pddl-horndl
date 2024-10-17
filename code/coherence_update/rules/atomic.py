# General rules for deleting atomic concepts and roles
# ~ First 2 bullet points/Sec 2.4
from coherence_update.rules.symbols import RULE_SEPARATOR


def build_del_concept_and_incompatible_rules_for_atomic_concepts(a_concepts):
    """
        Build rules for deleting atomic concepts and their incompatible rules
        param:
            a_concepts: string[]
    """
    rules = []
    for a_concept in a_concepts:
        r_del = f"del_{a_concept}(X){RULE_SEPARATOR}del_{a_concept}_request(X), {a_concept}(X)."
        r_inc = f"incompatible_update(){RULE_SEPARATOR}ins_{a_concept}_request(X), del_{a_concept}_request(X)."
        r_update = f"updating(){RULE_SEPARATOR}ins_{a_concept}_request(X)."
        rules.extend([r_del, r_inc, r_update])

    return rules


def build_del_role_and_incompatible_rules_for_roles(roles):
    """
        Build rules for deleting roles and their incompatible rules
        param:
            roles: string[]
    """
    rules = []
    for role in roles:
        r_del = f"del_{role}(X,Y){RULE_SEPARATOR}del_{role}_request(X,Y), {role}(X,Y)."
        r_inc = f"incompatible_update(){RULE_SEPARATOR}ins_{role}_request(X,Y), del_{role}_request(X,Y)."
        r_update = f"updating(){RULE_SEPARATOR}ins_{role}_request(X,Y)."
        rules.extend([r_del, r_inc, r_update])

    return rules


def build_funct_P_and_funct_inv_P_rules(functs, functs_inv):
    """
        Build rules for funct(P) and invFunct(P)
        param:
            functs: string[]
            functs_inv: string[]
    """
    rules = []
    for funct in functs:
        rules.extend(functP(funct))
    for funct_inv in functs_inv:
        rules.extend(functInvP(funct_inv))

    return rules


def functP(repr):
    """
        Caution: repr is representation of `P`, not `functP`
    """
    r_del = f"del_{repr}(X,Y){RULE_SEPARATOR}{repr}(X,Y), ins_{repr}_request(X,Z), Y!=Z."
    r_inc = f"incompatible_update(){RULE_SEPARATOR}ins_{repr}_request(X,Y), ins_{repr}_request(X,Z), Y!=Z."
    r_update = f"updating(){RULE_SEPARATOR}ins_{repr}_request(X,Y)."
    return [r_del, r_inc, r_update]


def functInvP(repr):
    """
        Caution: repr is representation of `P`, not `functP`
    """
    r_del = f"del_{repr}(X,Y){RULE_SEPARATOR}{repr}(X,Y), ins_{repr}_request(Z,Y), X!=Z."
    r_inc = f"incompatible_update(){RULE_SEPARATOR}ins_{repr}_request(X,Y), ins_{repr}_request(Z,Y), X!=Z."
    r_update = f"updating(){RULE_SEPARATOR}ins_{repr}_request(X,Y)."
    return [r_del, r_inc, r_update]

