import re
import unicodedata
import torch
import itertools

from .voc import Voc, EOS_token, PAD_token


# turn a unicode string into asc ii
# https://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


# lowercase, trim, and remove non-letter characters except for
# basic punctuation
def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r'([.!?])', r' \1', s)
    s = re.sub(r'[^a-zA-Z.!?]+', r' ', s)
    s = re.sub(r'\s+', r' ', s).strip()
    
    return s

    
# read query/response pairs and return a Voc object
def readVocs(datafile, corpus_name):
    print('Reading q/a lines...')
    
    # read the file and split into lines
    lines = open(datafile, 'r', encoding='utf-8').read().strip().split('\n')
    # split every line into pairs and normalize
    qa_pairs = [
        tuple([normalizeString(sentence) for sentence in line.split('\t')])
        for line in lines
    ]
    voc = Voc(corpus_name)
    
    return voc, qa_pairs


# return true iff both sentences in a pair 'p' are under max_length(MAX_SENTENCE_LENGTH) threshold
def filterPair(p, max_length):
    # input sequences need to preserve the last word for EOS token
    return len(p[0].split(' ')) < max_length and \
        len(p[1].split(' ')) < max_length

    
# filter pairs using filterPair
def filterPairs(pairs, max_length):
    return [pair for pair in pairs if filterPair(pair, max_length)]


# using the helper function defined above, return a populated voc object and pairs list
def loadPrepareData(corpus_name, datafile, save_dir, max_length):
    print('Start preparing training data ...')
    voc, qa_pairs = readVocs(datafile, corpus_name)
    print('Read {!s} sentence pairs'.format(len(qa_pairs)))
    
    qa_pairs = filterPairs(qa_pairs, max_length)
    print('Trimmed to {!s} sentence pairs'.format(len(qa_pairs)))
    
    print('Counting words ...')
    for pair in qa_pairs:
        voc.addSentence(pair[0])
        voc.addSentence(pair[1])
    print('Counted words: ', voc.num_words)
    
    return voc, qa_pairs


def trimRareWords(voc, qa_pairs, min_count):
    voc.trim(min_count)
    
    kept_qa_pairs = []
    
    for pair in qa_pairs:
        q = pair[0]
        a = pair[1]
        should_keep = True
        
        for word in q.split(' '):
            if word not in voc.word2index:
                should_keep = False
                break
        
        if should_keep:
            for word in a.split(' '):
                if word not in voc.word2index:
                    should_keep = False
                    break
        
        if should_keep:
            kept_qa_pairs.append(pair)
    
    print('Trimmed from {} pairs to {}, {:.4f} of total'.format(
        len(qa_pairs), len(kept_qa_pairs), len(kept_qa_pairs) / len(qa_pairs)
    ))
    
    return kept_qa_pairs


def indexesFromSentence(voc, sentence):
    return [voc.word2index[word] for word in sentence.split(' ')] + [EOS_token]


# pad each encoded token list againist the longest one in the list
# and implicitly transpose
# e.g. 
# input: 
# [[1, 2, 3, 4],
#  [5, 6],
#. [3, 5, 8]]
# 
# output: 
# [(1, 5, 6)
#  (2, 6, 5),
#  (3, 0, 8),
#. (4, 0, 0)]
def zeroPadding(batch_of_encoded_sentences):
    return list(itertools.zip_longest(
        *batch_of_encoded_sentences,
        fillvalue=PAD_token
    ))


def binaryMatrix(padded_batch_of_encoded_sentences):
    m = []
    for i, seq in enumerate(padded_batch_of_encoded_sentences):
        m.append([])
        
        for token in seq:
            if token == PAD_token:
                m[i].append(0)
            else:
                m[i].append(1)
    
    return m
                

# convert batch of sentences (query sentence) to tensor, create a correctly shaped zero-padded tensor.
# it also returns a tensor of lengths for each of the sequences in the batch
def inputVar(batch_of_sentences, voc):
    batch_of_encoded = [indexesFromSentence(voc, sentence) for sentence in batch_of_sentences]
    lengths = [len(encoded_seq) for encoded_seq in batch_of_encoded]
    batch_of_padded_encoded = zeroPadding(batch_of_encoded)
    
    return torch.LongTensor(batch_of_padded_encoded), torch.tensor(lengths)
    

# convert batch of sentences (answer/target sentences) to tensor
def outputVar(batch_of_sentences, voc):
    batch_of_encoded = [indexesFromSentence(voc, sentence) for sentence in batch_of_sentences]
    max_target_length = max([len(encoded_seq) for encoded_seq in batch_of_encoded])
    batch_of_padded_encoded = zeroPadding(batch_of_encoded)
    mask = binaryMatrix(batch_of_padded_encoded)
    
    return torch.LongTensor(batch_of_padded_encoded), torch.BoolTensor(mask), max_target_length
    

# takes a bunch of pairs and returns the input and target tensors
def batch2TrainData(voc, pair_batch):
    pair_batch.sort(key=lambda x: len(x[0].split(' ')), reverse=True)
    input_batch, output_batch = [], []
    
    for pair in pair_batch:
        input_batch.append(pair[0])
        output_batch.append(pair[1])
        
    padded_encoded_input_batch, lengths = inputVar(input_batch, voc)
    padded_encoded_output_batch, mask, max_target_len = outputVar(output_batch, voc)
    
    return padded_encoded_input_batch, lengths,\
        padded_encoded_output_batch, mask, max_target_len

