import sklearn_crfsuite
from sklearn_crfsuite import metrics


train_feat = './outputs/KOR_train.feature'
dev_feat = './outputs/KOR_dev.feature'
dev_name = './KOREAN_NAME_CORPUS/KOR_dev.name'
test_feat = './outputs/KOR_test.feature'
test_name = './KOREAN_NAME_CORPUS/KOR_test.name'

# Preprocess
features = ["pre2_token", "pre_token", "cur_token", "post_token", 
            "post2_token", "cur_pos", "cur_eoj", "pre_pos", "pre_eoj", 
            "post_pos", "post_eoj", "token_len", "token_shape", "prefix", 
            "suffix", "pre_tag"]
new_classes = []
x_train, y_train = [], []
feats, tags = [], []
with open(train_feat, 'r', encoding='utf-8') as f:
    for line in f:
        data = line.strip().split("\t")
        if len(data) == 1:
            x_train.append(feats)
            y_train.append(tags)
            feats, tags = [], []
        else:
            ldict = {}
            for i in range(1, len(data)-1):
                ldict[features[i-1]] = data[i]
            feats.append(ldict)
            tags.append(data[-1])
        if data[-1]!="-X-" and len(data) > 1 and data[-1] not in new_classes:
            new_classes.append(data[-1])
new_classes.sort()
        
x_dev, y_dev, w_dev = [], [], []
feats, tags, words = [], [], []
with open(dev_feat, 'r', encoding='utf-8') as f:
    for line in f:
        data = line.strip().split("\t")
        if len(data) == 1:
            x_dev.append(feats)
            feats = []
        else:
            ldict = {}
            for i in range(1, len(data)-1):
                ldict[features[i-1]] = data[i]
            feats.append(ldict)
with open(dev_name, 'r', encoding='utf-8') as f:
    for line in f:
        data = line.strip().split("\t")
        if len(data) == 1:
            y_dev.append(tags)
            w_dev.append(words)
            tags, words = [], []
        else:
            tags.append(data[-1])
            words.append(data[0])

x_test, y_test, w_test = [], [], []
feats, tags, words = [], [], []
with open(test_feat, 'r', encoding='utf-8') as f:
    for line in f:
        data = line.strip().split("\t")
        if len(data) == 1:
            x_test.append(feats)
            feats = []
        else:
            ldict = {}
            for i in range(1, len(data)-1):
                ldict[features[i-1]] = data[i]
            feats.append(ldict)
with open(test_name, 'r', encoding='utf-8') as f:
    for line in f:
        data = line.strip().split("\t")
        if len(data) == 1:
            y_test.append(tags)
            w_test.append(words)
            tags, words = [], []
        else:
            tags.append(data[-1])
            words.append(data[0])

# Train a CRF model
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)
crf.fit(x_train, y_train)

# Evaluate
y_pred_dev = crf.predict(x_dev)
print(metrics.flat_classification_report(y_dev, y_pred_dev, labels = new_classes))
y_pred_test = crf.predict(x_test)
print(metrics.flat_classification_report(y_test, y_pred_test, labels = new_classes))

# Output results
dev_result = './outputs/response.name'
test_result = './outputs/KOR_test.name'
with open(dev_result, 'w', encoding='utf-8') as f:
    for i in range(len(w_dev)):
        for j in range(len(w_dev[i])):
            f.write(str(w_dev[i][j]) + "\t" + str(y_pred_dev[i][j]) + "\n")
        f.write("\n")
        
with open(test_result, 'w', encoding='utf-8') as f:
    for i in range(len(w_test)):
        for j in range(len(w_test[i])):
            f.write(str(w_test[i][j]) + "\t" + str(y_pred_test[i][j]) + "\n")
        f.write("\n")