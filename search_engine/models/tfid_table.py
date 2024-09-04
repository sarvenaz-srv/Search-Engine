from .inverted_index import InvertedIndex
import math

import pickle

class TFIDFTable:
    def __init__(self, inverted_index: InvertedIndex) -> None:
        self.__inverted_index = inverted_index
        self.__tf_idf = {}
        
    def get_tf_idf(self):
        return self.__tf_idf
    
    def get_inverted_index(self):
        return self.__inverted_index

    def get_docs(self, token: str):
        return self.__inverted_index.docs(token)
    
    def get_tf_of_doc_token(self, doc_id:int,token:str):
        return self.__tf_idf.get(doc_id, {}).get(token, 0)
        
    def get_token(self):
        return self.__inverted_index.tokens()
        
    def calc_tf_idf(self, is_query=False):
        for token in self.__inverted_index.tokens():
            for doc_id, doc_indices in self.__inverted_index.docs(token):
                if doc_id == 'freq':
                    continue
                tf_idf_of_doc = self.__tf_idf.get(doc_id, {})        
                tf = len(doc_indices)
                n = self.__inverted_index.token_df(token)
                if is_query:
                    tf_idf_of_doc[token] = math.log((1 + tf))  
                else:
                    tf_idf_of_doc[token] = math.log((1 + tf)) * (math.log(self.__inverted_index.number_all_docs()/n)) 
                if tf_idf_of_doc[token] == 0:
                    print(f'tf idf for {token} in {doc_id} is 0')
                self.__tf_idf[doc_id] = tf_idf_of_doc
        
    
    def print_max_and_min_idf(self):
        maxIdf = -1 * math.inf
        maxToken = None
        
        minIdf = math.inf
        minToken = None
        
        for token in self.__inverted_index.tokens():
            df = math.log(self.__inverted_index.number_all_docs()/(self.__inverted_index.token_df(token)))
            if df > maxIdf:
                maxIdf = df
                maxToken = token
            if df < minIdf:
                minIdf = df
                minToken = token
                
        print("Min: ", minToken, " idf = ", minIdf)
        print("Max: ", maxToken, " idf =  ", maxIdf)
        
    def print_doc_weights_info(self, doc_id):
        weights = self.__tf_idf.get(doc_id)
        # print((weights.keys()))
        maxWeight = -1 * math.inf
        maxToken = None
        
        minWeight = math.inf
        minToken = None
        
        for t in weights.keys():
            if(weights.get(t) > maxWeight):
                maxToken = t
                maxWeight = weights.get(t)
            if(weights.get(t) < minWeight):
                minToken = t
                minWeight = weights.get(t)
        print("Min: ", minToken, " Weight = ", minWeight)
        print("Max: ", maxToken, " Weight = ", maxWeight)
                
            
        
    def save(self, path: str ='tfidf.in'):
        with open(path, 'wb') as dictionary_file:
            pickle.dump(self, dictionary_file)
    
    @staticmethod
    def load(path='./tfidf.in'):
        with open(path, 'rb') as dictionary_file:
            tfidftable = pickle.load(dictionary_file)
        return tfidftable
    
def calc_diff(docs_tf_idf: TFIDFTable, query_tf_idf: TFIDFTable):
    result = {}
    for query_token in query_tf_idf.get_token():
        print(f'query token is {query_token}')
        qt_tf_idf = query_tf_idf.get_tf_of_doc_token(-1, query_token)
        print(f'tf of it is {qt_tf_idf}')

        for candidate_doc_id,  indices in docs_tf_idf.get_docs(query_token):
            # print(f'candidate_doc_id {candidate_doc_id}')
            d_tf_id = docs_tf_idf.get_tf_of_doc_token(candidate_doc_id, query_token)
            # print(f'tf of it{d_tf_id}')
            if d_tf_id == 0 or qt_tf_idf == 0:
                print('an invalid state')
            temp = result.get(candidate_doc_id, 0)
            temp += qt_tf_idf * d_tf_id
            # print(f'temp is {temp}')
            result[candidate_doc_id] = temp
            # break
        # break
    result = sorted(result, key=lambda item: result[item], reverse=True)
    return result
        
                