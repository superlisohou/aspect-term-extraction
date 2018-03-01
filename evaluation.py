#-*-coding:utf-8-*-
"""
Created on Sat Feb 24 2018
@author: Li, Supeng

Evaluate the tagging result
"""
from xml.etree import cElementTree
import pandas as pd


def evaluation():
    infile = open('result.txt')

    # read the test data, the data is in a xml format
    raw_doc = cElementTree.ElementTree(file='Laptops_Test_Gold.xml')

    # get the root element, all sentences
    sentences = raw_doc.getroot()

    # read the ground truth
    sentence_id_list = []
    # list to store all true aspect term
    truth_list = []

    for sentence in sentences:
        true_aspect_term_list = []
        sentence_id_list.append(sentence.attrib['id'])
        for element in sentence:
            if element.tag == 'aspectTerms':
                for aspect_term in element:
                    true_aspect_term_list.append(aspect_term.attrib['term'].lower().replace('-', ' '))
        truth_list.append(true_aspect_term_list)

    # get prediction result
    prediction_list = []
    aspect_term_list = []
    # buffer to store words within an aspect term
    aspect_term_buffer = ''

    for line in infile.readlines():
        word_list = line.strip('\n').split('\t')

        # for CRF, end of sentence are indicated by '\n'
        # for LR, end of sentence are indicated by a space word
        # for random guess, end of sentence are indicated by a None
        if line == '\n' or word_list[0] == ' ' or len(word_list[0]) == 0:
            if aspect_term_buffer != '':
                aspect_term_list.append(aspect_term_buffer)
            prediction_list.append(aspect_term_list)
            aspect_term_list = []
            aspect_term_buffer = ''
            continue

        if word_list[-1] == 'B':
            if aspect_term_buffer != '':
                aspect_term_list.append(aspect_term_buffer)
                aspect_term_buffer = ''
            aspect_term_buffer += (word_list[0])
        elif word_list[-1] == 'I':
            if aspect_term_buffer != '':
                aspect_term_buffer += (' ' + word_list[0])
            else:
                aspect_term_buffer += (word_list[0])
        else:
            if aspect_term_buffer != '':
                aspect_term_list.append(aspect_term_buffer)
                aspect_term_buffer = ''
    sentences_data = []
    for i in range(len(sentence_id_list)):
        sentences_data.append({'id': sentence_id_list[i], 'true aspect term': set(truth_list[i]),
                               'predicted aspect term': set(prediction_list[i])})

    # calculate performance metrics: recall and precision
    true_positive = 0
    false_negative = 0
    false_positive = 0

    for sentence in sentences_data:
        for aspect_term in sentence['true aspect term']:
            if aspect_term in sentence['predicted aspect term']:
                true_positive += 1
            else:
                false_negative += 1

        for aspect_term in sentence['predicted aspect term']:
            if aspect_term not in sentence['true aspect term']:
                false_positive += 1

    recall = true_positive / (true_positive + false_negative)
    precision = true_positive / (true_positive + false_positive)
    F1_score = 2 * true_positive / (2 * true_positive + false_negative + false_positive)

    print('recall:', recall)
    print('precision:', precision)
    print('F1 score:', F1_score)
    pd.DataFrame(sentences_data).to_csv('extraction result.csv')
    print('Please check the "extraction result.csv" to see extracted aspect terms')