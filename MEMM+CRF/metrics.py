from sklearn_crfsuite import metrics

dev_name = './KOREAN_NAME_CORPUS/KOR_dev.name'
dev_result = './outputs/response.name'
test_name = './KOREAN_NAME_CORPUS/KOR_test.name'
test_result = './outputs/KOR_test.name'

new_classes = []
y_dev, tags = [], []
with open(dev_name, 'r', encoding='utf-8') as f:
    for line in f:
        data = line.strip().split("\t")
        if len(data) == 1:
            y_dev.append(tags)
            tags = []
        else:
            tags.append(data[-1])
        if data[-1]!="-X-" and len(data) > 1 and data[-1] not in new_classes:
            new_classes.append(data[-1])

y_pred_dev, tags = [], []
with open(dev_result, 'r', encoding='utf-8') as f:
    for line in f:
        data = line.strip().split("\t")
        if len(data) == 1:
            y_pred_dev.append(tags)
            tags = []
        else:
            tags.append(data[-1])

y_test, tags = [], []
with open(test_name, 'r', encoding='utf-8') as f:
    for line in f:
        data = line.strip().split("\t")
        if len(data) == 1:
            y_test.append(tags)
            tags = []
        else:
            tags.append(data[-1])

y_pred_test, tags = [], []
with open(test_result, 'r', encoding='utf-8') as f:
    for line in f:
        data = line.strip().split("\t")
        if len(data) == 1:
            y_pred_test.append(tags)
            tags = []
        else:
            tags.append(data[-1])

new_classes.sort()
print(metrics.flat_classification_report(y_dev, y_pred_dev, labels = new_classes))
print(metrics.flat_classification_report(y_test, y_pred_test, labels = new_classes))