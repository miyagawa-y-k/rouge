from collections import deque
import spacy

# ROUGE-L
class ROUGEL():
    #
    # init
    #
    def __init__(self):
        self.tokenizer = spacy.load("ja_ginza")
        self.stopwords = ['\r\n', '\n', '\n\n', '。']

    #
    # Split the input sentence with a stopword and return sentece list.
    #
    def sentences_split(self, sentence: str) -> list:
        token_queue = deque(list(sentence))
        # return
        sentences = []
        sentence = ""
        while token_queue:
            token = token_queue.popleft()
            if any([token == stopword for stopword in self.stopwords]):
                if len(sentence):
                    sentences.append(sentence)
                sentence = ""
            else:
                sentence += token
        if len(sentence):
            sentences.append(sentence)
        return sentences

    #
    # Splits the input a sentence and return token list.
    #
    def tokens_split(self, sentence: str) -> list:
        token_queue = deque(self.tokens_split_(sentence=sentence))
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

    # 
    # Split the sentence and return token list.
    #
    def tokens_split_(self, sentence: str) -> list:
        tokens = self.tokenizer(sentence)
        return [token.text for token in tokens]

    #
    # Calcuate LCS
    #
    def lcs(self, summary:str, reference:str) -> int:
        # lcs
        dp = [[0] * (len(reference)+1) for _ in range(len(summary)+1)]
        for i, token_i in enumerate(summary):
            for j, token_j in enumerate(reference):
                if token_i == token_j:
                    dp[i+1][j+1] = dp[i][j]+1
                else:
                    dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])
        return dp[len(summary)][len(reference)]

    #
    # Calcuate recall
    #
    def recall(self, summary:str, reference:str) -> float:
        lcs = self.lcs(summary, reference)
        return lcs/len(reference) if len(reference) else 0
    
    #
    # Calcuate precision
    #
    def precision(self, summary:str, reference:str) -> float:
        lcs = self.lcs(summary, reference)
        return lcs/len(summary) if len(summary) else 0
    
# ROUGE-N
class ROUGEN():
    #
    # init
    #
    def __init__(self, ngram:int = 1):
        self.tokenizer = spacy.load("ja_ginza")
        self.stopwords = ['\r\n', '\n', '\n\n', '。']
        self.ngram = ngram

    #
    # Split the input sentence with a stopword and return sentece list.
    #
    def sentences_split(self, sentence: str) -> list:
        token_queue = deque(list(sentence))
        # return
        sentences = []
        sentence = ""
        while token_queue:
            token = token_queue.popleft()
            if any([token == stopword for stopword in self.stopwords]):
                if len(sentence):
                    sentences.append(sentence)
                sentence = ""
            else:
                sentence += token
        if len(sentence):
            sentences.append(sentence)
        return sentences

    #
    # Splits the input a sentence and return token list.
    #
    def tokens_split(self, sentence: str) -> list:
        token_queue = deque(self.tokens_split_(sentence=sentence))
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

    # 
    # Split the sentence and return token list.
    #
    def tokens_split_(self, sentence: str) -> list:
        tokens = self.tokenizer(sentence)
        res = []
        for token_num in range(len(tokens)+1-self.ngram):
            res.append(tokens[token_num:token_num+self.ngram])
        return res

    #
    # Calcuate LCS
    #
    def calc_score(self, summary:str, reference:str) -> int:
        res_set = set(list(map(lambda x: str(x), reference)))
        sum_set = set(list(map(lambda x: str(x), summary)))
        intersction_set = sum_set & res_set
        res = len(intersction_set)
        print(f"intersection:{intersction_set}")
        return res

    #
    # Calcuate recall
    #
    def recall(self, summary:str, reference:str) -> float:
        match_ngram = self.calc_score(summary, reference)
        return match_ngram/len(reference) if len(reference) else 0
    
    #
    # Calcuate precision
    #
    def precision(self, summary:str, reference:str) -> float:
        match_ngram = self.calc_score(summary, reference)
        return match_ngram/len(summary) if len(summary) else 0