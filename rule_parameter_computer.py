#! /usr/bin/python
from collections import defaultdict


class ParameterComputer(object):
    def __init__(self, input_file):
        self.input_file = input_file
        self.nonterminal_cnt_dict = dict()
        self.binary_rule_cnt_dict = defaultdict(dict)
        self.emission_cnt_dict = defaultdict(dict)
        self.binary_parameter = defaultdict(dict)
        self.uni_parameter = defaultdict(dict)

    def counter(self):
        with open(self.input_file, "r") as f:
            line = f.readline()
            while line:
                self._counter_helper(line)
                line = f.readline()

    def _counter_helper(self, line):
        info = line.split()
        if len(info) == 3:
            # It is a NONTERMINAL
            cnt, data_type, label = info
            self.nonterminal_cnt_dict[label] = int(cnt)
        elif len(info) == 4:
            # It is a UNARYRULE
            cnt, data_type, label, word = info
            self.emission_cnt_dict[label][word] = int(cnt)
        elif len(info) == 5:
            # It is a BINARYRULE
            cnt, data_type, parent, label1, label2 = info
            self.binary_rule_cnt_dict[parent][(label1, label2)] = int(cnt)

    def parameter_computer(self):
        for parent, children in self.binary_rule_cnt_dict.items():
            for children_val, cnt in children.items():
                self.binary_parameter[parent][children_val] = float(cnt)/self.nonterminal_cnt_dict[parent]
        for label, word_cnt in self.emission_cnt_dict.items():
            for word, cnt in word_cnt.items():
                self.uni_parameter[label][word] = float(cnt)/self.nonterminal_cnt_dict[label]
