import string

class FeatureBuilder:
    def __init__(self, file_name, train=False):
        path = "./KOREAN_NAME_CORPUS/"
        self.in_file = path + file_name
        self.out_file = "./outputs/" + file_name[0:file_name.find(".")] + \
                        ".feature"
        self.w_file = open(self.out_file, 'w', encoding='utf-8')
        self.train = train

    def write_features(self, token, feature, tag):
        out_line = token
        for f in feature:
            out_line = out_line + "\tfeature=" + str(f)
        if self.train:
            out_line = out_line + "\t" + str(tag)
        self.w_file.write(out_line + "\n")

    def build_features(self, sentence):
        for idx, items in enumerate(sentence):
            pre_tag = "@@"
            
            if idx > 1:
                pre2 = sentence[idx-2]
            else:
                pre2 = ["None", "*S*", None, "@@"]
            if idx > 0:
                pre = sentence[idx-1]
            else:
                pre = ["None", "*S*", None, "@@"]
            if idx < len(sentence) - 1:
                post = sentence[idx+1]
            else:
                post = ["None", "*E*", None, None]
            if idx < len(sentence) - 2:
                post2 = sentence[idx+2]
            else:
                post2 = ["None", "*E*", None, None]
            
            if self.train:
                cur_token, cur_pos, cur_eoj, cur_tag = items
                pre2_token, pre2_pos, pre2_eoj, pre2_tag = pre2
                pre_token, pre_pos, pre_eoj, pre_tag = pre
                post_token, post_pos, post_eoj, post_tag = post
                post2_token, post2_pos, post2_eoj, post2_tag = post2
            else:
                for p in [pre2, pre, post, post2]:
                    if len(p) == 4:
                        p.pop()
                cur_token, cur_pos, cur_eoj = items
                pre2_token, pre2_pos, pre2_eoj = pre2
                pre_token, pre_pos, pre_eoj = pre
                post_token, post_pos, post_eoj = post
                post2_token, post2_pos, post2_eoj = post2          

            token_len = len(cur_token)
            token_shape = ""
            for ch in cur_token:
                if ord('가') <= ord(ch) <= ord('힣'):
                    token_shape += "k"
                elif ord(u'\u4e00') <= ord(ch) <= ord(u'\u9fff'):
                    token_shape += "c"
                elif ord('a') <= ord(ch.lower()) <= ord('z'):
                    token_shape += "e"
                elif ch.isdigit():
                    token_shape += "d"
                else:
                    token_shape += "p"

            prefix = cur_token[:1]
            suffix = cur_token[-1:]
            
            features_list = [pre2_token, pre_token, cur_token, post_token, 
                             post2_token, cur_pos, cur_eoj, pre_pos, pre_eoj, 
                             post_pos, post_eoj, token_len, token_shape, 
                             prefix, suffix, pre_tag]

            features = [f for f in features_list]

            if cur_token == "-DOCSTART-":
                features = ["-X-" for i in range(len(features_list))]

            if self.train:
                self.write_features(cur_token, features, cur_tag)
            else:
                self.write_features(cur_token, features, None)

        self.w_file.write("\n")

    def run(self):
        sentence = []
        with open(self.in_file, 'r', encoding='utf-8') as fp:
            for line in fp:
                line = line.strip().split("\t")
                if len(line) == 1:
                    self.build_features(sentence)
                    sentence = []
                else:
                    sentence.append(line)
        self.w_file.close()
        print("Finished feature building. Output path: " + self.out_file)


if __name__ == '__main__':
    builder = FeatureBuilder("KOR_train.pos-name", train=True)
    builder.run()

    builder_dev = FeatureBuilder("KOR_dev.pos")
    builder_dev.run()

    builder_test = FeatureBuilder("KOR_test.pos")
    builder_test.run()
