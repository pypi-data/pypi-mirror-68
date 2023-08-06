import torch.nn as nn


class EncoderRNN(nn.Module):
    
    def __init__(self, embedding, hidden_size, gru_layers=1, dropout=0):
        """
        embedding: embedding transforming layer passed in, feature_size == hidden_size
        """
        super(EncoderRNN, self).__init__()
        
        self.embedding = embedding
        self.hidden_size = hidden_size
        self.gru_layers = gru_layers
        self.dropout = dropout

        self.gru = nn.GRU(
            hidden_size,
            hidden_size,
            gru_layers,
            dropout=(0 if gru_layers == 1 else dropout),
            bidirectional = True
        )
    
    
    def forward(self, batch_seqs, seq_lengths_in_batch, hidden=None):
        """
        Parameters:
        
        - batch_seqs: input features, batch of encoded sequences, shape of (max_seq_length, batch_size)
                      max_seq_length: max sequence ((query) sentence) length in this batch
        - seq_length_in_batch: length of each sequence in batch, shape of (batch_size)
        - hidden: hidden_state, shape of (num_layers x num_directions, batch_size, hidden_size)
        
        
        output: tuple(outputs, hidden)
        
        - outputs: output features from last hidden layer of GRU (sum of bidirectional outputs)
                   shape of (max_seq_length, batch_size, hidden_size)
                   max_seq_length: max sequence ((query) sentence) length in this batch
        - hidden: updated hidden_state after going through GRUs
                  shape of (gru_layers * num_direction, batch_size, hidden_size)
        """
        # convert batch of encoded sequences into embeddings
        batch_embedded = self.embedding(batch_seqs)
        
        # pack padded batch of sequences
        batch_packed_embedded = nn.utils.rnn.pack_padded_sequence(batch_embedded, seq_lengths_in_batch)
        
        # forward through gru
        # outputs: shape of (max_seq_length, batch_size, num_direction x hidden_size)
        outputs, hidden = self.gru(batch_packed_embedded, hidden)
        
        # unpack padding
        outputs, _ = nn.utils.rnn.pad_packed_sequence(outputs)
        
        # sum bidirectional GRU outputs
        outputs = outputs[:, :, :self.hidden_size] + outputs[:, :, self.hidden_size:]
        
        return outputs, hidden
