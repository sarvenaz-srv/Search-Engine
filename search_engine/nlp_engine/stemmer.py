from search_engine.models.token import Token
from hazm import Stemmer


def stem_tokens(tokens: list[Token]):
    stemmer: Stemmer = Stemmer()
    # stems = [stemmer.stem(token._token) 
    for token  in tokens:
        token.change_token(stemmer.stem(token._token))
    return tokens
