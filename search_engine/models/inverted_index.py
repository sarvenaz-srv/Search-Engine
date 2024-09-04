from .token import Token
import pickle

class InvertedIndex:
    def __init__(self) -> None:
        self.__inverted = {}
        self.__champion = {}
        self.__doc_ids = set()
        
    def number_all_docs(self):
        return len(self.__doc_ids) ##     
    
    def inverted_index(self):
        return self.__inverted
    
    def tokens(self):
        return self.__inverted.keys()
    
    def champion(self):
        return self.__champion
    
    def docs(self, token: str) -> dict:
        return self.__inverted.get(token, {}).items()
    
    def get_stop_words(self, limit: int = 50) -> list[str] and list[int]:
        sorted_keys = sorted(self.__inverted.keys(), key=lambda item : self.token_tf(item), reverse=True)
        return sorted_keys[:limit], [self.token_tf(t) for t in sorted_keys[:limit]]
    
    def remove_stop_words(self, limit: int = 50):
        stop_words, freqs = self.get_stop_words(limit)
        for word in stop_words:
            self.__inverted.pop(word)
        return stop_words, freqs

    def token_tf(self, token: str):
        token_docs = self.__inverted.get(token, {})
        return token_docs.get('freq', 0)
    
    def token_df(self, token: str):
        token_docs = self.__inverted.get(token, {})
        return max(len(token_docs.keys()) - 1, 0) # remove `freq` term from keys 

    def create_champion(self, r:int):
        self.__champion = {}
        for key, item in self.__inverted.items():
            freq = self.__inverted.get(key).pop('freq')
            sorted_doc_by_tf = sorted(item.items(), key=lambda k: len(k[1]), reverse=True)
            self.__inverted.get(key)['freq'] = freq
            self.__champion[key] = list(dict(sorted_doc_by_tf[:r]).keys())
             
    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        string = ''
        for term in self.__inverted.keys():
            string += f"{term}: \n"
            for doc_id in self.__inverted[term]:
                string += f"{str(doc_id)} : {str(self.__inverted[term][doc_id])}\n"
            string += "\n"

        return string
    
    def token_exist(self, token: str):
        return token in self.__inverted
    
    def add_token(self, token:Token, doc_id: int):
        token_docs = self.__inverted.get(token._token, {})
        freq = token_docs.get('freq', 0)
        token_docs['freq'] = freq + 1
        token_indices = token_docs.get(doc_id, [])          
        token_indices.append(token._index)
        token_docs[doc_id] = token_indices
        self.__inverted[token._token] = token_docs
        self.__doc_ids.add(doc_id)
    
    def add_tokens(self, tokens: list[Token], doc_id: int):
        for token in tokens:
            self.add_token(token, doc_id)
            
    def save(self, path: str ='inverted.in'):
        with open(path, 'wb') as dictionary_file:
            pickle.dump(self, dictionary_file)
            
    def print_common_tokens(self, limit: int = 3):
        sorted_keys = sorted(self.__inverted.keys(), key=lambda item : self.token_df(item), reverse=True)
        print(sorted_keys[:limit], [self.token_df(t) for t in sorted_keys[:limit]])
        
            
    def print_least_common_tokens(self, limit: int = 3):
        sorted_keys = sorted(self.__inverted.keys(), key=lambda item : self.token_df(item))
        print(sorted_keys[:limit], [self.token_df(t) for t in sorted_keys[:limit]])
        print(sorted_keys[0])
        print(self.__inverted.get(sorted_keys[0]))
        
    def print_dict_size(self):
        print(len(self.__inverted.keys()))
        print('freq' in self.__inverted.keys())
        
    @staticmethod
    def load(path='./inverted.in'):
        with open(path, 'rb') as dictionary_file:
            inverted = pickle.load(dictionary_file)
        return inverted
    

