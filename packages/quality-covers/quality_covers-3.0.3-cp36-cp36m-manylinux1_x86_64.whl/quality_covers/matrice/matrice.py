import os
import operator
import re

import numpy as np


def extract_binary_matrices(filename):
    """Extract binary matrices (extent and intent) of output filename"""
    filename = os.path.abspath(filename)
    output_filename_extent = filename + '.binary_extent'
    output_filename_intent = filename + '.binary_intent'
    intent_str_to_int = {}
    intent_int_to_str = {}
    extents = []
    intents = []
    print('Reading:', filename)
    with open(filename, 'r') as f:
        for line in f.read().splitlines():
            line = re.sub('\s*#.*$', '', line)
            if not line:
                continue
            if 'Mandatory:' in line:
                continue
            if 'Non-mandatory:' in line:
                continue
            if 'Total:' in line:
                continue
            line = line.replace(' Mandatory', '')
            extent, intent = line.split(';')
            extent = extent.strip()
            intent = intent.strip()
            extents.append([int(val.strip()) for val in extent.split(',')])
            temp_intents = []
            for val in intent.split(','):
                val = val.strip()
                if intent_str_to_int.get(val, None) is None:
                    new_val_int = len(intent_str_to_int) + 1
                    intent_str_to_int[val] = new_val_int
                    intent_int_to_str[new_val_int] = val

                temp_intents.append(intent_str_to_int[val])

            intents.append(temp_intents)

    # intent
    max_value_intent = max([max(intent) for intent in intents])

    new_intents = []

    for intent in intents:
        new_intent = []
        for i in range(1, max_value_intent+1):
            if i in intent:
                new_intent.append('1')
            else:
                new_intent.append('0')

        new_intents.append(new_intent)

    np_intents = np.array(new_intents)

    with open(output_filename_intent, 'w') as f:
        sorted_intent = sorted(intent_str_to_int.items(), key=operator.itemgetter(1))
        f.write(' '.join([a for a, b in sorted_intent]) + '\n')
        for np_intent in np_intents:
            f.write(' '.join(np_intent) + '\n')

    print('Wrote intent binary matrice:', output_filename_intent)
    # extent
    max_value_extent = max([max(extent) for extent in extents])

    new_extents = []

    for extent in extents:
        new_extent = []
        for i in range(1, max_value_extent+1):
            if i in extent:
                new_extent.append('1')
            else:
                new_extent.append('0')

        new_extents.append(new_extent)

    np_extents = np.array(new_extents)
    np_extents = np_extents.transpose()

    with open(output_filename_extent, 'w') as f:
        for np_extent in np_extents:
            f.write(' '.join(np_extent) + '\n')

    print('Wrote extent binary matrice:', output_filename_extent)


if __name__ == '__main__':
    extract_binary_matrices('/home/toad/projects/pattern_mining/backend/quality_covers_interface/quality_covers/matrice/test.out')
