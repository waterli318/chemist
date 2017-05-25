from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import MySQLdb
import codecs
#
title = u'''blackmores celery 3000 50 tablets '''
title2 = u'''blackmores celery 3000 10 tablets '''
stop_words = set(stopwords.words('english'))
word_tokens = word_tokenize(title)
word_tokens2 = word_tokenize(title2)
# filtered_sentence1 = [w for w in word_tokens if not w in stop_words]

# filtered_sentence2 = [w for w in word_tokens2 if not w in stop_words]
# mysql = MySQLdb.connect(user="admin", passwd="fred1",
#                              charset='utf8', db="ml")
# cur = mysql.cursor(cursorclass=MySQLdb.cursors.DictCursor)
# cur.execute("""select brand from product group by brand
#  """)
# print stop_words
# B = cur.fetchall()
# brands = []
# for b in B:
#     brands.append(b['brand'])
# print brands

# f = codecs.open('brands', 'w', 'utf-8')
# for b in brands:
#   print>>f, b
#
# f.close()



# number1 = [w for w in word_tokens if w.isnumeric()]
# number2 = [w for w in word_tokens2 if w.isnumeric()]
newn = set(word_tokens) ^ set(word_tokens2)
print newn
# print len(newn)
# print(number)


# training_sets = self.open_training_sets()

        # start to train the model
        # i = input("type in starting index. (max index %s)" % len(P))

        # for p in P[i:]:
        #     # start processing p'th documents
        #     # do sphinx search
        #     title = re.sub('[\'"]', ' ', p['title'].encode('utf8'))
        #     q = "SELECT *, WEIGHT() AS w FROM scraped WHERE MATCH('@title \"" + \
        #         self.mysql.escape_string(title) + "\"/1') LIMIT 16 " + \
        #         "OPTION ranker=" + self.ranker_name + "('')"
        #     sph.execute(q)
        #     d = Document(p)
        #     d_title = d.title.raw_text
        #     d_desc = d.descriptions.raw_text
        #     d.preprocess()
        #
        #     compare results from sphinx
        #     for r in sph.fetchall():
        #         if r['id'] not in M:
        #             self.logger.error("Error: product %s not found", r['id'])
        #             continue
        #         d1 = Document(M[r['id']])
        #
        #         print('product 1: title: %s' % d_title)
        #         print('brand: %s' % d.brand)
        #         print('supplier: %s' % d.supplier)
        #         print('product 2: title: %s' % d1.title.raw_text)
        #         print('brand: %s' % d1.brand)
        #         print('supplier: %s' % d1.supplier)
        #
        #         # take input as y_data
        #         y_data = raw_input("Are they the same product? y/n :")
        #         if y_data != 'y' and y_data != 'n':
        #             print('product 1: desc: %s' % d_desc)
        #             print('product 2: desc: %s' % d1.descriptions.raw_text)
        #             y_data = raw_input("Are they the same product? y/n :")
        #         if y_data != 'y' and y_data != 'n':
        #             y_data = 'n'
        #
        #         d1.preprocess()
        #         training_sets.append((dict(a=d.title.raw_text, b=d1.title.raw_text), y_data))
        #     if 'a' == funcI:
        #         self.save_training_sets(training_sets)
        #     else:
        #         self.save_testing_sets(training_sets)
        #     y_n = raw_input('Would you like to continue? y/n :')
        #     if y_n == 'y':
        #         continue
        #     else:
        #         break