#-*-coding:utf-8-*-
"""
Created on Sat Feb 24 2018
@author: Li, Supeng

Use conditional random field to do tagging
You should address the path of CRF++ package using --p argument
"""
from add_pos_tag import add_pos_tag
import os
from evaluation import evaluation


# train and test conditional random fields model
# output is a .txt file include the predicted label as well as the true label and original word
def conditional_random_field(package_path, train_file_name='Laptops_Train_v2.xml',
                             test_file_name='Laptops_Test_Gold.xml',
                             split_character_set=[' ', ',', '.', '?', '!', ':', ';']):
    # prepare train data
    add_pos_tag(input_file_name=train_file_name, split_character_set=split_character_set)
    # prepare test data
    add_pos_tag(input_file_name=test_file_name, split_character_set=split_character_set)
    # train model
    os.system(package_path + 'crf_learn -f 1 -c 9 template ' + train_file_name.split('.')[0] + '.data model')
    # test model
    os.system(package_path + 'crf_test -m model ' + test_file_name.split('.')[0] + '.data > result.txt')


