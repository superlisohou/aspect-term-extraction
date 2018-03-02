#-*-coding:utf-8-*-
"""
Created on Sat Feb 24 2018
@author: Li, Supeng

A simple aspect term extraction with two algorithms: conditional random fields and logistic regression
"""

import argparse
from conditional_random_field import conditional_random_field
from logistic_regression import logistic_regression
from trivial_learner import trivial_learner
from evaluation import evaluation

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--a', type=str)
    parser.add_argument('--p', type=str)
    args = parser.parse_args()

    if args.a is None:
        print('Please use --a argument to specify which algorithm to use, ' +
              'crf for conditional random field and lr for logistic regression and t for a trivial learner' +
              'if you choose crf, please also specify the path of CRF++ package')
        return

    elif args.a == 'lr':
        logistic_regression()
        evaluation()

    elif args.a == 't':
        trivial_learner()
        evaluation()

    elif args.a == 'crf':
        if args.p is None:
            print('Please use --p argument to specify the path of CRF++ package')
            return
        else:
            conditional_random_field(package_path=args.p)
            evaluation()
    else:
        print('Please use --a argument to specify which algorithm to use, ' +
              'crf for conditional random field and lr for logistic regression' +
              'if you choose crf, please also specify the path of CRF++ package')
        return

if __name__ == '__main__':
    main()
