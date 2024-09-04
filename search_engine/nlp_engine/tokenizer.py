from search_engine.models.token import Token

def tokenize_content(content: str) -> list[Token]:
    tokens = []
    for index, token in enumerate(content.split()):
        tokens.append(Token(token, index))
    return tokens
