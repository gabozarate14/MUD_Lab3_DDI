#!/usr/bin/env python3

import sys
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import PassiveAggressiveClassifier, SGDClassifier
import numpy as np
import argparse
from joblib import dump


def load_data(data):
	features = []
	labels = []
	for interaction in data:
		interaction = interaction.strip()
		interaction = interaction.split('\t')
		interaction_dict = {feat.split('=')[0]:feat.split('=')[1] for feat in interaction[1:] }
		features.append(interaction_dict)
		labels.append(interaction[0])
	return features, labels

if __name__ == '__main__':

	if len(sys.argv) < 4:
		print("One parameter of execution is missing")
		sys.exit(1)

	model_file = sys.argv[1]
	vectorizer_file = sys.argv[2]
	model = sys.argv[3]


	train_features, y_train = load_data(sys.stdin)
	y_train = np.asarray(y_train)
	classes = np.unique(y_train)

	v = DictVectorizer()
	X_train = v.fit_transform(train_features)

	if model == "NB":
		clf = MultinomialNB(alpha=0.01)
	elif model == "SGD":
		clf = SGDClassifier(loss='hinge', alpha=0.0001, penalty='l2', max_iter=1000)
	elif model == "PAC":
		clf = PassiveAggressiveClassifier(C=0.1)
	else:
		raise ValueError("Invalid model specified")

	clf.partial_fit(X_train, y_train, classes)

	#Save classifier and DictVectorizer
	dump(clf, model_file) 
	dump(v, vectorizer_file)
