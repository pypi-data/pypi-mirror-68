import torch

CORPUS_NAME = 'cornell movie-dialogs corpus'
MAX_SENTENCE_LENGTH = 15
MIN_TRIM_WORD_COUNT = 3  # Minimum word count threshold for trimming

USE_CUDA = torch.cuda.is_available()
DEVICE = torch.device('cuda' if USE_CUDA else 'cpu')

MODEL_NAME = 'chatbot_model'
ATTN_MODEL = 'dot'
# ATTN_MODEL = 'general'
# ATTN_MODEL = 'concat'
HIDDEN_SIZE = 500
ENCODER_GRU_LAYERS = 2
DECODER_GRU_LAYERS = 2
