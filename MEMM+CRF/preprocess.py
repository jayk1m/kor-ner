import json


NEcorpus = 'KOREAN_NAME_CORPUS/NEtaggedCorpus_train.json'
train_file = 'KOREAN_NAME_CORPUS/KOR_train.pos-name'
dev_pos = 'KOREAN_NAME_CORPUS/KOR_dev.pos'
dev_name = 'KOREAN_NAME_CORPUS/KOR_dev.name'
test_pos = 'KOREAN_NAME_CORPUS/KOR_test.pos'
test_name = 'KOREAN_NAME_CORPUS/KOR_test.name'

with open(NEcorpus, 'r', encoding='utf-8') as f:
    data = json.load(f)

#print len(data['sentence']) #3555
#train/dev/test = 2500/530/525
total = []
for sc in data['sentence']:
    words = []
    for m in sc['morp']:
        words.append([m['lemma'], m['type'], m['id'], 'O'])
    for w in sc['word']:
        for i in range(w['begin'], w['end'] + 1):
            words[i][2] = i - w['begin']
    for ne in sc['NE']:
        for i in range(ne['begin'], ne['end'] + 1):
            words[i][3] = ne['type']
    total.append(words)

train = total[:2500]
test = total[2500:3030]
dev = total[3030:]

# BIO tagging
for sc in total:
    prev_tag = "O"
    for w in sc:
        tag = w[3]
        if tag == "O":
            prev_tag = tag
            continue
        if tag != "O" and prev_tag == "O":
            w[3] = "B-" + tag
            prev_tag = tag
        elif prev_tag != "O" and prev_tag == tag:
            w[3] = "I-" + tag
            prev_tag = tag
        elif prev_tag != "O" and prev_tag != tag:
            w[3] = "B-" + tag
            prev_tag = tag

# BIOES tagging
#for sc in total:
#    sc_len = len(sc)
#    for idx in range(sc_len):
#        if sc[idx][3] != "O":
#            tag = sc[idx][3].split('-')[-1]
#            if "B-" in sc[idx][3]:
#                if idx == sc_len-1 or "I-" not in sc[idx+1][3]:
#                    sc[idx][3] = "S-" + tag
#            elif "I-" in sc[idx][3]:
#                if idx == sc_len-1 or "I-" not in sc[idx+1][3]:
#                    sc[idx][3] = "E-" + tag                

with open(train_file, 'w', encoding='utf-8') as f:
    f.write('-DOCSTART-\t-X-\t-X-\t-X-\n\n')
    for sc in train:
        for w in sc:
            f.write('%s\t%s\t%d\t%s\n' % (w[0], w[1], w[2], w[3]))
        f.write('\n')

with open(dev_pos, 'w', encoding='utf-8') as f1, open(dev_name, 'w', encoding='utf-8') as f2:
    f1.write('-DOCSTART-\t-X-\t-X-\n\n')
    f2.write('-DOCSTART-\t-X-\n\n')
    for sc in dev:
        for w in sc:
            f1.write('%s\t%s\t%d\n' % (w[0], w[1], w[2]))
            f2.write('%s\t%s\n' % (w[0], w[3]))
        f1.write('\n')
        f2.write('\n')

with open(test_pos, 'w', encoding='utf-8') as f1, open(test_name, 'w', encoding='utf-8') as f2:
    f1.write('-DOCSTART-\t-X-\t-X-\n\n')
    f2.write('-DOCSTART-\t-X-\n\n')
    for sc in test:
        for w in sc:
            f1.write('%s\t%s\t%d\n' % (w[0], w[1], w[2]))
            f2.write('%s\t%s\n' % (w[0], w[3]))
        f1.write('\n')
        f2.write('\n')