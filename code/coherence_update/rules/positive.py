# Positive inclusion rules (Sec 2.4)

def atomicB_in_atomicA(b_repr, a_repr):
    """
        :param b_repr: string
        :param a_repr: string
        :param super_predicates: string[]
    """
    r_del = f"del_{b_repr}(X) :- {b_repr}(X), del_{a_repr}_request(X)."
    r_inc = f"incompatible_update() :- ins_{b_repr}_request(X), del_{a_repr}_request(X)."

    return [r_del, r_inc]


def atomicB_in_atomicA_closure(b_repr, a_repr, ai_reprs):
    """
        param ai_reprs: list of A_i concepts where
            A in A_i
    """
    r_closure = f"ins_{a_repr}_closure(X) :- del_{b_repr}(X), not {a_repr}(X), not ins_{a_repr}_request(X), not del_{a_repr}_request(X)"

    for ai_repr in ai_reprs:
        if ai_repr == a_repr:
            continue

        r_closure += f", not del_{ai_repr}_request(X)"
    r_closure += "."

    return [r_closure]


def domP_in_atomicB(p_repr, b_repr):
    """
        Caution: p_repr is representation of `P`, not `domP` (or existsP)
    """
    r_del = f"del_{p_repr}(X,Y) :- {p_repr}(X,Y), del_{b_repr}_request(X)."
    r_inc = f"incompatible_update() :- ins_{p_repr}_request(X,Y), del_{b_repr}_request(X)."
    return [r_del, r_inc]


def domP_in_atomicB_closure(p_repr, b_repr, bi_reprs):
    """
        param bi_reprs: list of B_i concepts where
            b in B_i
    """
    r_closure = f"ins_{b_repr}_closure(X) :- del_{p_repr}(X,Y), not {b_repr}(X), not ins_{b_repr}_request(X), not del_{b_repr}_request(X)"

    for bi_repr in bi_reprs:
        if bi_repr == b_repr:
            continue

        r_closure += f", not del_{bi_repr}_request(X)"
    r_closure += "."

    return [r_closure]


def rngP_in_atomicB(p_repr, b_repr):
    """
        Caution: p_repr is representation of `P`, not `rngP` (or existsPMinus)
    """
    r_del = f"del_{p_repr}(X,Y) :- {p_repr}(X,Y), del_{b_repr}_request(Y)."
    r_inc = f"incompatible_update() :- ins_{p_repr}_request(X,Y), del_{b_repr}_request(Y)."
    return [r_del, r_inc]


def rngP_in_atomicB_closure(p_repr, b_repr, bi_reprs):
    """
        param bi_reprs: list of B_i concepts where
            b in B_i

    """
    r_closure = f"ins_{b_repr}_closure(X) :- del_{p_repr}(Y,X), not {b_repr}(X), not ins_{b_repr}_request(X), not del_{b_repr}_request(X)"

    for bi_repr in bi_reprs:
        if bi_repr == b_repr:
            continue

        r_closure += f", not del_{bi_repr}_request(X)"
    r_closure += "."

    return [r_closure]


def roleR_in_roleP(r_repr, p_repr):
    r_del = f"del_{r_repr}(X,Y) :- {r_repr}(X,Y), del_{p_repr}_request(X,Y)."
    r_inc = f"incompatible_update() :- ins_{r_repr}_request(X,Y), del_{p_repr}_request(X,Y)."
    return [r_del, r_inc]


def roleR_in_roleP_closure(r_repr, p_repr, pi_reprs, si_reprs):
    """
        param pi_reprs: list of P_i roles where
            P in P_i
        param si_reprs: list of S_i roles where
            P in inv(S_i)
    """
    r_closure = f"ins_{p_repr}_closure(X,Y) :- del_{r_repr}(X,Y), not {p_repr}(X,Y), not ins_{p_repr}_request(X,Y), not del_{p_repr}_request(X,Y)"

    for pi_repr in pi_reprs:
        if pi_repr == p_repr:
            continue

        r_closure += f", not del_{pi_repr}_request(X,Y)"

    for si_repr in si_reprs:
        r_closure += f", not del_{si_repr}_request(Y,X)"
    r_closure += "."

    return [r_closure]


def roleR_in_invP(r_repr, p_repr):
    """
        Caution: p_repr is representation of `P`, not `invP`.
    """
    r_del = f"del_{r_repr}(X,Y) :- {r_repr}(X,Y), del_{p_repr}_request(Y,X)."
    r_inc = f"incompatible_update() :- ins_{r_repr}_request(X,Y), del_{p_repr}_request(Y,X)."
    return [r_del, r_inc , r_closure]


def roleR_in_invP_closure(r_repr, p_repr, pi_reprs, si_reprs):
    """
        param pi_reprs: list of P_i roles where
            P in P_i
        param si_reprs: list of S_i roles where
            P in inv(S_i)
    """

    r_closure = f"ins_{p_repr}_closure(X,Y) :- del_{r_repr}(Y,X), not {p_repr}(X,Y), not ins_{p_repr}_request(X,Y), not del_{p_repr}_request(X,Y)"
    for pi_repr in pi_reprs:
        if pi_repr == p_repr:
            continue

        r_closure += f", not del_{pi_repr}_request(X,Y)"
    for si_repr in si_reprs:
        r_closure += f", not del_{si_repr}_request(Y,X)"
    r_closure += "."
    return [r_closure]


def invR_in_roleP(left_repr, right_repr):
    r_del = f"del_{left_repr}(X,Y) :- {left_repr}(X,Y), del_{right_repr}_request(Y,X)."
    r_inc = f"incompatible_update() :- ins_{left_repr}_request(X,Y), del_{right_repr}_request(Y,X)."

    return [r_del, r_inc]



POS_INCL_METHOD_MAP = {
    "aAInaBSub": atomicB_in_atomicA,
    "rInPSub": roleR_in_roleP,
    "rInPMinusSub": roleR_in_invP,
    "rMinusInPSub": invR_in_roleP,
    "ePInaBSub": domP_in_atomicB,
    "ePMinusInaBSub": rngP_in_atomicB,
}

POS_INCL_CLOSURE_METHOD_MAP = {
    "aAInaBSub": atomicB_in_atomicA_closure,
    "rInPSub": roleR_in_roleP_closure,
    "rInPMinusSub": roleR_in_invP_closure,
    "ePInaBSub": domP_in_atomicB_closure,
    "ePMinusInaBSub": rngP_in_atomicB_closure,
}
