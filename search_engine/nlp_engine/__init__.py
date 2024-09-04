from .normalizer import normalize_content
from .tokenizer import tokenize_content
from .stemmer import stem_tokens

def get_processed_tokens(id: int, content: str):
    # print(f'starting of pre process doc: {id}')
    content = normalize_content(content)
    # print("Normalized: ", content )
    tokens = tokenize_content(content)
    # print("Tokenized: ", tokens)
    # printed_tokens = []
    # for t in tokens:
    #     printed_tokens.append(t._token)
    # print("Tokens: ", printed_tokens)
    stems = stem_tokens(tokens)
    # printed_stems = []
    # for s in stems:
    #     printed_stems.append(s._token)
    # print("Stems: ", printed_stems)
    return stems