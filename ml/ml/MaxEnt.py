from nltk.classify import maxent
import MySQLdb
import pickle
import nltk
import logging

class MaxEnt:
    def import_data_from_sql(self):
        cur = self.mysql.cursor()
        cur.execute('''SELECT * FROM document_feature where document_feature.iflag is NULL''')
        # let F equals all features pairs
        F = cur.fetchall()
        # construct vector for training
        T = []

        # TODO: solve the keyword indexing return type issue
        # if use dict(a=feature['keyword'], the return type would be str
        # if use a=feature[index], the return type would be int
        for feature in F:
            t = [dict(a=feature[2],
                      b=feature[3],
                      c=feature[4],
                      d=feature[5],
                      e=feature[6],
                      f=feature[7],
                      g=feature[8],
                      h=feature[9],
                      i=feature[10],
                      j=feature[11]), feature[12]]
            T.append(t)
        return T

    def __init__(self, logger=None):
        print("Connecting to MySQL...")
        self.mysql = MySQLdb.connect(user="admin", passwd="fred1",
                                         charset='utf8', db="scraped")
        print("MySQL connected.")
        self.logger = logger if logger else logging.getLogger('training')
        self.T = self.import_data_from_sql()
        self.logger.info("%d features loaded", len(self.T))

    # save training_set
    def save_training_sets(self,training_sets):
        training_data = open('training_sets.pickle', 'wb')
        pickle.dump(training_sets, training_data)
        training_data.close()
        print("training sets successfully saved.")


    def save_testing_sets(self, testing_sets):
        training_data = open('testing_sets.pickle', 'wb')
        pickle.dump(testing_sets, training_data)
        training_data.close()
        print("testing sets successfully saved.")


    # try to open classifier
    def open_classifier(self):
        try:
            trained_classifier = open("classifier.pickle", "rb")
            # classifier = pickle.load(bayes_classifier)
            # bayes_classifier.close()
        except Exception as e:
            print "cannot load classifier, reason: %s" % e
            return None
        print("classifier successfully loaded.")
        return pickle.load(trained_classifier)


    # save classifier
    def save_classifier(self, trained_classifier):
        classifier = open("classifier.pickle", "wb")
        pickle.dump(trained_classifier, classifier)
        classifier.close()
        print("classifier successfully saved.")

    def test_classifier(self, classifier, testing_sets):
        pdist = classifier.prob_classify(testing_sets)
        print('%8.2f%6.2f' % (pdist.prob('n'), pdist.prob('y')))

    def label(self, classifier):
        cur = self.mysql.cursor()
        cur.execute('''SELECT * FROM document_feature where document_feature.iflag!=0 or document_feature.iflag is NULL''')
        F = cur.fetchall()
        Testing_set = []
        print("starting classifying..")
        for feature in F:
            t = dict(a=feature[2],
                      b=feature[3],
                      c=feature[4],
                      d=feature[5],
                      e=feature[6],
                      f=feature[7],
                      g=feature[8],
                      h=feature[9],
                      i=feature[10],
                      j=feature[11])
            cur.execute('''UPDATE document_feature SET document_feature.iflag=%d
                    WHERE document_feature.d1=%s AND document_feature.d2=%s'''
                        % (classifier.classify(t), feature[0], feature[1]))
            self.mysql.commit()
        self.logger.info("Classifying finished.")


        # search product details by id
    def get_product_info(self, id):
        cur = self.mysql.cursor()
        sqlstr = '''SELECT * FROM product where id=%d''' % id
        cur.execute(sqlstr)
        return cur.fetchone()

if __name__ == '__main__':
    me = MaxEnt()
    # algorithm could be one of ['IIS','GIS','MEGAM','TADM']
    #i = input("Select the function: 1. Training 2. Classifying 3. Display Results\n")
    i=4
    if i==1:
        algorithm = 'GIS'
        training_set = me.T
        print("start training classifier...")
        try:
            classifier = nltk.classify.MaxentClassifier.train(me.T, algorithm, trace=0, max_iter=1000)
        except Exception as e:
            me.logger.info(me, "Exception: %r" % e.message)
        me.save_classifier(classifier)
        me.logger.info(me, 'Training finished.')
        print("finished training.")
    elif i==2:
        classifier = me.open_classifier()
        if classifier!=None:
            me.label(classifier)
        else:
            print("Classifier not exist.")
    elif i==3:
            print("1 means identical, 0 means different")
            n = 0
            cur = me.mysql.cursor()
            cur.execute('''SELECT * FROM document_feature limit 5000''')
            F = cur.fetchall()
            for f in F:
                cur.execute('''SELECT title, supplier FROM product WHERE id=%s''' % f[0])
                print(cur.fetchone())
                cur.execute('''SELECT title, supplier FROM product WHERE id=%s''' % f[1])
                print(cur.fetchone())
                print(f[12])
                n+=1
                if(n%5==0):
                    k = raw_input("would you like to continue display? y/n \n")
                    if k == 'n':
                        break
    else:
        cur = me.mysql.cursor()
        cur.execute('''SELECT pid FROM product_group WHERE gid=1 or gid=1243''')
        P = cur.fetchall()
        for p in P:
            cur.execute('''SELECT title, supplier FROM product WHERE id=%s''' % p[0])
            print(cur.fetchone())
    # print("classifier accuracy: ", (nltk.classify.accuracy(classifier, testing_set))*100)
    # classifier.show_most_informative_features(5)
