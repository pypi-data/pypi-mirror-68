import torch
import torch.nn as nn
import torch.nn.functional as F


class Attention(nn.Module):
    
    AVAILABLE_METHODS = ['dot', 'general', 'concat']
    
    def __init__(self, method, hidden_size):
        super(Attention, self).__init__()
        
        if method not in Attention.AVAILABLE_METHODS:
            raise ValueError(self.method, 'is not an appropriate attention method')
        
        self.method = method
        self.hidden_size = hidden_size
        
        if self.method == 'general':
            self.attn = nn.Linear(hidden_size, hidden_size)
        elif self.method == 'concat':
            self.attn = nn.Linear(hidden_size * 2, hidden_size)
            self.v = nn.Parameter(torch.FloatTensor(hidden_size))
    
    
    def dot_score(self, decoder_output, encoder_outputs):
        """
        sum across the columns for each sample in the batch
        result in (seq_len (max_sen_length), batch_size) shape result
        """
        return torch.sum(decoder_output * encoder_outputs, dim=2)
    
    
    def general_score(self, decoder_output, encoder_outputs):
        """
        first go through a attention layer (transformation)
        then element wise prod, and sum across the columns for each sample in the batch
        """
        energies = self.attn(encoder_outputs)
        return torch.sum(decoder_output * energies, dim=2)
    
    
    def concat_score(self, decoder_output, encoder_outputs):
        """
        first concat hidden with encoder_outputs
        then go through attention layer (transformation), then go throgh tanh activation
        then element wise prod with parameter v, and sum across the columns for each sample in the batch
        """
        seq_len = encoder_outputs.size()[0]
        # after concat, shape become (seq_len, batch_size, 2 * hidden_size)
        # basically, columns (feature_size doubled) for each sample in the batch
        concated = torch.cat(
            (decoder_output.expand(seq_len, -1, -1), encoder_outputs),
            dim=2
        )
        energies = self.attn(concated).tanh()
        return torch.sum(self.v * energies, dim=2)
        
        
    def forward(self, decoder_output, encoder_outputs):
        """
        calculate attention weights (energies) based on the given method
        
        Parameters:
        - decoder_output: current decoder GRU output, since we feed batch to decoder 
                  1 timestep (shape: (1, batch_size)) at a time, then its 
                  output will be shape of (1, batch_size, hidden_size), thus
                  decoder_output will be (1, batch_size, hidden_size)
        - encoder_outputs: (max_seq_length, batch_size, hidden_size)
                            max_seq_length: max sequence ((query) sentence) length 
                            in this batch
        
        Return:
        - softmax: (batch_size, 1, hidden_size)
        """
        if self.method == 'general':
            attn_weights = self.general_score(decoder_output, encoder_outputs)
        elif self.method == 'concat':
            attn_weights = self.concat_score(decoder_output, encoder_outputs)
        elif self.method == 'dot':
            attn_weights = self.dot_score(decoder_output, encoder_outputs)
        
        # transpose (seq_len (max_sen_length), batch_size)
        # after transpose: (batch_size, seq_len (max_sen_length))
        attn_weights = attn_weights.t()
        
        # apply softmax across columns (dim=1) for each sample (row) in the batch
        # basically each token in a seq sample gets a attn weight value in the batch
        # and then add a dimension, results in (batch_size, 1, seq_len (max_sen_length)) shape
        return F.softmax(attn_weights, dim=1).unsqueeze(1)
