import MySQLdb
import logging
import random

class compareP:

    # get 1.id1 2.id2 from document_feature
    def get_id(self, idno, feature):
        if(1==idno):
            return feature[0]
        if(2==idno):
            return feature[1]

    # search product details by id
    def get_product_info(self, id):
        cur = self.mysql.cursor()
        sqlstr = '''SELECT * FROM product where id=%d''' % id
        cur.execute(sqlstr)
        return cur.fetchone()

    def __init__(self, logger=None):
        # conduct first N data_set
        self.N = 5
        print("Connecting to MySQL...")
        self.mysql = MySQLdb.connect(user="admin", passwd="fred1",
                                     charset='utf8', db="scraped")
        print("MySQL connected.")
        self.logger = logger if logger else logging.getLogger('training')
        self.F = self.import_data_from_sql(self.N)
        self.logger.info("%d features loaded", len(self.F))

    # return first n document_features from database
    def import_data_from_sql(self, n=0):
        cur = self.mysql.cursor()
        if(n!=0):
            cur.execute('''SELECT * FROM document_feature limit %d''' % n)
        else:
            cur.execute('''SELECT * FROM document_feature''')
        # let F equals all features pairs
        F = cur.fetchall()
        # construct vector for training
        return F

    # update iflag according to product id1 and product id2
    def insert_feature_valuse(self, pid1, pid2, value):
        cur = self.mysql.cursor()
        sqlstr = '''UPDATE document_feature SET document_feature.iflag=%d
                    WHERE document_feature.d1=%s AND document_feature.d2=%s'''\
                 % (int(value), int(pid1), int(pid2))
        cur.execute(sqlstr)
        self.mysql.commit()

    # return random n rows from document_feature table
    def random_row(self, n=2000):
        cur = self.mysql.cursor()
        cur.execute('''SELECT * from document_feature ORDER BY RAND() LIMIT %d''' % n)
        return cur.fetchall()



if __name__ == '__main__':
    cp = compareP()
    #R = cp.random_row(2000)
    #for r in R:
     #   print(r)
    # for f in cp.F:
    # p1 = cp.get_product_info(cp.F[0][0])
    # p2 = cp.get_product_info(cp.F[0][1])
    #
    # cp.insert_feature_valuse(p1[0], p2[0], 0)

