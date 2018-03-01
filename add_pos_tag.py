#-*-coding:utf-8-*-
"""
Created on Sat Feb 24 2018
@author: Li, Supeng

Use nltk package to perform part-of-speech tagging
"""
from xml_data_parser import xml_data_parser
import nltk


def add_pos_tag(input_file_name, split_character_set):

    #
    xml_data_parser(input_file_name=input_file_name, split_character_set=split_character_set)
    # read the input file
    infile = open(input_file_name.split('.')[0] + '.txt')
    #
    outfile = open(input_file_name.split('.')[0] + '.data', 'w')
    # store the token within a sentence
    token_list = []
    label_list = []
    for line in infile.readlines():
        # do pos tagging for each sentence
        if line == '\n':
            outfile.write
            pos_tag_list = nltk.pos_tag(token_list)
            # output the result
            for i in range(len(token_list)):
                outfile.write(token_list[i] + '\t')
                outfile.write(pos_tag_list[i][1] + '\t')
                outfile.write(label_list[i] + '\n')
            # use '\n' to indicate the end of sentence
            outfile.write('\n')
            token_list = []
            label_list = []
        else:
            line_list = line.strip('\n').split('\t')
            # append token
            token_list.append(line_list[0])
            # append label
            label_list.append(line_list[1])
    outfile.close()
