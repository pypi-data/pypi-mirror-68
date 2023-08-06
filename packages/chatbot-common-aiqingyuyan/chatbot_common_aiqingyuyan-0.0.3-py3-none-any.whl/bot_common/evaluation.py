from .models.encoder_rnn import EncoderRNN
from .models.decoder_rnn import LuongAttnDecoderRNN
from .text_processing.voc import SOS_token
from .text_processing.voc import Voc
from .text_processing.utils import indexesFromSentence
from .constants import MAX_SENTENCE_LENGTH
from .constants import DEVICE

import torch
import torch.nn as nn
import os
# import constants


# Computation Graph:
# 1. Forward input through encoder model
# 2. Prepare encoder's final hidden output to be first hidden input to the decoder
# 3. Initialize decoder's first input as SOS_token
# 4. Initialize tensors to append decoded words to
# 5. Iteratively decode one word token at a time:
#      5.1 Forward through decoder
#      5.2 Obtain most likely word token and its softmax score
#      5.3 Record token and score
#      5.4 Prepare current token to be next docoder input
# 6. Return collections of word tokens and scroes

class GreedySearchDecoder(nn.Module):
    
    def __init__(self, encoder, decoder, device):
        super(GreedySearchDecoder, self).__init__()
        
        self.encoder = encoder
        self.decoder = decoder
        self.device = device
    
    
    def forward(self, input_seq, input_seq_length, max_length):
        """
        Parameters:
        
        - input_seq: shape of (len(input_seq), 1);
                     encoded input sequence (sentence) token
        - input_seq_length: shape of (1);
                            length of input_seq as a tensor of list, size of 1,
                            mainly to fit encoder forward method requirements,
                            which has a `lengths` parameter taking a tensor of 1-dim list;
                            len(input_seq) == input_seq_length.item()
        - max_length: used to bound response sentence length
        """
        # forward input through encoder model
        encoder_outputs, encoder_hidden = self.encoder(input_seq, input_seq_length)
        # prepare encoder's final hidden output to be first hidden input to the decoder
        decoder_hidden = encoder_hidden[:self.decoder.gru_layers]
        # initialize decoder's first input as SOS_token
        # shape of (1, 1), since decoder is feeded one time step at a time
        decoder_input = torch.LongTensor([[SOS_token]]).to(self.device)
        # initialize tensors to append decoded words to
        all_tokens = torch.zeros([0], device=self.device, dtype=torch.long)
        all_scores = torch.zeros([0], device=self.device)
        # Iteratively decode one word token at a time:
        for _ in range(max_length):
            # Forward pass through decoder
            # - decoder_outputs: shape of (1, vocabulary_size);
            decoder_outputs, decoder_hidden = \
                self.decoder(decoder_input, decoder_hidden, encoder_outputs)
            # Obtain most likely word token and its softmax score
            # - decoder_scores: shape of (1)
            # - decoder_input: shape of (1)
            decoder_scores, decoder_input = torch.max(decoder_outputs, dim=1)
            # append token and score
            all_tokens = torch.cat((all_tokens, decoder_input), dim=0)
            all_scores = torch.cat((all_scores, decoder_scores), dim=0)
            # Prepare current token to be next docoder input
            # - unsqueeze: change shape from (1) to (1, 1)
            decoder_input = torch.unsqueeze(decoder_input, 0)
        
        # Return collections of word tokens and scroes
        return all_tokens, all_scores


def evaluate(encoder, decoder, searcher, voc, sentence, max_length=MAX_SENTENCE_LENGTH):
    """
    Parameters:
    
    - encoder: an instance of EncoderRNN
    - decoder: an instance of LuongAttnDecoderRNN
    - searcher: an instance of GreedySearchDecoder
    """
    # Format input sentence as a batch
    # - words to indices
    indices_batch = [indexesFromSentence(voc, sentence)]
    # Create lengths tensor
    lengths = torch.tensor([len(indices) for indices in indices_batch]).to(DEVICE)
    # Transpose dimensions of indices_batch to match encoder model's expectations
    # - from (1, input sentence length) to (input sentence length, 1)
    batch_input = torch.LongTensor(indices_batch).transpose(0, 1).to(DEVICE)
    # Decode sentence with searcher
    out_tokens, scores = searcher(batch_input, lengths, max_length)
    # Indices to words
    final_words = [voc.index2work[word_idx.item()] for word_idx in out_tokens]
    
    return final_words
