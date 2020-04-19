Written in Python 2.7
All the output files including feature files, name files, and Max Entropy model are in outputs directory.

To execute, run the following commands sequentially at the top-most directory:
$ python FeatureBuilder.py
$ javac -cp maxent-3.0.0.jar;trove.jar *.java
$ java -cp .;maxent-3.0.0.jar;trove.jar MEtrain outputs/CONLL_train.feature outputs/MEmodel
$ java -cp .;maxent-3.0.0.jar;trove.jar [MEtag or MEtagVit] outputs/CONLL_dev.feature outputs/MEmodel outputs/response.name
$ java -cp .;maxent-3.0.0.jar;trove.jar [MEtag or MEtagVit] outputs/CONLL_test.feature outputs/MEmodel outputs/CONLL_test.name
$ python score.name.py
* If using Unix-oriented terminal, please replace all semi-colons (;) to colons (:).

Features used:
1. [pre2, pre, cur, post, post2]_token = 2 preceding, current and 2 succeeding words (tokens) 
2. [pre, cur, post]_pos = pos tags of the previous, current, and next words 
3. [pre, cur, post]_bio = bio tags of the previous, current, and next words
4. l_token = lower-cased string of the current word
5. upper_char_frac = fraction of the number of upper-case letters
6. title_cased = whether or not the string is title-cased (starts with upper-case character)
7. prefix = first 3 letters of the current word
8. suffix = last 3 letters of the current word
9. token_shape = shape of the current word (e.g. if the word is 'Hello.10', the corresponding shape is 'Ssssspdd'; 
                 S or s for upper- and lower-case characters, d for digits, p for punctuations)
10. pre_tag = name tag of previous token (if there's no previous word, '@@' is assigned)

Results:
1. features_list = [pre2_token, pre_token, cur_token, post_token, post2_token, cur_pos, cur_bio, pre_pos, pre_bio, post_pos, post_bio, 
                    l_token, title_cased, all_lower, prefix, suffix, pre_tag]
49599 out of 51578 tags correct
  accuracy: 96.16
5917 groups in key
5355 groups in response
4426 correct groups
  precision: 82.65
  recall:    74.80
  F1:        78.53

2. features_list = [pre2_token, pre_token, cur_token, post_token, post2_token, cur_pos, cur_bio, pre_pos, pre_bio, post_pos, post_bio, 
                    l_token, upper_char_frac, prefix, suffix, pre_tag]
50120 out of 51578 tags correct
  accuracy: 97.17
5917 groups in key
5750 groups in response
4891 correct groups
  precision: 85.06
  recall:    82.66
  F1:        83.84

3. features_list = [pre2_token, pre_token, cur_token, post_token, post2_token, cur_pos, cur_bio, pre_pos, pre_bio, post_pos, post_bio, 
                    l_token, upper_char_frac, title_cased, all_lower, prefix, suffix, pre_tag]
50133 out of 51578 tags correct
  accuracy: 97.20
5917 groups in key
5747 groups in response
4901 correct groups
  precision: 85.28
  recall:    82.83
  F1:        84.04

4. features_list = [pre2_token, pre_token, cur_token, post_token, post2_token, cur_pos, cur_bio, pre_pos, pre_bio, post_pos, post_bio, 
                    l_token, upper_char_frac, title_cased, token_shape, prefix, suffix, pre_tag]
50196 out of 51578 tags correct
  accuracy: 97.32
5917 groups in key
5856 groups in response
4953 correct groups
  precision: 84.58
  recall:    83.71
  F1:        84.14

5. features_list = [pre2_token, pre_token, cur_token, post_token, post2_token, cur_pos, cur_bio, pre_pos, pre_bio, post_pos, post_bio, 
                    l_token, upper_char_frac, title_cased, all_lower, token_shape, prefix, suffix, pre_tag]
50215 out of 51578 tags correct
  accuracy: 97.36
5917 groups in key
5854 groups in response
4962 correct groups
  precision: 84.76
  recall:    83.86
  F1:        84.31

The above features resulted in the highest accuracy and F1 score. With Viterbi tagging, F1 score rised quite a bit:
50246 out of 51578 tags correct
  accuracy: 97.42
5917 groups in key
5858 groups in response
4982 correct groups
  precision: 85.05
  recall:    84.20
  F1:        84.62

It seems like upper_char_frac and token_shape are some significant features to achieve higher score.
Experimenting with different lengths of prefix and suffix can be a good exercise to figure out how they affect the results.
