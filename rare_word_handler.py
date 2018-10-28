#! /usr/bin/python
import json
from collections import defaultdict

RARE_THRESHOLD = 5


class RareReplacer(object):
    def __init__(self, train_file):
        self.train_file = train_file
        self.counter_dict = defaultdict(int)
        self.rare_set = set()

    def parser(self, tree):
        if isinstance(tree, basestring):
            self.counter_dict[tree] += 1
            return
        if len(tree) == 3:
            # It is a binary rule.
            self.parser(tree[1])
            self.parser(tree[2])
        elif len(tree) == 2:
            # It is a unary rule.
            self.parser(tree[1])

    def counter(self):
        for word, cnt in self.counter_dict.items():
            if cnt < RARE_THRESHOLD:
                self.rare_set.add(word)

    def replacer(self, tree):
        if isinstance(tree, basestring):
            if tree in self.rare_set:
                return "_RARE_"
            return tree
        if len(tree) == 3:
            # It is a binary rule.
            return [tree[0], self.replacer(tree[1]), self.replacer(tree[2])]
        elif len(tree) == 2:
            # It is a unary rule.
            return [tree[0], self.replacer(tree[1])]

    def main(self, output_file):
        with open(self.train_file, "r") as f:
            line = f.readline()
            while line:
                tree = json.loads(line)
                self.parser(tree)
                line = f.readline()
            self.counter()
            f.seek(0) # cursor back to the first line
            line = f.readline()
            while line:
                tree = json.loads(line)
                new_tree = self.replacer(tree)
                line = f.readline()
                output_file.write(json.dumps(new_tree) + "\n")
