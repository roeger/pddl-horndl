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
BENCHMARKS_DIR = project.get_repo_base()/"benchmarks/outputs"
SCP_LOGIN = "myname@myserver.com"

SUITE = list(f"cat:problem_{i}.pddl" for i in range(6, 8))
FULLSUITE = []
FULLSUITE.extend(f"blocks:problem_-{i}-{j}.pddl" for i in range(4, 12) for j in range(3))
FULLSUITE.extend(f"blocks:problem_-{i}-{j}.pddl" for i in range(12, 16) for j in range(2))
FULLSUITE.append("blocks:problem_-16-1.pddl")
FULLSUITE.append("blocks:problem_-16-2.pddl")
FULLSUITE.append("blocks:problem_-17-0.pddl")
FULLSUITE.extend(f"catOG:problem_{i}.pddl" for i in range(6, 26))
FULLSUITE.extend(f"catOG:problem_{i}.pddl" for i in range(6, 26))
FULLSUITE.extend(f"elevator:problem_{i}.pddl" for i in range(15, 35))
FULLSUITE.extend(f"order:problem_{i}.pddl" for i in range(4, 8))
FULLSUITE.extend(f"order:problem_{i}.pddl" for i in range(10, 61, 5))
FULLSUITE.extend(f"robot:problem_{i}.pddl" for i in range(3, 23))
#FULLSUITE.extend(["robot:problem_37.pddl", "robot:problem_110.pddl"])
FULLSUITE.extend(f"task:problem_{i}.pddl" for i in range(3, 23))
FULLSUITE.extend(f"trip:problem_{i}.pddl" for i in range(4, 8))
FULLSUITE.extend(f"trip:problem_{i}.pddl" for i in range(10, 61, 5))
FULLSUITE.extend(f"tripv2:problem_{i}.pddl" for i in range(4, 8))
FULLSUITE.extend(f"tripv2:problem_{i}.pddl" for i in range(10, 61, 5))

REVISION_CACHE = (
    os.environ.get("DOWNWARD_REVISION_CACHE") or project.DIR / "data" / "revision-cache"
)
if project.REMOTE:
    ENV = project.BaselSlurmEnvironment(email="gabriele.roeger@unibas.ch")
    SUITE = FULLSUITE 
else:
    ENV = project.LocalEnvironment(processes=1)
    SUITE = FULLSUITE 

CONFIGS = [
    ("astar-blind", ["--search", "astar(blind())"]),
    ("greedy-blind", ["--search", "lazy_greedy([blind()])"]),
    ("ff", ["--search", "let(hff,ff(),lazy_greedy([hff],preferred=[hff]))"]),
    ("ff-approx", ["--search", "let(hff,ff(axioms=approximate_negative),lazy_greedy([hff],preferred=[hff]))"]),
]
BUILD_OPTIONS = []
DRIVER_OPTIONS = [
    "--validate",
    "--overall-time-limit",
    "30m",
    "--overall-memory-limit",
    "3G",
]
# Pairs of revision identifier and optional revision nick.
REV_NICKS = [
    ("a6b98adb939b9fb91eb8f0b5e74eb68a323d65ae", ""), # 24-4-2025
]
ATTRIBUTES = [
    "error",
    "planner_exit_code",
    "unsolvable",
    "planner_memory",
    "planner_time",
    "total_time",
    "coverage",
    "cost",
    "plan_length",
    "expansions",
    "memory",
    "run_dir",
    "initial_h_value",
    "translator_peak_memory",
    "translator_time_done",
    "translator_axioms",
    "translator_axioms_removed",
    "translator_axioms_removed_by_simplifying",
    "translator_derived_variables",
    "translator_facts",
    "translator_time_instantiating",
    "translator_time_processing_axioms",
    "translator_time_simplifying_axioms"
]

variants = { "wtseitin" : "_tseitin", "wotseitin" : "_no_tseitin"}
benchmark_folders = ["var0", "original", "var2"]

exp = Experiment(environment=ENV)
for rev, rev_nick in REV_NICKS:
    cached_rev = CachedFastDownwardRevision(REVISION_CACHE, REPO, rev, BUILD_OPTIONS)
    cached_rev.cache()
    exp.add_resource("", cached_rev.path, cached_rev.get_relative_exp_path())
    for config_nick, config in CONFIGS:
        for task in suites.build_suite(BENCHMARKS_DIR, SUITE,
                                       variants=list(variants.values()),
                                       folders=benchmark_folders):
            for variant, prefix in variants.items():
                for folder in benchmark_folders:
                    if not prefix in task[folder]:
                        continue
                    algo_name = f"{config_nick}-{variant}-{folder}"
                    #algo_name = f"{config_nick}_{folder}"
                    if rev_nick:
                        #algo_name = f"{rev_nick}-{algo_name}" 
                        algo_name = f"{rev_nick}-{config_nick}-{variant}-{folder}"
                    algo = FastDownwardAlgorithm(
                        algo_name,
                        cached_rev,
                        DRIVER_OPTIONS,
                        config,
                    )
                    run = FastDownwardRun(exp, algo, task[folder][prefix])
                    exp.add_run(run)

exp.add_parser(project.FastDownwardExperiment.EXITCODE_PARSER)
exp.add_parser(project.FastDownwardExperiment.TRANSLATOR_PARSER)
exp.add_parser(project.FastDownwardExperiment.SINGLE_SEARCH_PARSER)
exp.add_parser(project.FastDownwardExperiment.PLANNER_PARSER)

exp.add_step("build", exp.build)
exp.add_step("start", exp.start_runs)
exp.add_step("parse", exp.parse)
exp.add_fetcher(name="fetch")

project.add_absolute_report(
    exp,
    attributes=ATTRIBUTES,
)

def only_var0_no_tseitin(run):
    return run["variant"] in ["_no_tseitin"] and run["folder"] == "var0"

def only_var1_no_tseitin(run):
    return run["variant"] in ["_no_tseitin"] and run["folder"] == "var1"

def only_var2_no_tseitin(run):
    return run["variant"] in ["_no_tseitin"] and run["folder"] == "var2"

def only_var3_no_tseitin(run):
    return run["variant"] in ["_no_tseitin"] and run["folder"] == "var3"

def only_var0_with_tseitin(run):
    return run["variant"] in ["_tseitin"] and run["folder"] == "var0"

def only_var1_with_tseitin(run):
    return run["variant"] in ["_tseitin"] and run["folder"] == "var1"

def only_var2_with_tseitin(run):
    return run["variant"] in ["_tseitin"] and run["folder"] == "var2"

def only_var3_with_tseitin(run):
    return run["variant"] in ["_tseitin"] and run["folder"] == "var3"

#project.add_absolute_report(
#    exp,
#    name="coverage-var0-notseitin",
#    attributes=["coverage"],
#    filter=only_var0_no_tseitin,
#    format="tex"
#)
#project.add_absolute_report(
#    exp,
#    name="coverage-var1-notseitin",
#    attributes=["coverage"],
#    filter=only_var1_no_tseitin,
#    format="tex"
#)
#project.add_absolute_report(
#    exp,
#    name="coverage-var2-notseitin",
#    attributes=["coverage"],
#    filter=only_var2_no_tseitin,
#    format="tex"
#)
#project.add_absolute_report(
#    exp,
#    name="coverage-var3-notseitin",
#    attributes=["coverage"],
#    filter=only_var3_no_tseitin,
#    format="tex"
#)
#
#project.add_absolute_report(
#    exp,
#    name="coverage-var0-withtseitin",
#    attributes=["coverage"],
#    filter=only_var0_with_tseitin,
#    format="tex"
#)
#project.add_absolute_report(
#    exp,
#    name="coverage-var1-withtseitin",
#    attributes=["coverage"],
#    filter=only_var1_with_tseitin,
#    format="tex"
#)
#project.add_absolute_report(
#    exp,
#    name="coverage-var2-withtseitin",
#    attributes=["coverage"],
#    filter=only_var2_with_tseitin,
#    format="tex"
#)
#project.add_absolute_report(
#    exp,
#    name="coverage-var3-withtseitin",
#    attributes=["coverage"],
#    filter=only_var3_with_tseitin,
#    format="tex"
#)
#project.add_scatter_plot_reports(
#    exp,
#    algorithm_pairs=[["astar-blind-wotseitin-var0", "ff-approx-wotseitin-var0"]],
#    attributes=["cost"],
#    filter=only_var0_no_tseitin
#)
#project.add_scatter_plot_reports(
#    exp,
#    algorithm_pairs=[["ff-wotseitin-original", "ff-wotseitin-var2"], ["ff-approx-wtseitin-original", "ff-approx-wtseitin-var2"]],
#    attributes=["total_time"],
#    filter=only_var0_no_tseitin
#)
project.add_scatter_plot_reports(
    exp,
    algorithm_pairs=[
        ["ff-wtseitin-var2", "ff-wtseitin-original"],
        ["ff-wotseitin-var2", "ff-wotseitin-original"],
        ["ff-approx-wtseitin-var2", "ff-approx-wtseitin-original"],
        ["ff-approx-wotseitin-var2", "ff-approx-wotseitin-original"],
        ],
    attributes=["total_time"],
#    filter=only_var0_no_tseitin
)
#project.add_scatter_plot_reports(
#    exp,
#    algorithm_pairs=[
#        ["ff-wotseitin-var0", "ff-approx-wotseitin-var0"],
#        ["ff-wtseitin-var0", "ff-approx-wtseitin-var0"],
#        ["ff-wotseitin-var2", "ff-approx-wotseitin-var2"],
#        ["ff-wtseitin-var2", "ff-approx-wtseitin-var2"],
#        ["ff-wotseitin-original", "ff-approx-wotseitin-original"],
#        ["ff-wtseitin-original", "ff-approx-wtseitin-original"],
#        ],
#    attributes=["total_time"],
##    filter=only_var0_no_tseitin
#)
#project.add_scatter_plot_reports(
#    exp,
#    algorithm_pairs=[["greedy-blind-wotseitin-var0", "ff-approx-wotseitin-var0"]],
#    attributes=["evaluations_per_time"],
#    filter=only_var0_no_tseitin
#)

exp.run_steps()
