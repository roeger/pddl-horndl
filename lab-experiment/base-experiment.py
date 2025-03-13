#! /usr/bin/env python

## compare the benchmark version with tseitin transformation against the one without

import os

import custom_parser
import project

import suites

from downward.cached_revision import CachedFastDownwardRevision
from downward.experiment import FastDownwardAlgorithm, FastDownwardRun
from lab.experiment import Experiment


#REPO = project.get_repo_base()
REPO = os.environ["DOWNWARD_AIBASEL"]
BENCHMARKS_DIR = project.get_repo_base()/"benchmarks"/"outputs"
SCP_LOGIN = "myname@myserver.com"

SUITE = list(f"cat:problem_{i}.pddl" for i in range(6, 8))
FULLSUITE = []
FULLSUITE.extend(f"cat:problem_{i}.pddl" for i in range(6, 26))
FULLSUITE.extend(f"catOG:problem_{i}.pddl" for i in range(10, 26))
FULLSUITE.extend(f"elevator:problem_{i}.pddl" for i in range(15, 35))
FULLSUITE.extend(f"order:problem_{i}.pddl" for i in range(4, 8))
FULLSUITE.extend(f"order:problem_{i}.pddl" for i in range(10, 61, 5))
FULLSUITE.extend(f"robot:problem_{i}.pddl" for i in range(3, 23))
FULLSUITE.extend(["robot:problem_37.pddl", "robot:problem_110.pddl"])
FULLSUITE.extend(f"task:problem_{i}.pddl" for i in range(3, 23))
FULLSUITE.extend(f"trip:problem_{i}.pddl" for i in range(4, 8))
FULLSUITE.extend(f"trip:problem_{i}.pddl" for i in range(10, 61, 5))
FULLSUITE.extend(f"tripv2:problem_{i}.pddl" for i in range(4, 8))
FULLSUITE.extend(f"tripv2:problem_{i}.pddl" for i in range(10, 61, 5))
print(SUITE)

REVISION_CACHE = (
    os.environ.get("DOWNWARD_REVISION_CACHE") or project.DIR / "data" / "revision-cache"
)
if project.REMOTE:
    ENV = project.BaselSlurmEnvironment(email="gabriele.roeger@unibas.ch")
    SUITE = FULLSUITE 
else:
    ENV = project.LocalEnvironment(processes=1)

CONFIGS = [
    ("ff", ["--search", "let(hff,ff(),lazy_greedy([hff],preferred=[hff]))"]),
    ("ff-approx", ["--search", "let(hff,ff(axioms=approximate_negative),lazy_greedy([hff],preferred=[hff]))"]),
    ("cea", ["--search", "let(hcea,cea(),lazy_greedy([hcea],preferred=[hcea]))"]),
    ("cea-approx", ["--search", "let(hcea,cea(axioms=approximate_negative),lazy_greedy([hcea],preferred=[hcea]))"]),
    ("cg", ["--search", "let(hcg,cg(),lazy_greedy([hcg],preferred=[hcg]))"]),
    ("cg-approx", ["--search", "let(hcg,cg(axioms=approximate_negative),lazy_greedy([hcg],preferred=[hcg]))"]),
]
BUILD_OPTIONS = []
DRIVER_OPTIONS = [
#    "--validate",
    "--overall-time-limit",
    "5m",
    "--overall-memory-limit",
    "8G",
]
# Pairs of revision identifier and optional revision nick.
REV_NICKS = [
    ("1eef26b2cbf599a1894606aa898d9d49e1034cb9", ""), # 24.06.1
]
ATTRIBUTES = [
    "error",
    "run_dir",
    "search_start_time",
    "search_start_memory",
    "total_time",
    "h_values",
    "coverage",
    "expansions",
    "memory",
    project.EVALUATIONS_PER_TIME,
]

variants = { "notseitin" : "", "tseitin" : "compiled_"}

exp = Experiment(environment=ENV)
for rev, rev_nick in REV_NICKS:
    cached_rev = CachedFastDownwardRevision(REVISION_CACHE, REPO, rev, BUILD_OPTIONS)
    cached_rev.cache()
    exp.add_resource("", cached_rev.path, cached_rev.get_relative_exp_path())
    for config_nick, config in CONFIGS:

        for task in suites.build_suite(BENCHMARKS_DIR, SUITE,
                                                prefixes=list(variants.values())):
            for variant, prefix in variants.items():
                algo_name = f"{rev_nick}-{config_nick}-{variant}" if rev_nick else f"{config_nick}-{variant}"
                algo = FastDownwardAlgorithm(
                    algo_name,
                    cached_rev,
                    DRIVER_OPTIONS,
                    config,
                )
                run = FastDownwardRun(exp, algo, task[prefix])
                exp.add_run(run)

exp.add_parser(project.FastDownwardExperiment.EXITCODE_PARSER)
exp.add_parser(project.FastDownwardExperiment.TRANSLATOR_PARSER)
exp.add_parser(project.FastDownwardExperiment.SINGLE_SEARCH_PARSER)
exp.add_parser(custom_parser.get_parser())
exp.add_parser(project.FastDownwardExperiment.PLANNER_PARSER)

exp.add_step("build", exp.build)
exp.add_step("start", exp.start_runs)
exp.add_step("parse", exp.parse)
exp.add_fetcher(name="fetch")

project.add_absolute_report(
    exp,
    attributes=ATTRIBUTES,
#    filter=[project.add_evaluations_per_time, project.group_domains],
)
#if not project.REMOTE:
#    project.add_scp_step(exp, SCP_LOGIN, REMOTE_REPOS_DIR)
#project.add_compress_exp_dir_step(exp)

exp.run_steps()
