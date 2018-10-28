#! /usr/bin/python
import os
from cky_implement import CKY
from rare_word_handler import RareReplacer
from rule_parameter_computer import ParameterComputer

if __name__ == "__main__":
    file_name = "hw2/parse_train_vert.dat"
    with open(file_name, "r") as f:
        RR = RareReplacer("hw2/parse_train_vert.dat")
        RR.main(file("new_vertical_train_file.dat", "w"))
    os.system("python hw2/count_cfg_freq.py new_vertical_train_file.dat > new_vert_cfg.counts")
    PC = ParameterComputer("new_vert_cfg.counts")
    PC.counter()
    PC.parameter_computer()
    obj = CKY(PC.binary_parameter, PC.uni_parameter)
    output_file = "new_parsed_vert.dat"
    with open(output_file, "w") as fout:
        with open("hw2/parse_dev.dat", "r") as fin:
            line = fin.readline()
            while line:
                fout.write(obj.main(line.split()) + "\n")
                line = fin.readline()
