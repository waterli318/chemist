import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from util import tokenise, is_number

class TextField:
    def __init__(self, value):
        self.raw_text = value
        self.word_vec = re.split(r'[^\w]+', value.lower())
        self.word_vec = [w for w in self.word_vec if len(w) > 0]
        self.word_set = frozenset(self.word_vec)

    def next_of(self, w):
        try:
            n = self.word_vec[self.word_vec.index(w) + 1]
        except:
            n = None
        return n
    
    def contains(self, w):
        return w in self.word_set


class Document:

    def __init__(self, r):
        self.id = r['id']
        self.brand = r['brand']
        self.supplier = r['supplier']
        self.title = TextField(r['title'])
        self.breadcrumbs = TextField(r['breadcrumbs'])
        self.option_text = TextField(r['option_text'])
        s1 = r['short_description'] if r['short_description'] else ''
        s2 = r['description'] if r['description'] else ''
        self.descriptions = TextField(s1 + ' ' + s2)
        self.stop_words = set(stopwords.words('english'))
        # numbers
        word_tokens = word_tokenize(self.title.raw_text)
        filtered_numbers = [w for w in word_tokens if w.isnumeric()]
        self.numbers = filtered_numbers
        # brand

    def has_brand(self):
        return self.brand and len(self.brand) > 0

    def preprocess(self):
        # abstract title
        word_tokens = word_tokenize(self.title.raw_text)
        filtered_numbers= [w for w in word_tokens if w.isnumeric()]
        self.numbers = filtered_numbers

        # abstract descriptions
        # reg_tokenizer = RegexpTokenizer(r'\w+')
        # word_tokens = reg_tokenizer.tokenize(self.descriptions.raw_text)
        # # word_tokens = word_tokenize(self.descriptions.__str__())
        # filtered_sentence = [w for w in word_tokens if not w in self.stop_words]
        # self.descriptions = filtered_sentence

class Feature:
    def __init__(self):
        self.wc_total_strong = 0
        self.wc_total_weak = 0
        self.wc_breadcrumbs = 0
        self.wc_option_text = 0
        self.wc_description = 0
        self.wc_brand_name = 0
        self.wc_number = 0
        self.wc_spec_number = 0
        self.brand_count = 0
        self.same_supplier = 0
        # self.wc_title = 0


class FeatureGenerator:
    def __init__(self, brand_names, unit_words):
        self.brand_names = brand_names
        self.unit_words = unit_words

    def update(self, result, w, d, d1):
        if w in self.brand_names:
            result.wc_brand_name += 1

        if is_number(w):
            result.wc_number += 1
            if d.title.next_of(w) in self.unit_words:
                result.wc_spec_number += 1

        hit_count = 0

        if d1.breadcrumbs.contains(w):
            result.wc_breadcrumbs += 1
            hit_count += 1

        if d1.option_text.contains(w):
            result.wc_option_text += 1
            hit_count += 1

        if d1.descriptions.contains(w):
            result.wc_description += 1
            hit_count += 1

        if hit_count == 0:
            result.wc_total_strong += 1

    def generate(self, d1, d2):
        result = Feature()

        s1_2 = d1.title.word_set - d2.title.word_set
        s2_1 = d2.title.word_set - d1.title.word_set

        result.wc_total_weak = len(s1_2) + len(s2_1)

        word_tokens1 = word_tokenize(d1.title.raw_text)
        word_tokens2 = word_tokenize(d2.title.raw_text)
        # result.wc_title = set(word_tokens1) ^ set(word_tokens2)

        for w in s1_2:
            self.update(result, w, d1, d2)

        for w in s2_1:
            self.update(result, w, d2, d1)

        if d1.has_brand():
            result.brand_count += 1

        if d2.has_brand():
            result.brand_count += 1

        if d1.supplier == d2.supplier:
            result.same_supplier = 1

        return result
