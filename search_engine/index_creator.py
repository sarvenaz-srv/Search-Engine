
from .utils.utils import get_all_docs
from .nlp_engine import get_processed_tokens
from .models.inverted_index import InvertedIndex
from .models.token import Token
from .models.tfid_table import TFIDFTable

def save_stop_words(stop_words: list[str], freqs: list[int]):
    with open('stop_words.txt', 'w', encoding='utf-8') as f:
        f.write(str(stop_words))
        f.write('\n')
        f.write(str(freqs))
        

def get_news_content(doc: dict) -> str:
    # print("Content: ", doc.get("content", "") )
    return doc.get("content", "")    

def create_inverted_index(id: int, content: str, inverted_index: InvertedIndex):
    processed_tokens : list[Token] = get_processed_tokens(id, content)
    inverted_index.add_tokens(processed_tokens, id)
    

def __create_inverted_index_for_docs(docs: dict) -> InvertedIndex:
    inverted_index = InvertedIndex()
    for id, doc in docs.items():
        create_inverted_index(id, get_news_content(doc), inverted_index)
        # break;
    
    stop_words, freqs = inverted_index.remove_stop_words(50)
    save_stop_words(stop_words, freqs)
    
    inverted_index.create_champion(10)
    
    # inverted_index.print_common_tokens()
    # inverted_index.print_least_common_tokens()
    # inverted_index.print_dict_size()
    
    inverted_index.save()
    return inverted_index

def create_or_get_inverted_index(load=False):
    if load:
        inv = InvertedIndex.load()
        print('loaded')
        docs_tf_idf = TFIDFTable.load()
    else:
        docs = get_all_docs()
        inv = __create_inverted_index_for_docs(docs=docs)
        docs_tf_idf = TFIDFTable(inv)
        docs_tf_idf.calc_tf_idf()
        # docs_tf_idf.print_max_and_min_idf()
        # docs_tf_idf.print_doc_weights_info('4092')
        docs_tf_idf.save()
    return docs_tf_idf, inv

        
    