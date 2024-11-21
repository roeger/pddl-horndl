def variable_name(variable):
    return "h" + variable

def variable_definition(variable, args):
    return f"{variable}({args})"

def expression(variable):
    return f"lazy_greedy([{variable_name(variable)}],preferred=[{variable_name(variable)}])"

def build_arguments(heuristic):
    var = variable_name(heuristic["variable"])
    definition = variable_definition(heuristic["variable"], heuristic["args"])
    exp = expression(heuristic["variable"])
    return f'"let({var},{definition},{exp})"'

def result_domain(task, i):
    return f"benchmarks/outputs/{task}/domain_{i}.pddl"

def result_problem(task, i):
    return f"benchmarks/outputs/{task}/problem_{i}.pddl"

def compiled_domain(task, i):
    return f"benchmarks/outputs/{task}/compiled_domain_{i}.pddl"

def compiled_problem(task, i):
    return f"benchmarks/outputs/{task}/compiled_problem_{i}.pddl"

heuristics = [
    {"variable": "cea", "args": "", "name": "cea"},
    {"variable": "cea", "args": "axioms=approximate_negative", "name": "cea_approximate_negative"},
    {"variable": "ff", "args": "", "name": "hff"},
    {"variable": "cg", "args": "", "name": "cg"},
    # {"variable": "landmark_cost_partitioning", "args": "lm_rhw()", "name": "lm_rhw"},
    # {"variable": "landmark_cost_partitioning", "args": "lm_zg()", "name": "lm_zg"},
]

pddl = [("cat",17), ("elevator", 22), ("task", 15), ("order", 15), ("trip", 5), ("tripv2", 10)]
# ("robot", 9)

if __name__ == "__main__":
    import os
    import time
    fastdownward="/home/zinzin2312/repos/downward/fast-downward.py"
    file="csvs/heuristics_test.csv"

    for h in heuristics:
        arg = build_arguments(h)
        for tsk in pddl:
            task, nr = tsk[0], tsk[1]

            dom = result_domain(task, nr)
            prob = result_problem(task, nr)
            start = time.time()
            command = f"timeout 20 {fastdownward} {dom} {prob} --search {arg}"
            os.system(command)
            end = time.time()
            elapsed = end - start
            with open(file, 'a') as f:
                f.write(f"{h['name']},{dom},{elapsed}\n")

            com_d = compiled_domain(task, nr)
            com_p = compiled_problem(task, nr)
            start = time.time()
            os.system(f"timeout 20 {fastdownward} {com_d} {com_p} --search '{arg}'")
            end = time.time()
            elapsed = end - start
            with open(file, 'a') as f:
                f.write(f"{h['name']},{com_d},{elapsed}\n")
