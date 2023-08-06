import torch
import torch.nn as nn
import torch.nn.functional as F

from .attention import Attention


class LuongAttnDecoderRNN(nn.Module):
    
    def __init__(self, attn_model, embedding, hidden_size, output_size, gru_layers=1, dropout=0.1):
        """
        Parameters:
        - output_size: vocabulary size
        """
        super(LuongAttnDecoderRNN, self).__init__()
        
        self.attn_model = attn_model
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.gru_layers = gru_layers
        self.dropout = dropout
        
        # define layers
        self.embedding = embedding
        self.embedding_dropout = nn.Dropout(dropout)
        self.gru = nn.GRU(
            hidden_size,
            hidden_size,
            gru_layers,
            dropout=(0 if gru_layers == 1 else dropout)
        )
        self.concat = nn.Linear(hidden_size * 2, hidden_size)
        self.out = nn.Linear(hidden_size, output_size)
        
        self.attn = Attention(attn_model, hidden_size)
        
    
    def forward(self, input_step, last_hidden, encoder_outputs):
        """
        Parameters:
        - input_step: one time step (one word) of input sequence batch;
                      shape of (1, batch_size)
                      first time step to decoder will be `SOS_Token` in each column
                      [[SOS_Token, SOS_Token, ... SOS_Token]]
        - last_hidden: last GRU layer's hidden output
                      shape (gru_layers * num_directions, batch_size, hidden_size)
        - encoder_outputs: (max_seq_length, batch_size, hidden_size)
                            max_seq_length: max sequence ((query) sentence) length 
                            in this batch
                            
        Return: tupe(output, hidden)
        
        - output: (batch_size, output_size);
                   predicted softmax output, each row represents a prediction
                   for an input query word in this time step batch (input_step);
                   column represents the probablitiy for each word in vocabulary
        - hidden: (gru_layers * num_directions, batch_size, hidden_size);
                   current GRU's hidden output
        """
        # Note: we run this one step (word) at a time
        # get embbedding of current input
        embedded = self.embedding(input_step)
        embedded = self.embedding_dropout(embedded)
        # forward through unidirectional GRU
        # - rnn_output: (1, batch_size, hidden_size)
        rnn_output, hidden = self.gru(embedded, last_hidden)
        # calculate attention weights from the current GRU output
        attn_weights = self.attn(rnn_output, encoder_outputs)
        # multiply attention weights to encoder outputs to get 
        # new "weighted sum" context vector
        # - bmm: batch matrix multiplication, after transpose
        #   encoder_outputs will be (batch_size, max_seq_length, hidden_size)
        #   attn_weights will be (batch_size, 1, max_seq_length)
        #   result will be (batch_size, 1, hidden_size)
        context = attn_weights.bmm(encoder_outputs.transpose(0, 1))
        # concatenate weighted context vector and GRU output using Luong eq. 5
        # - rnn_output will be (batch_size, hidden_size)
        rnn_output = rnn_output.squeeze(0)
        # - context will be (batch_size, hidden_size)
        context = context.squeeze(1)
        # - concat_input will be (batch_size, hidden_size * 2)
        concat_input = torch.cat((rnn_output, context), 1)
        concat_output = torch.tanh(self.concat(concat_input))
        # predict next word using Luong eq. 6
        output = self.out(concat_output)
        output = F.softmax(output, dim=1)
        
        return output, hidden
