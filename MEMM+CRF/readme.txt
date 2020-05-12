Written in Python 3.7
All the output files including feature files, name files, and Max Entropy model are in outputs directory.

To execute MEMM, run the following commands sequentially at the top-most directory:
$ python preprocess.py
$ python FeatureBuilder.py
$ javac -cp maxent-3.0.0.jar;trove.jar *.java
$ java -cp .;maxent-3.0.0.jar;trove.jar MEtrain outputs/CONLL_train.feature outputs/MEmodel
$ java -cp .;maxent-3.0.0.jar;trove.jar [MEtag or MEtagVit] outputs/CONLL_dev.feature outputs/MEmodel outputs/response.name
$ java -cp .;maxent-3.0.0.jar;trove.jar [MEtag or MEtagVit] outputs/CONLL_test.feature outputs/MEmodel outputs/CONLL_test.name
$ python score.name.py
$ python metric.py
* If using Unix-oriented terminal, please replace all semi-colons (;) to colons (:).

To execute CRF, run the following commands sequentially at the top-most directory:
$ python preprocess.py
$ python FeatureBuilder.py
$ python CRF.py
$ python score.name.py


Features used:

Features = [pre2_token, pre_token, cur_token, post_token, post2_token, cur_pos, cur_eoj, 
            pre_pos, pre_eoj, post_pos, post_eoj, token_len, token_shape, prefix, suffix, pre_tag]

1. [pre2, pre, cur, post, post2]_token = 2 preceding, current and 2 succeeding words (tokens) 
2. [pre, cur, post]_pos = pos tags of the previous, current, and next words 
3. [pre, cur, post]_eoj = position in Eojeol of the previous, current, and next words (morphemes)
4. prefix = first 1 letters of the current word
5. suffix = last 1 letters of the current word
6. token_len = length of the current word
7. token_shape = shape of the current word (e.g. if the word is 'Hello.하이10', the corresponding shape is 'eeeeepkkdd'; 
                 k for Korean characters, e for English characters, c for Chinese characters, d for digits, p for punctuations)
8. pre_tag = name tag of previous token (if there's no previous word, '@@' is assigned)


Results:
METAG=================================
	dev:
             precision    recall  f1-score   support

       B-DT       0.94      0.76      0.84       503
       B-LC       0.69      0.63      0.66       309
       B-OG       0.75      0.43      0.54       828
       B-PS       0.67      0.65      0.66       223
       B-TI       0.80      0.89      0.84        44
       I-DT       0.96      0.91      0.94       837
       I-LC       0.65      0.29      0.40       104
       I-OG       0.73      0.30      0.43       627
       I-PS       0.50      0.19      0.28        52
       I-TI       0.97      0.88      0.93        78
          O       0.93      0.99      0.96     16701

avg / total       0.91      0.92      0.91     20306

18690 out of 20307 tags correct
  accuracy: 92.04
3605 groups in key
2614 groups in response
2178 correct groups
  precision: 83.32
  recall:    60.42
  F1:        70.04

	test:
             precision    recall  f1-score   support

       B-DT       0.87      0.66      0.75       299
       B-LC       0.71      0.58      0.64       276
       B-OG       0.67      0.45      0.54       431
       B-PS       0.75      0.55      0.64       400
       B-TI       0.92      0.45      0.60        49
       I-DT       0.92      0.72      0.81       533
       I-LC       0.72      0.25      0.37       131
       I-OG       0.71      0.31      0.43       427
       I-PS       0.62      0.15      0.24        66
       I-TI       0.84      0.79      0.82       117
          O       0.94      0.99      0.97     17104

avg / total       0.92      0.93      0.92     19833

18390 out of 19834 tags correct
  accuracy: 92.72
2729 groups in key
1833 groups in response
1445 correct groups
  precision: 78.83
  recall:    52.95
  F1:        63.35

MEVIT==================================
	dev:
             precision    recall  f1-score   support

       B-DT       0.94      0.79      0.86       503
       B-LC       0.68      0.62      0.65       309
       B-OG       0.77      0.42      0.54       828
       B-PS       0.67      0.65      0.66       223
       B-TI       0.81      0.89      0.85        44
       I-DT       0.96      0.92      0.94       837
       I-LC       0.66      0.28      0.39       104
       I-OG       0.74      0.29      0.42       627
       I-PS       0.53      0.17      0.26        52
       I-TI       0.99      0.88      0.93        78
          O       0.93      0.99      0.96     16701

avg / total       0.91      0.92      0.91     20306

18696 out of 20307 tags correct
  accuracy: 92.07
3605 groups in key
2591 groups in response
2172 correct groups
  precision: 83.83
  recall:    60.25
  F1:        70.11

	test:
             precision    recall  f1-score   support

       B-DT       0.88      0.68      0.77       299
       B-LC       0.73      0.58      0.65       276
       B-OG       0.68      0.43      0.53       431
       B-PS       0.76      0.55      0.64       400
       B-TI       0.92      0.47      0.62        49
       I-DT       0.92      0.72      0.81       533
       I-LC       0.74      0.27      0.39       131
       I-OG       0.76      0.30      0.43       427
       I-PS       0.62      0.15      0.24        66
       I-TI       0.84      0.74      0.79       117
          O       0.94      0.99      0.97     17104

avg / total       0.92      0.93      0.92     19833

18405 out of 19834 tags correct
  accuracy: 92.80
2729 groups in key
1796 groups in response
1440 correct groups
  precision: 80.18
  recall:    52.77
  F1:        63.65

CRF=====================================
	dev:
             precision    recall  f1-score   support

       B-DT       0.86      0.75      0.80       503
       B-LC       0.69      0.79      0.73       309
       B-OG       0.82      0.50      0.62       828
       B-PS       0.54      0.85      0.66       223
       B-TI       0.84      0.98      0.91        44
       I-DT       0.99      0.62      0.76       837
       I-LC       0.71      0.21      0.33       104
       I-OG       0.93      0.19      0.32       627
       I-PS       0.56      0.17      0.26        52
       I-TI       0.65      0.78      0.71        78
          O       0.93      0.99      0.96     16701

avg / total       0.92      0.91      0.90     20306

18564 out of 20307 tags correct
  accuracy: 91.42
3605 groups in key
2489 groups in response
1993 correct groups
  precision: 80.07
  recall:    55.28
  F1:        65.41

	test:
             precision    recall  f1-score   support

       B-DT       0.81      0.71      0.75       299
       B-LC       0.67      0.71      0.69       276
       B-OG       0.78      0.46      0.58       431
       B-PS       0.75      0.75      0.75       400
       B-TI       0.71      0.61      0.66        49
       I-DT       0.97      0.48      0.64       533
       I-LC       0.73      0.34      0.46       131
       I-OG       0.82      0.07      0.13       427
       I-PS       0.43      0.05      0.08        66
       I-TI       0.91      0.50      0.64       117
          O       0.94      0.99      0.96     17104

avg / total       0.92      0.92      0.91     19833

18313 out of 19834 tags correct
  accuracy: 92.33
2729 groups in key
1688 groups in response
1330 correct groups
  precision: 78.79
  recall:    48.74
  F1:        60.22