from .utils import compile_patterns
import re 

space_after, space_before = r'\.:!\?؛؟،»\]\)\}', r'«\[\(\{'

character_refinement_patterns = compile_patterns([
    (r' {2,}', ' '),  # حذف اسپیس‌های اضافه
    (r'\n{3,}', '\n'),  # خذف خط جدیدهای اضافه
    (r"\u200a", ""),
    (r"\u200b", ""),
    (r"\u200d", ""),
    (r"\u200f", ""),
    (r"\u200e", ""),
    (r"\u200c{1,} ", " "),  # remove unneded ZWNJs before space
    (r" \u200c{1,}", " "),  # remove unneded ZWNJs after space
    (r"\b\u200c*\B", ""),  # remove unneded ZWNJs at the beginning of words
    (r"\B\u200c*\b", ""),  # remove unneded ZWNJs at the end of words
    (r'[ـ\r]', ''),  # حذف حالت کشیده حرف
    ('"([^\n"]+)"', r'«\1»'),  # جایگذاری گیومه به جای کوت
    ('([\d+])\.([\d+])', r'\1٫\2'),  # جایگذاری ممیز به جای نقطه در اعداد ممیزی
    # حذف فتحه، کسره، ضمه، تنوین و ...
    ('[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652]', ''),
])


space_of_letters_patterns = compile_patterns([
# remove space before and after quotation
    ('" ([^\n"]+) "', r'"\1"'),
    (" ([" + space_after + "])", r"\1"),  # remove space before
    ("([" + space_before + "]) ", r"\1"),  # remove space after
    # put space after . and :
    (
        "([" + space_after[:3] + "])([^ " + space_after + r"\d۰۱۲۳۴۵۶۷۸۹])",
        r"\1 \2",
    ),
    (
        "([" + space_after[3:] + "])([^ " + space_after + "])",
        r"\1 \2",
    ),  # put space after
    (
        "([^ " + space_before + "])([" + space_before + "])",
        r"\1 \2",
    ),  # put space before
    # put space after number; e.g., به طول ۹متر -> به طول ۹ متر
    (r"(\d)([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])", r"\1 \2"),
    # put space after number; e.g., به طول۹ -> به طول ۹
    (r"([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d)", r"\1 \2"),
])


unicode_replacements = [
    ## جایگذاری برخی از کلمات دو شکل
    ("﷽", "بسم الله الرحمن الرحیم"),
    ("﷼", "ریال"),
    ("(ﷰ|ﷹ)", "صلی"),
    ("ﷲ", "الله"),
    ("ﷳ", "اکبر"),
    ("ﷴ", "محمد"),
    ("ﷵ", "صلعم"),
    ("ﷶ", "رسول"),
    ("ﷷ", "علیه"),
    ("ﷸ", "وسلم"),
    ("ﻵ|ﻶ|ﻷ|ﻸ|ﻹ|ﻺ|ﻻ|ﻼ", "لا"),
]


half_space_patterns = compile_patterns([
    (r'([^ ]ه) ی ', r'\1‌ی '),  # حذف ی اسپیس: خانه ی پدری
    # قراردادن نیم‌فاصله بعد از نمی و می
    (r'(^| )(ن?می) ', r'\1\2‌'),
    # قرار دادن نیمفاصله قبل از تر, تری, ترین, گر, گری, ها, های
    (r'(?<=[^\n\d ' + space_after + space_before + \
        ']{2}) (تر(ین?)?|گری?|های?)(?=[ \n' + space_after + space_before + ']|$)', r'‌\1'),
    # join ام, ایم, اش, اند, ای, اید, ات
    (r'([^ ]ه) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n' + \
        space_after + ']|$)', r'\1‌\2'),
    (r'‌ ','‌'), # حذف اسپیس بعد از نیمفاصله
    (r' ‌','‌'), # حذف اسپیس قبل نیم‌فاصله
])


def maketrans(A, B): return dict((ord(a), b) for a, b in zip(A, B))

def fix_persian_style(content: str) -> str:
    translation_src, translation_dst = ' ىكي“”', ' یکی""' ## اصلاح ک و ی عربی
    translation_src += '0123456789%' ## جایگذاری اعداد انگلیسی با فارسی
    translation_dst += '۰۱۲۳۴۵۶۷۸۹٪'
    translation_src += 'آ' # اصلاح آ و ا
    translation_dst += 'ا'
    translations = maketrans(translation_src, translation_dst)
    content = content.translate(translations)

    for pattern, repl in character_refinement_patterns:
        content = pattern.sub(repl, content)
        
    for old, new in unicode_replacements:
        content = re.sub(old, new, content)
        

    return content


def fix_half_space(content: str) -> str:
    ## حل مشکلات نیم‌فاصله
    for pattern, repl in half_space_patterns:
        content = pattern.sub(repl, content)
    return content


def fix_space_of_letters(content: str) -> str:
    """حل مشکلات فاصله"""
    for pattern, repl in space_of_letters_patterns:
        content = pattern.sub(repl, content)
    return content



def punc_normalize(content: str)-> str:
    removed_special_chars = content.translate(
        {ord(c): '' for c in "!@#$%^&*()«»\"\'[]{};؛:٫,.،/<>?؟\|`~-=_+٪"})  # حذف حروف خاص
    return removed_special_chars


def normalize_content(content: str) -> str:
    content = fix_persian_style(content)
    content = fix_half_space(content)
    content = fix_space_of_letters(content)
    content = punc_normalize(content)
    return content

if __name__ == '__main__':
    # text = '''به گزارش خبرگزاری فارس، کنفدراسیون فوتبال آسیا (AFC) در نامه ای رسمی به فدراسیون فوتبال ایران و باشگاه گیتی پسند زمان  قرعه کشی جام باشگاه های فوتسال آسیا را رسماً اعلام کرد. بر این اساس 25 فروردین ماه 1401 مراسم قرعه کشی جام بااشگاه های فوتسال آسیا در مالزی برگزار می شود. باشگاه گیتی پسند بعنوان قهرمان فوتسال ایران در سال 1400 به این مسابقات راه پیدا کرده است. پیش از این گیتی پسند تجربه 3 دوره حضور در جام باشگاه های فوتسال آسیا را داشته که هر سه دوره به فینال مسابقات راه پیدا کرده و یک عنوان قهرمانی و دو مقام دومی بدست آورده است. انتهای پیام/   
    # '''
    text='\n\u0628\u0647 \u06af\u0632\u0627\u0631\u0634 \u062e\u0628\u0631\u06af\u0632\u0627\u0631\u06cc \u0641\u0627\u0631\u0633\u060c \u06a9\u0646\u0641\u062f\u0631\u0627\u0633\u06cc\u0648\u0646 \u0641\u0648\u062a\u0628\u0627\u0644 \u0622\u0633\u06cc\u0627 (AFC) \u062f\u0631 \u0646\u0627\u0645\u0647 \u0627\u06cc \u0631\u0633\u0645\u06cc \u0628\u0647 \u0641\u062f\u0631\u0627\u0633\u06cc\u0648\u0646 \u0641\u0648\u062a\u0628\u0627\u0644 \u0627\u06cc\u0631\u0627\u0646 \u0648 \u0628\u0627\u0634\u06af\u0627\u0647 \u06af\u06cc\u062a\u06cc \u067e\u0633\u0646\u062f \u0632\u0645\u0627\u0646\u00a0 \u0642\u0631\u0639\u0647 \u06a9\u0634\u06cc \u062c\u0627\u0645 \u0628\u0627\u0634\u06af\u0627\u0647 \u0647\u0627\u06cc \u0641\u0648\u062a\u0633\u0627\u0644 \u0622\u0633\u06cc\u0627 \u0631\u0627 \u0631\u0633\u0645\u0627\u064b \u0627\u0639\u0644\u0627\u0645 \u06a9\u0631\u062f. \u0628\u0631 \u0627\u06cc\u0646 \u0627\u0633\u0627\u0633 25 \u0641\u0631\u0648\u0631\u062f\u06cc\u0646 \u0645\u0627\u0647 1401 \u0645\u0631\u0627\u0633\u0645 \u0642\u0631\u0639\u0647 \u06a9\u0634\u06cc \u062c\u0627\u0645 \u0628\u0627\u0634\u06af\u0627\u0647 \u0647\u0627\u06cc \u0641\u0648\u062a\u0633\u0627\u0644 \u0622\u0633\u06cc\u0627 \u062f\u0631 \u0645\u0627\u0644\u0632\u06cc \u0628\u0631\u06af\u0632\u0627\u0631 \u0645\u06cc \u0634\u0648\u062f. \u0628\u0627\u0634\u06af\u0627\u0647 \u06af\u06cc\u062a\u06cc \u067e\u0633\u0646\u062f \u0628\u0639\u0646\u0648\u0627\u0646 \u0642\u0647\u0631\u0645\u0627\u0646 \u0641\u0648\u062a\u0633\u0627\u0644 \u0627\u06cc\u0631\u0627\u0646 \u062f\u0631 \u0633\u0627\u0644 1400 \u0628\u0647 \u0627\u06cc\u0646 \u0645\u0633\u0627\u0628\u0642\u0627\u062a \u0631\u0627\u0647 \u067e\u06cc\u062f\u0627 \u06a9\u0631\u062f\u0647 \u0627\u0633\u062a. \u067e\u06cc\u0634 \u0627\u0632 \u0627\u06cc\u0646 \u06af\u06cc\u062a\u06cc \u067e\u0633\u0646\u062f \u062a\u062c\u0631\u0628\u0647 3 \u062f\u0648\u0631\u0647 \u062d\u0636\u0648\u0631 \u062f\u0631 \u062c\u0627\u0645 \u0628\u0627\u0634\u06af\u0627\u0647 \u0647\u0627\u06cc \u0641\u0648\u062a\u0633\u0627\u0644 \u0622\u0633\u06cc\u0627 \u0631\u0627 \u062f\u0627\u0634\u062a\u0647 \u06a9\u0647 \u0647\u0631 \u0633\u0647 \u062f\u0648\u0631\u0647 \u0628\u0647 \u0641\u06cc\u0646\u0627\u0644 \u0645\u0633\u0627\u0628\u0642\u0627\u062a \u0631\u0627\u0647 \u067e\u06cc\u062f\u0627 \u06a9\u0631\u062f\u0647 \u0648 \u06cc\u06a9 \u0639\u0646\u0648\u0627\u0646 \u0642\u0647\u0631\u0645\u0627\u0646\u06cc \u0648 \u062f\u0648 \u0645\u0642\u0627\u0645 \u062f\u0648\u0645\u06cc \u0628\u062f\u0633\u062a \u0622\u0648\u0631\u062f\u0647 \u0627\u0633\u062a. \u0627\u0646\u062a\u0647\u0627\u06cc \u067e\u06cc\u0627\u0645\/\n\n\n'
    print(normalize_content(text))
