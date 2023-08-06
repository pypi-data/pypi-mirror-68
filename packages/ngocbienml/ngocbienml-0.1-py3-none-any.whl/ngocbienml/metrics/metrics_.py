from __future__ import print_function

from sklearn.metrics import *
import pandas as pd
import numpy as np
import pandas as pd


def binary_score(model, test, y_test, name='test'):

    from sklearn.metrics import accuracy_score, balanced_accuracy_score, recall_score
    from collections import Counter
    try:
        pred_test_proba = model.predict_proba(test)
        if len(pred_test_proba.shape)>1:
            pred_test_proba = pred_test_proba[:, 1]
    except AttributeError:
        pred_test_proba = model.predict(test)
    gini_test = gini(y_test, pred_test_proba)
    pred_test = model.predict(test)
    if len(np.unique(pred_test))>2 :
        pred_test = pred_test>.5
    is_balanced_ = (sum(y_test))/(len(y_test))
    if np.abs(is_balanced_-.5)<.02:
        is_balanced = True
    else:
        is_balanced = False
    print('*'*80)
    print('on %s'%name.upper())
    if not is_balanced:
        acc_test = balanced_accuracy_score(y_test, pred_test)*100
        print('balanced accuracy = %.3f %%' % acc_test, end=' | ')
    acc_test = accuracy_score(y_test, pred_test)*100
    print('Accuracy = %.3f %%' % acc_test, end=' | ')
    print('Gini = %.3f ' % gini_test, end=' | ')
    recall = recall_score(y_test, pred_test)
    print('Recall score=%.3f' % recall, end=' | ')

    print('confusion matrix:')
    df = pd.DataFrame(confusion_matrix(y_test, pred_test), index=['True_0', 'True_1'], columns=['Pred_0', 'Pred_1'])
    print(df)


def binary_score_(y_test, pred_test_label, pred_test_proba, name='test'):

    from sklearn.metrics import accuracy_score, balanced_accuracy_score, recall_score
    from collections import Counter
    if len(pred_test_proba.shape)>1:
        pred_test_proba = pred_test_proba[:, 1]
    gini_test = gini(y_test, pred_test_proba)
    is_balanced_ = (sum(pred_test_label))/(len(pred_test_label))
    if np.abs(is_balanced_-.5)<.02:
        is_balanced = True
    else:
        is_balanced = False
    print('*'*80)
    print('on %s'%name.upper())
    if not is_balanced:
        acc_test = balanced_accuracy_score(y_test, pred_test_label)*100
        print('balanced accuracy = %.3f %%' % acc_test, end=' | ')
    acc_test = accuracy_score(y_test, pred_test_label)*100
    print('Accuracy = %.3f %%' % acc_test, end=' | ')
    print('Gini = %.3f ' % gini_test, end=' | ')
    recall = recall_score(y_test, pred_test_label)
    print('Recall score=%.3f' % recall, end=' | ')

    print('confusion matrix:')
    df = pd.DataFrame(confusion_matrix(y_test, pred_test_label), index=['True_0', 'True_1'], columns=['Pred_0', 'Pred_1'])
    print(df)


def multiclass_score(model, test, y_test, name):

    from sklearn.metrics import balanced_accuracy_score, accuracy_score
    pred_test = model.predict(test)
    if len(pred_test.shape)>1:
        pred_test = np.argmax(pred_test, axis=1)
    acc_test = balanced_accuracy_score(y_test, pred_test)*100
    print('*'*80)
    print('On %s: Balanced accuracy  = %.3f %%' % (name, acc_test), end=' | ')
    print('accuracy = %.3f %%' % accuracy_score(y_test, pred_test), end=' | ')
    index = ['True_%s' % str(i) for i in range(len(np.unique(y_test)))]
    columns = ['Pred_%s' % str(i) for i in range(len(np.unique(y_test)))]
    df = pd.DataFrame(confusion_matrix(y_test, pred_test), index=index, columns=columns)
    print('Confusion matrix:')
    print(df)


def gini(actual, pred):

    from sklearn.metrics import roc_curve, auc
    fpr, tpr, thresholds = roc_curve(actual, pred, pos_label=1)
    auc_score = auc(fpr,tpr)
    return 2*auc_score-1


def confusion_matrix(actual, pred):

    from sklearn.metrics import confusion_matrix
    return confusion_matrix(actual, pred)
