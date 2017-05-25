import os
import re
import sys
import json
import MySQLdb
import logging

from collections import Counter

# import for product classification
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
import nltk
import pickle

from ml.document import TextField, Document, Feature, FeatureGenerator
from ml.util import is_number, tokenise

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

MIN_FREQ = 80


class Featuriser:
    
    # check if ranker plugin for sphinx loaded, if not, load ranker plugin.
    def create_plugins(self):
        cur = self.sphinx.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute("show plugins")
        for r in cur.fetchall():
            if r['Name'] == self.ranker_name: return
        cur.execute("create plugin %s type 'ranker' soname '%s.so'" %
                    (self.ranker_name, self.ranker_name))
        print("Ranker plugin loaded.")
    
    # load data from mysql and sphinx.
    def __init__(self, reset_unit_words=True, ranker_name='hit_count',
                 logger=None):
        print("Connecting to MySQL...")
        self.mysql = MySQLdb.connect(user="admin", passwd="fred1",
                                     charset='utf8', db="scraped")
                                     print("MySQL connected. \n Connecting MySQL to sphinx...")
                                     self.sphinx = MySQLdb.connect(host="0", port=9307)
                                     print("Sphinx connected.")
                                     self.ranker_name = ranker_name
                                     self.logger = logger if logger else logging.getLogger('scraped')
                                     self.load_brand_names()
                                     if reset_unit_words:
                                         self.reset_unit_words()
                                     self.load_unit_words()
    self.classifier = self.open_classifier()
        self.fg = FeatureGenerator(self.brand_names, self.unit_words)
        print("Information loaded.")

    def load_brand_names(self):
        cur = self.mysql.cursor()
        cur.execute("SELECT name FROM brand")
        brand_names = [r[0].lower() for r in cur.fetchall() if r[0]]
        self.brand_names = frozenset(brand_names)
        self.logger.info("%d brand name(s) loaded", len(self.brand_names))

def load_unit_words(self):
    cur = self.mysql.cursor()
        self.unit_words = {}
        cur.execute("select name, freq from unit_word where freq>=%s", (MIN_FREQ,))
        for r in cur.fetchall():
            self.unit_words[r[0]] = r[1]
    self.logger.info("%d unit words loaded", len(self.unit_words))

def reset_unit_words(self):
    cur = self.mysql.cursor()
        cur.execute("select name from product")
        cnt = Counter()
        for r in cur.fetchall():
            ws = tokenise(r[0], self.brand_names)
            for i in xrange(len(ws) - 1):
                if is_number(ws[i]) and ws[i + 1].isalpha():
                    cnt[ws[i + 1]] += 1

    cur.execute("TRUNCATE TABLE unit_word")
        for w in cnt:
            cur.execute("INSERT INTO unit_word (name, freq) VALUES (%s, %s)",
                        (w, cnt[w]))
        self.mysql.commit()
        self.logger.info("%d unit words found", len(cnt))

# try to open training_sets
def open_training_sets(self):
    try:
        training_data = open("training_sets.pickle", "rb")
            training_sets = pickle.load(training_data)
            training_data.close()
        except Exception as e:
            print "cannot load classifier, reason: %s" % e
            training_sets = []
            return training_sets
    print("training sets successfully loaded.")
        return training_sets

# try to open testing_sets
def open_testing_sets(self):
    try:
        testing_data = open("training_sets.pickle", "rb")
            testing_sets = pickle.load(testing_data)
            testing_data.close()
        except Exception as e:
            print "cannot load classifier, reason: %s" % e
    print("testing sets successfully loaded.")
        return testing_sets

# save training_set
@staticmethod
    def save_training_sets( training_sets):
        training_data = open('training_sets.pickle', 'wb')
        pickle.dump(training_sets, training_data)
        training_data.close()
        print("training sets successfully saved.")
    
    def save_testing_sets(self, testing_sets):
        training_data = open('testing_sets.pickle', 'wb')
        pickle.dump(testing_sets, training_data)
        training_data.close()
        print("testing sets successfully saved.")
    
    # try to pen classifier
    @staticmethod
    def open_classifier():
        try:
            bayes_classifier = open("naviebayes.pickle", "rb")
        # classifier = pickle.load(bayes_classifier)
        # bayes_classifier.close()
        except Exception as e:
            print "cannot load classifier, reason: %s" % e
        print("classifier successfully loaded.")
        return pickle.load(bayes_classifier)
    
    # save classifier
    def save_classifier(self, bayes_classifier):
        classifier = open("naviebayes.pickle", "wb")
        pickle.dump(bayes_classifier, classifier)
        classifier.close()
        print("classifier successfully saved.")
    
    # feature selection.
    def execute(self):
        # funcI = raw_input("a.Training sets \nb.Testing sets")
        
        # connect to mysql and sphinx
        print("Getting cursor from MySQL and sphinx...")
        cur = self.mysql.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sph = self.sphinx.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        
        self.create_plugins()
        self.logger.info("Loading products ...")
        cur.execute("""select id, brand, supplier, title, breadcrumbs,
            option_text, short_description, description from product
            """)
        P = cur.fetchall()
        self.logger.info("%d products loaded", len(P))
        M = { p['id']: p for p in P }
        
        n = 1
        for p in P:
            d = Document(p)
            title = re.sub('[\'"]', ' ', p['title'].encode('utf8'))
            q = "SELECT *, WEIGHT() AS w FROM scraped WHERE MATCH('@title \"" +\
                self.mysql.escape_string(title) + "\"/1') LIMIT 64 "+\
                "OPTION ranker=" + self.ranker_name + "('')"
            sph.execute(q)
            
            if n % 500 == 0: self.logger.info('Processed %d documents', n)
            n += 1
            
            for r in sph.fetchall():
                if r['id'] not in M:
                    self.logger.error("Error: product %s not found", r['id'])
                    continue
                d1 = Document(M[r['id']])
                si = [str(i) for i in sorted([d.id, d1.id])]
                
                cur.execute("SELECT * from document_feature WHERE d1=%s AND d2=%s" %
                            (si[0], si[1]))
                            if cur.fetchone():
                                self.logger.info('Skip %s %s', si[0], si[1])
                                    continue
                                        
                                        f = self.fg.generate(d, d1).__dict__
                                            pc = ', '.join(['%s'] * (2 + len(f)))
                                                cols = ', '.join(['d1', 'd2'] + f.keys())
                                                    
                                                    sql = "INSERT INTO document_feature(%s) VALUES (%s)" % (cols, pc)
                                                        cur.execute(sql, si + f.values())
                                                            self.logger.info('Done %s %s', si[0], si[1])
                                                        self.mysql.commit()
    
    self.logger.info("Finished")

# add cid to products
def executeClassifing(self):
    # funcI = raw_input("a.Training sets \nb.Testing sets")
    
    # connect to mysql and sphinx
    print("Getting cursor from MySQL for classifing...")
        cur = self.mysql.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute('''SELECT d1 FROM document_feature WHERE iflag=1 GROUP BY d1''')
        G = cur.fetchall()
        Group=0
        for g in G:
            # if d1 not in id-group
            cur.execute('''SELECT gid FROM product_group WHERE pid=%s''' % g['d1'])
            res = cur.fetchone()
            if(res):
                group=res['gid']
            else:
                Group+=1
                group=Group
                cur.execute("INSERT INTO product_group(gid,pid) VALUES (%d,%d)" % (group,g['d1']))
            # put all d2 not in id to id-group
            cur.execute('''SELECT d2 FROM document_feature WHERE d1=%s AND iflag=1''' % g['d1'])
            # put d1-group = d2-group to database
            P = cur.fetchall()
            for p in P:
                # insert id to group
                sql = "INSERT INTO product_group(gid,pid) VALUES (%d,%d)" % (group,p['d2'])
                cur.execute(sql)
            self.mysql.commit()
    #print("Finished processing d1=%s" % g['d1'])
    
    self.logger.info("Adding product_group Finished")
# try to open classifier
def open_classifier(self):
    try:
        trained_classifier = open("ml/classifier.pickle", "rb")
        # classifier = pickle.load(bayes_classifier)
        # bayes_classifier.close()
        except Exception as e:
            print "cannot load classifier, reason: %s" % e
            return None
    print("classifier successfully loaded.")
        return pickle.load(trained_classifier)

# compare id, brand, supplier, title, breadcrumbs,
# option_text, short_description, description of product
# using classifier TODO: fix bugs
def compare(self, d1, d2):
    feature = self.fg.generate(d1, d2).__dict__
        t = [dict(a=feature[0],
                  b=feature[1],
                  c=feature[2],
                  d=feature[3],
                  e=feature[4],
                  f=feature[5],
                  g=feature[6],
                  h=feature[7],
                  i=feature[8],
                  j=feature[9])]
        return self.classifier.classify(t)

# def desc_filter(self, d, stop_words):
# start processing documents
# d_word_tokens = word_tokenize(d['short_description'])
# d_filtered_sentence = [d_sw for d_sw in d_word_tokens.lower() if not d_sw in stop_words]
# d['short_description'] = d_filtered_sentence
# d_word_tokens = word_tokenize(d['description'])
# d_filtered_sentence = [d_sw for d_sw in d_word_tokens.lower() if not d_sw in stop_words]
# d['description'] = d_filtered_sentence
# return d
if __name__ == '__main__':
    logging.basicConfig(filename="scraped.log", level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S')
                        
                        pc = Featuriser(reset_unit_words=False,
                                        logger=logging.getLogger('scraped'))
                        
    pc.executeClassifing()

