from pathlib import Path

from lab import tools

def get_task_variants(benchmarks_dir, domain: str, problem: str, prefixes):
    result = dict()
    for prefix in prefixes:
        problem_file = Path(benchmarks_dir) / domain / f"{prefix}{problem}"
        domain_file_name = problem.replace("problem", "domain")
        domain_file = Path(benchmarks_dir) / domain / f"{prefix}{domain_file_name}"
        result[prefix] =  Task(domain, problem, problem_file=problem_file, domain_file=domain_file, properties={"variant": prefix})
    return result


class Task:
    def __init__(
        self, domain: str, problem: str, problem_file, domain_file=None, properties=None
    ):
        """
        *domain* and *problem* are the display names of the domain and
        problem, *domain_file* and *problem_file* are paths to the
        respective files on the disk. If *domain_file* is not given,
        assume that *problem_file* is a SAS task.

        *properties* may be a dictionary of entries that should be
        added to the properties file of each run that uses this
        problem. ::

            >>> task = Task(
            ...     "gripper",
            ...     "p01.pddl",
            ...     problem_file="/path/to/prob01.pddl",
            ...     domain_file="/path/to/domain.pddl",
            ...     properties={"relaxed": False},
            ... )
        """
        self.domain = domain
        self.problem = problem
        self.problem_file = problem_file
        self.domain_file = domain_file

        self.properties = properties or {}
        self.properties.setdefault("domain", self.domain)
        self.properties.setdefault("problem", self.problem)

    def __str__(self):
        return (
            f"<Task {self.domain}({self.domain_file}):{self.problem}"
            f"({self.problem_file}) {self.properties}>"
        )


#def _generate_problems(benchmarks_dir, description, prefixes):
#    """
#    Descriptions are problems (e.g., "cat:problem_11.pddl").
#    """
#    if ":" in description:
#        domain_name, problem_name = description.split(":", 1)
#        yield get_task_variants(benchmarks_dir, domain_name, problem_name,
#                                prefixes)


def build_suite(benchmarks_dir, descriptions, prefixes):
    """Compute a list of :class:`Task <downward.suites.Task>` objects.

    The path *benchmarks_dir* must contain a subdir for each domain.

    *descriptions* must be a list of domain or problem descriptions::

        build_suite(benchmarks_dir, ["gripper", "grid:prob01.pddl"])
    """
    result = []
    for description in descriptions:
        domain_name, problem_name = description.split(":", 1)
        task = get_task_variants(benchmarks_dir, domain_name, problem_name,
                                 prefixes)
        result.append(task)
    return result
