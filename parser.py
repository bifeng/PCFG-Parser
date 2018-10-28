#! /usr/bin/python
import json
import os
import sys
from cky_implement import CKY
from rare_word_handler import RareReplacer
from rule_parameter_computer import ParameterComputer


def q4_caller(input, output):
    with open(input, "r") as f:
        obj = RareReplacer(input)
        obj.main(file(output, "w"))
    f.close()


def q5_caller(train, dev, pred):
    os.system("python count_cfg_freq.py %s > new_cfg.counts" % train)
    PC = ParameterComputer("hw2/new_cfg.counts")
    PC.counter()
    PC.parameter_computer()
    obj = CKY(PC.binary_parameter, PC.uni_parameter)
    with open(pred, "w") as f:
        with open(dev, "r") as r:
            line = r.readline()
            while line:
                f.write(obj.main(line.split()) + "\n")
                line = r.readline()


def q6_caller(train, dev, pred):
    os.system("python count_cfg_freq.py %s > new_vert_cfg.counts" % train)
    PC = ParameterComputer("new_vert_cfg.counts")
    PC.counter()
    PC.parameter_computer()
    obj = CKY(PC.binary_parameter, PC.uni_parameter)
    with open(pred, "w") as fout:
        with open(dev, "r") as fin:
            line = fin.readline()
            while line:
                fout.write(obj.main(line.split()) + "\n")
                line = fin.readline()


def main(question_id, train_file, output_file, *prediction_file):
    if prediction_file:
        print "Question %s" % question_id
        print "Train file %s" % train_file
        print "Dev file %s" % output_file
        print "Prediction file %s" % prediction_file
    else:
        print "Question %s" % question_id
        print "Train file %s" % train_file
        print "Output file %s" % output_file
    if question_id not in ["q4", "q5", "q6"]:
        sys.stderr.write("""Input Format Error\n""")
    if question_id == "q4":
        q4_caller(train_file, output_file)
    elif question_id == "q5":
        q5_caller(train_file, output_file, prediction_file[0])
    elif question_id == "q6":
        q6_caller(train_file, output_file, prediction_file[0])


def usage():
    sys.stderr.write("""
    Usage: \n
    Q4:\n
    python parser.py q4 parse_train.dat parse_train.RARE.dat\n
    Q5:\n
    python parser.py q5 parse_train.RARE.dat parse_dev.dat q5_prediction_file\n
    python eval_parser.py parse_dev.key q5_prediction_file > q5_eval.txt\n
    Q6:\n
    python parser.py q4 parse_train_vert.dat parse_train_vert.RARE.dat\n
    python parser.py q6 parse_train_vert.RARE.dat parse_dev.dat q6_prediction_file\n
    python eval_parser.py parse_dev.key q6_prediction_file > q6_eval.txt\n\n""")


if __name__ == "__main__":
    usage()
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        sys.stderr.write("""Input Format Error\n""")
        sys.exit(1)
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])