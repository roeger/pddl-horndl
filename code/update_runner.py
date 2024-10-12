import os
from utils.functions import read_predicates, read_unary_predicate
from coherence_update.classes.tbox import TBox
from coherence_update.classes.inclusion import INCLUSION_TYPES_ORDER
from coherence_update.update import CohrenceUpdate

TMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp')

class UpdateRunner:
    def __init__(self, nmo_path = "nmo", rls_file_path = "code/nemo/t_closure.rls", write_to_file=False):
        self.nmo_path = nmo_path
        self.rls_file_path = rls_file_path
        self.write_to_file = write_to_file

    def __call__(self):
        if not os.path.exists(TMP_DIR):
            os.makedirs(TMP_DIR)

        self._remove_tmp_files()
        command = f"{self.nmo_path} {self.rls_file_path} --export all --export-dir tmp"
        os.system(command)
        try:
            inclusions = read_predicates(TMP_DIR, INCLUSION_TYPES_ORDER)
            roles = read_unary_predicate(TMP_DIR, 'atomicRole')
            a_atomics = read_unary_predicate(TMP_DIR, 'atomicConcept')
            functs = read_unary_predicate(TMP_DIR, 'funct')
            invFunct = read_unary_predicate(TMP_DIR, 'invFunct')
        except FileNotFoundError as e:
            print(e)
            exit(1)
        tbox = TBox(inclusions, roles=roles, a_concepts=a_atomics, functs=functs, functs_inv=invFunct)
        rules = CohrenceUpdate.run(tbox)
        if self.write_to_file:
            with open(os.path.join(TMP_DIR, '_update_rules.txt'), 'w') as f:
                for rule in rules:
                    f.write(rule + '\n')
        return rules

    def _remove_tmp_files(self):
        for file in os.listdir(TMP_DIR):
            file_path = os.path.join(TMP_DIR, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
                exit(1)
