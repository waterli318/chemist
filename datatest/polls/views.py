from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from paypal.standard.forms import PayPalPaymentsForm
from django.utils.decorators import available_attrs
from django.contrib.auth.decorators import login_required
import MySQLdb
import logging



def compare(request):
    com = compareP()
    ndf = 0
    #del request.session['wodetaiyang']
    #return HttpResponse('ok')

    if request.method == "GET":
        ndf = request.GET.get('index', 0)
        if 'wodetaiyang' not in request.session:
            F = com.random_row(2000)
            request.session['wodetaiyang'] = F
            request.session['index'] = 0
    else:
        p1_id = request.POST.get('p1_id')
        p2_id = request.POST.get('p2_id')
        iflag = request.POST.get('iflag', None)
        request.session['index'] = request.session['index'] + 1
        com.insert_feature_valuse(p1_id, p2_id, iflag)
            
    INDEX = request.session['index']
    iflag = request.session['wodetaiyang'][INDEX][12]
    while iflag != None:
        request.session['index'] = INDEX + 1
        INDEX = request.session['index']
        iflag = request.session['wodetaiyang'][INDEX][12]
    
    p1 = com.get_product_info(request.session['wodetaiyang'][INDEX][0])
    p1 = list(p1)
    p2 = com.get_product_info(request.session['wodetaiyang'][INDEX][1])
    p2 = list(p2)
    
    return render(request, 'compare.html', {'p1': p1, 'p2': p2})
    

class compareP:

    # get 1.id1 2.id2 from document_feature
    def get_id(self, idno, feature):
        if(1==idno):
            return feature[0]
        if(2==idno):
            return feature[1]

    def get_product_info(self, id):
        cur = self.mysql.cursor()
        sqlstr = '''SELECT id, name, brand, supplier, breadcrumbs, src_url, short_description, option_text FROM product where id=%d''' % id
        cur.execute(sqlstr)
        print(sqlstr)
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

    def import_data_from_sql(self, n):
        cur = self.mysql.cursor()
        if n == 0:
            cur.execute('''SELECT * FROM document_feature''')
        else:
            cur.execute('''SELECT * FROM document_feature limit %d''' % n)
        # let F equals all features pairs
        F = cur.fetchall()
        # construct vector for training
        return F

    def insert_feature_valuse(self, pid1, pid2, value):
        cur = self.mysql.cursor()
        sqlstr = '''UPDATE document_feature SET iflag=%s WHERE d1=%s AND d2=%s''' % (value, pid1, pid2)
        cur.execute(sqlstr)
        self.mysql.commit()
        
    def random_row(self, n):
        sqlstr = """SELECT * FROM document_feature ORDER BY RAND() LIMIT %d""" % n;
        cur = self.mysql.cursor()
        cur.execute(sqlstr)
        return cur.fetchall()
# Create your views here.
