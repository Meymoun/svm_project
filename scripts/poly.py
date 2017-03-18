import mp2
import numpy as np
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score

def train_model(sequence, feature, k, ws):
    clf = svm.SVC(class_weight='balanced', kernel='poly')

    target_names = ['Membrane', 'Intracellular', 'Globular', 'Extracellular']

    scores = []
    f1scores = []

    count = 0
    for n in range(k):
        count += 1

        # k-fold cross-validation, one part for test
        x_test = sequence[n]
        y_test = feature[n]

        x_train = np.concatenate([j for i, j in enumerate(sequence) if i != n])
        y_train = np.concatenate([j for i, j in enumerate(feature) if i != n])

        clf.fit(x_train, y_train)

        score = clf.score(x_test, y_test)
        prediction = clf.predict(x_test)
        classification = classification_report(y_test, prediction, target_names=target_names)
        f1 = f1_score(y_test, prediction, average='macro')

        print ('Model %r of %r, ws: %r\n' % (count, k, ws))
        print (classification)

        scores.append(score)
        f1scores.append(f1)

    print ('ws: %r' % ws)
    print ('Scores: %r\n' % scores)
    print ('Score mean: %f\n' % np.mean(scores))

    with open('./../output/svm_poly', 'a') as f:
        f.write('ws: %r, svm, kernel = rbf\n' % ws)
        f.write('Score mean: %f\n' % np.mean(scores))
        f.write('Standard deviation: %f\n' % np.std(scores))
        f.write('f1 score mean: %f\n' % np.mean(f1scores))
        f.write('f1 standard deviation: %f\n' % np.std(f1scores))


def run(input):

    ws = 19
    k = 5 # 5-fold cross-validation

    f = mp2.open_file(input)
    splitFile = mp2.split_file_content(f)


    conv_seq = mp2.convert_sequence(splitFile[0], ws)
    conv_label = mp2.convert_features(splitFile[1])

    shuttled = mp2.randomized(conv_seq, conv_label)

    sets = mp2.divide_in_sets(shuttled[0], shuttled[1], k)

    train_model(sets[0], sets[1], k, ws)

input = './../input/x3glob'
run(input)