"""
Created on Sat Feb 24 2018
@author: Li, Supeng

Use logistic regression to do tagging
"""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from add_pos_tag import add_pos_tag

# read tab delimited train or test data and return a pandas dataframe
def get_dataframe(input_file_name):

    infile = open(input_file_name)

    line_dict = []

    for line in infile.readlines():
        if line == '\n':
            line_dict.append({'word': ' ', 'POS tag': ' ', 'label': ' '})
            continue

        word_list = line.strip('\n').split('\t')
        line_dict.append({'word': word_list[0], 'POS tag': word_list[1], 'label': word_list[2]})

    return pd.DataFrame(line_dict)


def logistic_regression(train_file_name='Laptops_Train_v2.xml', test_file_name='Laptops_Test_Gold.xml',
                        split_character_set=[' ', ',', '.', '?', '!', ':', ';']):
    # prepare train data
    add_pos_tag(input_file_name=train_file_name, split_character_set=split_character_set)
    train_data = get_dataframe(train_file_name.split('.')[0] + '.data')
    # prepare test data
    add_pos_tag(input_file_name=test_file_name, split_character_set=split_character_set)
    test_data = get_dataframe(test_file_name.split('.')[0] + '.data')

    # manually prepare the feature
    train_data['last word'] = train_data['word'].shift(1)
    train_data['next word'] = train_data['word'].shift(-1)
    train_data['last POS tag'] = train_data['POS tag'].shift(1)
    train_data['next POS tag'] = train_data['POS tag'].shift(-1)
    train_data['last POS tag + POS tag'] = train_data['last POS tag'] + ',' + train_data['POS tag']
    train_data['next POS tag + POS tag'] = train_data['next word'] + ',' + train_data['word']
    train_data = train_data.fillna(' ')
    test_data['last word'] = test_data['word'].shift(1)
    test_data['next word'] = test_data['word'].shift(-1)
    test_data['last POS tag'] = test_data['POS tag'].shift(1)
    test_data['next POS tag'] = test_data['POS tag'].shift(-1)
    test_data['last POS tag + POS tag'] = test_data['last POS tag'] + ',' + test_data['POS tag']
    test_data['next POS tag + POS tag'] = test_data['next word'] + ',' + test_data['word']
    test_data = test_data.fillna(' ')

    # one hot encoding the features
    train_test_data = pd.concat([train_data, test_data], keys=['train', 'test'])
    train_test_x = pd.get_dummies(train_test_data['word'])
    train_test_x = train_test_x.merge(pd.get_dummies(train_test_data['word']), left_index=True, right_index=True)
    train_test_x = train_test_x.merge(pd.get_dummies(train_test_data['last word']), left_index=True, right_index=True)
    train_test_x = train_test_x.merge(pd.get_dummies(train_test_data['POS tag']), left_index=True, right_index=True)
    train_test_x = train_test_x.merge(pd.get_dummies(train_test_data['last POS tag + POS tag']), left_index=True,
                                      right_index=True)
    train_test_x = train_test_x.merge(pd.get_dummies(train_test_data['next POS tag + POS tag']), left_index=True,
                                      right_index=True)

    train_x = train_test_x.ix['train', :]
    test_x = train_test_x.ix['test', :]

    lr = LogisticRegression(C=1000)
    # train the model
    lr.fit(train_x.values, train_data['label'].values)
    # test the model
    test_data['predicted label'] = lr.predict(test_x)
    test_data[['word', 'label', 'predicted label']].to_csv('result.txt', sep='\t', index=False, header=False)
