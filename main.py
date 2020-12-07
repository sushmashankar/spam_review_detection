import argparse
import pandas as pd
from feature_extraction import *
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--dataset', action='store', dest='dataset', default='preprocessed.csv', required=False,
                        help='Path to the dataset that is to be used in the training and testing of the model')
    parser.add_argument('-c', '--classifier', action='store', dest='classifier', default='svm', required=False,
                        help='Classification algorithm to be used Ex. svm, naive')
    args = parser.parse_args()

    data = pd.read_csv(args.dataset)
    print(data.iloc[0]['preprocessed_text'])  # data.iloc[0][5] or data.iloc[0, 5]
    print(data.iloc[0]['deceptive'])  # data.iloc[0][0] or data.iloc[0, 0]

    if args.classifier.lower() == 'svm':
        X = data.iloc[:, 5 if args.dataset == 'preprocessed.csv' else 4]

    y = data.iloc[:, 0]

    ## get features
    # ngram
    X = calculate_bag_of_words(X, ngram = 2)
    # X = calculate_tf_idf(X, ngram = 2)
    print(X)

    ## split the data

    from sklearn.metrics import precision_recall_fscore_support as score
    from sklearn.metrics import f1_score

    ## train a model


    # splitting X and y into training and testing sets
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.295, random_state=109)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=2)
    # training the model on training set
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)
    # making predictions on the testing set
    y_pred = gnb.predict(X_test)

    p, r, f, s = score(y_test, y_pred,average=None)
    print(p, r, f, s )
    print('precision: {}'.format(p))
    f1_none = f1_score(y_test, y_pred, average=None)
    # print(f1_none)

    # comparing actual response values (y_test) with predicted response values (y_pred)
    print("Gaussian Naive Bayes model accuracy(in %):", metrics.accuracy_score(y_test, y_pred)*100)
