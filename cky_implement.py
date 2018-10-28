#! /usr/bin/python
import json
from collections import defaultdict
from rule_parameter_computer import ParameterComputer


class CKY(object):
    def __init__(self, binary_parameter, uni_parameter):
        self.binary_parameter = binary_parameter
        self.uni_parameter = uni_parameter
        self.nonterminals = set(self.binary_parameter.keys() + self.uni_parameter.keys())
        self.all_words = set()
        for word_para in self.uni_parameter.values():
            for x in word_para.keys():
                self.all_words.add(x)

    def _pi_table_init(self, sentence):
        self.back_pointer = defaultdict(dict)
        self.pi_table = defaultdict(dict)
        for i in range(1, len(sentence)+1):
            word = sentence[i-1]
            for label in self.nonterminals:
                self.pi_table[(i, i)].setdefault(label, 0)
                if word not in self.all_words:
                    word = "_RARE_"
                self.pi_table[(i, i)][label] = self.uni_parameter[label].get(word, 0)

    def _tree_builder(self, sentence, i, j, X):
        if i == j:
            return [X, sentence[i-1]]
        s, Y, Z = self.back_pointer[(i, j)][X]
        return [X, self._tree_builder(sentence, i, s, Y), self._tree_builder(sentence, s+1, j, Z)]

    def main(self, sentence):
        n = len(sentence)
        self._pi_table_init(sentence)
        for l in range(1, n):
            for i in range(1, n-l+1):
                j = i + l # i -> n-1+i
                for X in self.nonterminals:
                    self.pi_table[(i, j)].setdefault(X, 0)
                    for s in range(i, j):
                        for Y, Z in self.binary_parameter[X].keys():
                            a = self.pi_table.get((i, s)).get(Y)
                            b = self.pi_table.get((s+1, j)).get(Z)
                            temp_probability = self.binary_parameter[X][(Y, Z)] * a * b
                            if (temp_probability != 0 and self.pi_table[(i, j)][X] == 0) or self.pi_table[(i, j)][X] < temp_probability:
                                self.pi_table[(i, j)][X] = temp_probability
                                self.back_pointer[(i, j)][X] = (s, Y, Z)
        # Recovery
        if "S" in self.back_pointer[(1, n)]:
            return json.dumps(self._tree_builder(sentence, 1, n, "S"))
        else:
            max_score = max(self.pi_table[(1, n)].values())
            for k, v in self.pi_table[(1, n)].items():
                if v == max_score:
                    label = k
            return json.dumps(self._tree_builder(sentence, 1, n, label))
