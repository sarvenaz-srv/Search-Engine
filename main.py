from search_engine import index_creator
from search_engine.models.inverted_index import InvertedIndex
from search_engine.models.tfid_table import TFIDFTable, calc_diff
from search_engine.utils.utils import get_all_docs
from search_engine.constants import RESULT_COUNT

import time


def show_result(results):
    all_docs = get_all_docs()
    for i, result in enumerate(results):
        data = all_docs.get(result)
        print(f'{i}th result is {result}: {data.get("title")}, url: {data.get("url")}')
    

docs_tf_idf ,docs_inverted_index = index_creator.create_or_get_inverted_index(load=False)

# first_doc_content = "به گزارش خبرگزاری فارس، سردار آزمون ستاره تیم ملی کشورمان و عضو باشگاه زنیت به دلیل درخشش بی نظیرش در لیگ روسیه و نزدیک بودن زمان پایان قراردادش با باشگاه روسی مشتریان زیادی پیدا کرده است. سیماک سرمربی زنیت روز گذشته در مصاحبه با رسانه های روسیه اعلام کرد مسئله آینده آزمون آسان است این بازیکن قصد تمدید قراردادش را ندارد و در تابستان به باشگاه جدیدی می رود. در همین رابطه سایت «hitc» به تحلیل حرف های سرمربی زنیت پرداخت و این حرف ها را فرصتی استثنایی برای دو باشگاه اورتون و نیوکاسل دانست.  این رسانه انگلیسی، نوشت: سردار آزمون ستاره ایرانی زنیت در لیگ قهرمانان اروپا در یک بازی جذاب به کابوس هواداران چلسی تبدیل شد. این ستاره ایرانی یک گل فوق العاده در این بازی به ثمر رساند و اگر واکنش های فوق العاده کپه آ نبود می توانست چندین بار دیگر دروزاه شاگردان توخل را باز کند. ستاره ایرانی از دو سال گذشته بنا به اعلام مدیر برنامه اش از باشگاه اورتون با ریاست فرهاد مشیری ایرانی پیشنهاد داشته و یکی از گزینه های تقویت خط حمله این تیم است. از طرف دیگر نیوکاسل که در آستانه سقوط قرار دارد برای رهایی از این وضعیت بد می خواهد با مدیریت جدید سعودی ها سردار آزمون را جذب کند تا خط حمله اش جانی دوباره بگیرد.  قرارداد سردار آزمون تابستان پیش رو با زنیت به پایان می رسد و این بازیکن 17 میلیون پوندی به صورت رایگان به تیمی دیگر خواهد رفت. نیوکاسل و اورتون فرصتی طلایی برای جذب این بازیکن به صورت رایگان را دارند. البته مهاجم ملی پوش ایرانی از سوی باشگاه های یوونتوس، لیون و بایر لورکوزن نیز مورد توجه است و باید دید این بازیکن ایرانی 26 ساله چه تصمیمی برای آینده اش در تابستان می گیرد. آزمون از سال 2019 برای زنیت بازی می کند. ستاره ایرانی در مدت کمتر از 3 سال 3 بار قهرمانی لیگ برتر روسیه را تجربه کرد و یک بار نیز جایزه آقای گلی لیگ را از آن کرد. انتهای پیام/ "
# user_query = first_doc_content
user_query = input('please enter the query: ')

query_inverted_index = InvertedIndex()
index_creator.create_inverted_index(-1, user_query, query_inverted_index )
query_tf_idf_table = TFIDFTable(query_inverted_index)
query_tf_idf_table.calc_tf_idf(is_query=True)


start = time.time()


result = calc_diff(docs_tf_idf, query_tf_idf_table)

end = time.time()

show_result(result[:RESULT_COUNT])

print(end - start)

