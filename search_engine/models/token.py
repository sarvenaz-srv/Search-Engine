class Token:
    def __init__(self, token: str, index: int) -> None:
        self._token : str = token
        self._index : int= index

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self._token} : {self._index}\n"

    def __eq__(self, other):
        return self._token == other.token

    def change_token(self, token):
        self._token = token

 