import os
import sys
import re
import time
import subprocess
from utils.functions import read_predicates, read_unary_predicate
from coherence_update.classes.tbox import TBox
from coherence_update.classes.inclusion import INCLUSION_TYPES_ORDER
from coherence_update.update import CohrenceUpdate
from utils.functions import get_repr

class Timer:
    def __init__(self, message = None, end = "\n", file = sys.stderr, block = False):
        if message:
            print(message + "...", file = file, end="\n" if block else " ", flush=True)
        self.message = message
        self.block = block
        self._t = None
        self.end = end
        self.file = file
    def __enter__(self):
        self._t = time.time()
    def __exit__(self, *args, **kwargs):
        elapsed = time.time() - self._t
        print((self.message + " took " if self.block else "") + "%.4fs" % elapsed, end = self.end, file = self.file, flush=True)


TMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp')
RULES_FILE_NAME = '_update_rules.txt'

class UpdateRunner:
    def __init__(self, nmo_path = "", rls_file_path = "", ontology_file_path="", write_to_file=False):
        self.nmo_path = nmo_path
        self.rls_file_path = rls_file_path
        self.write_to_file = write_to_file
        self.ontology_file_path = ontology_file_path
        self.inclusions = None
        self.roles = None
        self.a_atomics = None
        self.functs = None
        self.invFunct = None
        self.compute_t_closure()

    def run(self):
        tbox = TBox(self.inclusions, roles=self.roles, a_concepts=self.a_atomics, functs=self.functs, functs_inv=self.invFunct)
        rules = CohrenceUpdate.run(tbox)
        if self.write_to_file:
            with open(os.path.join(TMP_DIR, RULES_FILE_NAME), 'w') as f:
                for rule in rules:
                    f.write(rule + '\n')
        return rules


    def compute_t_closure(self):
        if os.path.exists(TMP_DIR):
            subprocess.call(['rm', '-rf', TMP_DIR])

        os.makedirs(TMP_DIR)
        with open(self.rls_file_path, 'r') as f:
            rls = f.read()
            rls = re.sub(r'::DATA_IMPORT_PATH', self.ontology_file_path, rls)
        with open(self.rls_file_path, 'w') as f:
            f.write(rls)

        with Timer("Computing and writing TBox closure", block=True):
            subprocess.call([self.nmo_path, self.rls_file_path, '--export', 'all', '--export-dir', TMP_DIR], stderr=subprocess.PIPE)
            try:
                self.inclusions = read_predicates(TMP_DIR, INCLUSION_TYPES_ORDER)
                self.roles = read_unary_predicate(TMP_DIR, 'atomicRole')
                self.a_atomics = read_unary_predicate(TMP_DIR, 'atomicConcept')
                self.functs = read_unary_predicate(TMP_DIR, 'funct')
                self.invFunct = read_unary_predicate(TMP_DIR, 'invFunct')
            except FileNotFoundError as e:
                print(e)

        with open(self.rls_file_path, 'r') as f:
            rls = f.read()
            rls = re.sub(self.ontology_file_path, '::DATA_IMPORT_PATH', rls)
        with open(self.rls_file_path, 'w') as f:
            f.write(rls)
        subprocess.call(['rm', '-rf', TMP_DIR])

    # def unary_predicates(self):
    #     return [get_repr(uri) for uri in self.a_atomics]
    #
    # def binary_predicates(self):
    #     return set([get_repr(uri) for uri in self.roles + self.functs + self.invFunct])


if __name__ == '__main__':
    runner = UpdateRunner()
    rules = runner()
