# Negation inclusion rules (Sec 2.4)

# TODO(dnh):  Last 2 closure rules

def atomicB_in_not_atomicA(b_repr, a_repr):
    """
        Caution: a_repr is representation of `A`, not `not A`
    """
    r_del_b = f"del_{b_repr}(X) :- {b_repr}(X), ins_{a_repr}_request(X)."
    r_del_a = f"del_{a_repr}(X) :- {a_repr}(X), ins_{b_repr}_request(X)."
    r_inc = f"incompatible_update() :- ins_{b_repr}_request(X), ins_{a_repr}_request(X)."

    return [r_del_b, r_del_a, r_inc]


def atomicA_closure(a_repr, b_reprs, j_reprs, r_reprs):
    """
        param a_repr: string
        param b_reprs: list of B_i concepts where
            A in lnot B_i
        param j_reprs: list of J_i roles where
            A in lnot dom(J_i)
        param r_reprs: list of R_i roles where
            A in lnot rng(R_i)
    """
    r_closure = f"ins_{a_repr}(X) :- ins_{a_repr}_closure(X)"
    for b_repr in b_reprs:
        r_closure += f", not ins_{b_repr}_request(X)"

    for idx, j_repr in enumerate(j_reprs):
        r_closure += f", not ins_{j_repr}_request(X,Y{idx+1})"

    for idx, r_repr in enumerate(r_reprs):
        r_closure += f", not ins_{r_repr}_request(Y{idx+1},X)"
    r_closure += "."

    return [r_closure]


def roleP_closure(p_repr, r_reprs, s_reprs, t_reprs, q_reprs, w_reprs, u_reprs, a_reprs, b_reprs):
    """
        param p_repr: string
        param r_reprs: list of R_i roles where
            P in lnot r_i
        param s_reprs: list of S_i roles where
            P in lnot rng(S_i)
        param t_reprs: list of T_i roles where
            dom(P) in lnot dom(T_i)
        param q_reprs: list of Q_i roles where
            dom(P) in lnot rng(Q_i)
        param w_reprs: list of W_i roles where
            rng(P) in lnot dom(W_i)
        param u_reprs: list of U_i roles where
            rng(P) in lnot rng(U_i)
        param a_reprs: list of A_i concepts where
            dom(P) in lnot A_i
        param b_reprs: list of B_i concepts where
            rng(P) in lnot B_i
    """
    r_closure = f"ins_{p_repr}(X,Y) :- ins_{p_repr}_closure(X,Y)"
    for r_repr in r_reprs:
        r_closure += f", not ins_{r_repr}_request(X,Y)"
    for s_repr in s_reprs:
        r_closure += f", not ins_{s_repr}_request(Y,X)"
    for idx, t_repr in enumerate(t_reprs):
        r_closure += f", not ins_{t_repr}_request(X,Y{idx+1})"
    for idx, q_repr in enumerate(q_reprs):
        r_closure += f", not ins_{q_repr}_request(Y{idx+1},X)"
    for idx, w_repr in enumerate(w_reprs):
        r_closure += f", not ins_{w_repr}_request(Y,X{idx+1})"
    for idx, u_repr in enumerate(u_reprs):
        r_closure += f", not ins_{u_repr}_request(X{idx+1},Y)"
    for a_repr in a_reprs:
        r_closure += f", not ins_{a_repr}_request(X)"
    for b_repr in b_reprs:
        r_closure += f", not ins_{b_repr}_request(Y)"
    r_closure += "."

    return [r_closure]


def atomicB_in_not_domP(b_repr, p_repr):
    """
        Caution: p_repr is representation of `P`, not `not existsP`
    """
    r_del_b = f"del_{b_repr}(X) :- {b_repr}(X), ins_{p_repr}_request(X,Y)."
    r_del_p = f"del_{p_repr}(X,Y) :- {p_repr}(X,Y), ins_{b_repr}_request(X)."
    r_inc = f"incompatible_update() :- ins_{b_repr}_request(X), ins_{p_repr}_request(X,Y)."

    return [r_del_b, r_del_p, r_inc]


def domP_in_not_atomicB(p_repr, b_repr):
    """
        Caution: p_repr is representation of `P`, not `existsP`
            b_repr is representation of `B`
    """
    r_del_p = f"del_{b_repr}(X,Y) :- {b_repr}(X,Y), ins_{p_repr}_request(X)."
    r_del_b = f"del_{p_repr}(X) :- {p_repr}(X), ins_{b_repr}_request(X,Y)."
    r_inc = f"incompatible_update() :- ins_{p_repr}_request(X), ins_{b_repr}_request(X,Y)."

    return [r_del_b, r_del_p, r_inc]


def r_in_not_P(r_repr, p_repr):
    """
        Caution: p_repr is representation of `P`, not `not P`
    """
    r_del_r = f"del_{r_repr}(X,Y) :- {r_repr}(X,Y), ins_{p_repr}_request(X,Y)."
    r_del_p = f"del_{p_repr}(X,Y) :- {p_repr}(X,Y), ins_{r_repr}_request(X,Y)."
    r_inc = f"incompatible_update() :- ins_{r_repr}_request(X,Y), ins_{p_repr}_request(X,Y)."

    return [r_del_r, r_del_p, r_inc]


def r_in_not_invP(r_repr, p_repr):
    """
        Caution: p_repr is representation of `P`, not `not invP`
    """
    r_del_r = f"del_{r_repr}(X,Y) :- {r_repr}(X,Y), ins_{p_repr}_request(Y,X)."
    r_del_p = f"del_{p_repr}(X,Y) :- {p_repr}(X,Y), ins_{r_repr}_request(Y,X)."
    r_inc = f"incompatible_update() :- ins_{r_repr}_request(Y,X), ins_{p_repr}_request(Y,X)."

    return [r_del_r, r_del_p, r_inc]


NEG_INCL_METHOD_MAP = {
    "aAInNotaBSub": atomicB_in_not_atomicA,
    "aBInNotePSub": atomicB_in_not_domP,
    "ePInNotaBSub": domP_in_not_atomicB,
    "rInNotPSub": r_in_not_P,
    "rInNotPMinusSub": r_in_not_invP
}

