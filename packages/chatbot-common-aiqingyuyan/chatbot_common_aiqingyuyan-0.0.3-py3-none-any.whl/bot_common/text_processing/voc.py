PAD_token = 0  # used for padding short sentences
SOS_token = 1
EOS_token = 2


class Voc:
    
    def __init__(self, name):
        self.name = name
        self.trimmed = False
        self.word2index = {}
        self.word2count = {}
        self.index2work = {PAD_token: 'PAD', SOS_token: 'SOS', EOS_token: 'EOS'}
        self.num_words = 3 # SOS, EOS, PAD
        

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)
    
    
    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_words
            self.word2count[word] = 1
            self.index2work[self.num_words] = word
            self.num_words += 1
        else:
            self.word2count[word] += 1
        
        
    # remove words below a certain count threshold
    def trim(self, min_count_threshold):
        if self.trimmed:
            return
        
        words_kept = []
        for word, count in self.word2count.items():
            if count >= min_count_threshold:
                words_kept.append(word)
        
        print(
            'words_kept {} / {} = {:.4f}'
                .format(len(words_kept), len(self.word2count), len(words_kept) / len(self.word2count))
        )
        
        # reinitialize dictionaries after trimming
        self.word2index = {}
        self.word2count = {}
        self.index2work = {PAD_token: 'PAD', SOS_token: 'SOS', EOS_token: 'EOS'}
        self.num_words = 3
        
        # re-adding words
        for word in words_kept:
            self.addWord(word)
            
        self.trimmed = True
