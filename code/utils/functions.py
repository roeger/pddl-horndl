import csv
import os
from collections import defaultdict
from pprint import pprint
import re

def read_csv(file_name):
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def get_repr(uri):
    name = uri.split('/')[-1].split('#')[-1]
    # check if name is a blank node
    if name.startswith('_:'):
        name = f"blank{name[2:]}"
    else:
        # name = re.sub(r'_([a-z])', lambda x: x.group(1).upper(), name)
        # name = name[0].upper() + name[1:]

        # snake case of name
        name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name).lower()
    return name


def read_predicates(tmp_dir, pred_types):
    predicates = defaultdict(list)
    for ns in pred_types:
        file_name = os.path.join(tmp_dir, f'{ns}.csv')
        data = read_csv(file_name)
        predicates[ns] = data

    # pprint(predicates)
    return predicates


def flatten_list(l):
    if not l:
        return []
    return [item for sublist in l for item in sublist]


def read_binary_predicate(tmp_dir, pred_name):
    predicates = defaultdict(str)
    file_name = os.path.join(tmp_dir, f'{pred_name}.csv')
    data = read_csv(file_name)
    for row in data:
        predicates[row[0]] = row[1]

    return predicates


def read_unary_predicate(tmp_dir, pred_name):
    predicates = []
    file_name = os.path.join(tmp_dir, f'{pred_name}.csv')
    data = read_csv(file_name)
    for row in data:
        predicates.append(row[0])

    return predicates
