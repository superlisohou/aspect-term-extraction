#-*-coding:utf-8-*-
"""
Created on Sat Feb 24 2018
@author: Li, Supeng

A trivial learner
"""
from add_pos_tag import add_pos_tag
from logistic_regression import get_dataframe

def trivial_learner(train_file_name='Laptops_Train_v2.xml', test_file_name='Laptops_Test_Gold.xml',
                    split_character_set=[' ', ',', '.', '?', '!', ':', ';']):
    # prepare train data
    add_pos_tag(input_file_name=train_file_name, split_character_set=split_character_set)
    train_data = get_dataframe(train_file_name.split('.')[0] + '.data')
    # prepare test data
    add_pos_tag(input_file_name=test_file_name, split_character_set=split_character_set)
    test_data = get_dataframe(test_file_name.split('.')[0] + '.data')

    # build the dictionary
    dictionary = list(train_data.ix[train_data['label'] == 'I', 'word'])

    # test the dictionary
    test_data['predicted label'] = 'O'
    for i in test_data.index:
        if test_data.ix[i, 'word'] in dictionary:
            test_data.ix[i, 'predicted label'] = 'I'
    test_data[['word', 'label', 'predicted label']].to_csv('result.txt', sep='\t', index=False, header=False)