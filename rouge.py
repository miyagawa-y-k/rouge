# ROUGE-Lの実装
class ROUGEL():
    def __init__(self, tokenizer):
        # spacy
        self.tokenizer = tokenizer
        self.stopwords = ['\r\n', '\n', '\n\n', '。']

    def sentences_split(self, sentence):
        tokens = self.tokenizer(sentence)
        token_queue = deque([token.text for token in tokens])
        # return
        sentences = []
        sentence =[]
        while token_queue:
            token = token_queue.popleft()
            if any([token == stopword for stopword in self.stopwords]):
                if len(sentence):
                    sentences.append(sentence)
                sentence = []
            else:
                sentence.append(token)
        if len(sentence):
            sentences.append(sentence)
        return sentences

    def tokens_split(self, sentence=None):
        tokens = self.tokenizer(sentence)
        return [token.text for token in tokens]

    def lcs(self, summary=None, reference=None):
        # lcs
        dp = [[0] * (len(reference)+1) for _ in range(len(summary)+1)]
        for i, token_i in enumerate(summary):
            for j, token_j in enumerate(reference):
                if token_i == token_j:
                    dp[i+1][j+1] = dp[i][j]+1
                else:
                    dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])
        return dp[len(summary)][len(reference)]

    def recall(self, summary=None, reference=None):
        lcs = self.lcs(summary, reference)
        return lcs/len(reference)
    
    def precision(self, summary=None, reference=None):
        lcs = self.lcs(summary, reference)
        return lcs/len(summary)

    # 自分用
    def eval_recall(self, summary=None, reference=None):
        sumaries = self.sentences_split(summary)
        ref_tokens = self.tokens_split(reference)
        res = 0
        for summary in sumaries:
            res = max(res, self.recall(summary, ref_tokens))
        return res

    # 自分用
    def eval_precision(self, summary=None, reference=None):
        sumaries = self.sentences_split(summary)
        ref_tokens = self.tokens_split(reference)
        res = 0
        for summary in sumaries:
            res = max(res, self.precision(summary, ref_tokens))
        return res