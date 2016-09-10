import csv
import numpy as np
import sys


def count_sample(csv_name):
    f = open(csv_name,'r')
    ff = csv.reader(f)
    c=0
    for row in ff:
        c+=1
        #print c
    f.close()
    return c-1


def cat_numeric_feature(csv1,csv2):
    s1 = set()
    f = open(csv1,'r')
    ff = csv.reader(f)
    count = 0 
    for row in ff:
        if count == 0:
            feature = row[1:]
            for item in feature:
                s1.add(item)
        else:
            break
        count+=1
    f.close()
    s2 = set()
    f = open(csv2,'r')
    ff = csv.reader(f)
    count = 0 
    for row in ff:
        if count == 0:
            feature = row[1:]
            for item in feature:
                s2.add(item)
        else:
            break
        count+=1
    f.close()
    print "common"
    print s1.intersection(s2)
    print "in numeric not in cate"
    print s1.difference(s2)
    print "in cate not in numeric"
    print s2.difference(s1)

def sample_head(csv_name,size):
    f = open(csv_name,'r')
    ff = csv.reader(f)
    count = 0
    for row in ff:
        if count==size:
            break
        if count == 0:
            feature = row
            print "number of feature",len(row)
        else:
            fe = []
            for i in range(len(row)):
                if row[i]!='':
                    fe.append(feature[i]+": "+row[i])
            print fe
        count+=1
    f.close()


def category(csv_name):
    val=set()
    f = open(csv_name,'r')
    ff = csv.reader(f)
    count = 0
    for row in ff:
        if count:
            for i in range(len(row)):
                if i!=0 and row[i]!='':
                   val.add(row[i])
        count+=1
    return val

def multicat(csv_name):
    dic={}
    f = open(csv_name,'r')
    ff = csv.reader(f)
    count = 0
    for row in ff:
        if count ==0:
           feature = row
           for i in range(len(row)):
               if i!=0:
                   dic[row[i]]=set()
        else:
           for i in range(len(row)):
               if i!=0 and row[i]!='':
                   dic[feature[i]].add(row[i])
        count+=1
    print dic

def lexical(a,b):
    'return 1 if a<b in lexical order'
    'return 0 if a>b in lexical order'
    'we assume that a,b are stored in list'
    flag = 1
    n = len(a)
    if n==1:
        return a[0]<=b[0]
    else:
        if a[0]<b[0]:
            return True
        if a[0]==b[0]:
            return lexical(a[1:],b[1:])
        if a[0]>b[0]:
            return False

def extract(F):
    'F is in the form of L_S_F'
    import re
    pattern=re.compile('[0-9]+')
    L = re.findall(pattern,F)
    L=[int(i) for i in L]
    return L[:-1]
    

def time_relation(csv_name):
    f = open(csv_name,'r')
    ff = csv.reader(f)
    count = 0
    for row in ff:
        if count==0:
            feature = row
        else:
            fe = []
            for i in range(len(row)):
                if i!=0 and float(row[i])!=0:
                    fe.append((i,float(row[i])))
            "checking"
            for j in range(len(fe))-1:
                a = lexical(extract(feature[fe[j][0]]),extract(feature[fe[j+1][0]]))
                b = fe[j][1]<=fe[j+1][1]
                if a*b == False:
                    print fe[j],fe[j+1]
    return 0

def cor(x,y):
    "x, y are two columns and we want to calculate the correlation between them"
    import numpy as np
    x = np.array(x)
    y = np.array(y)
    if np.std(x)==0 or np.std(y)==0:
        return None
    else: 
        return np.corrcoef(x,y)[0,1]

def response(csv_name):
    f = open(csv_name,'r')
    ff = csv.reader(f)
    count = 0
    total = 0
    for row in ff:
        if count !=0 and float(row[-1])==1:
            total+=1
        count+=1
    print float(total)/count


def feature_response_cor(csv_name):
    """ this will be a roughly 3000*3000 matrix that we could handle and get some insights """
    f = open(csv_name,'r')
    ff = csv.reader(f)
    count = 0
    for row in ff:
        if count == 0:
            n = len(row)-1
            C = np.zeros((n,n))
            ind=[set() for i in range(n)]
            val=[{} for i in range(n)]
        else:
            for i in range(len(row)):
                if i!=0 and row[i] and float(row[i])!=0:
                    ind[i-1].add(count)
                    val[i-1][count]=float(row[i])
        count+=1

    for i in range(n):
        for j in range(n-i):
            """ compute the corrcoef in C[i,j] and C[j,i] """
            indices = ind[i]&ind[i+j]
            x = [val[i][k] for k in indices]
            y = [val[i+j][k] for k in indices]
            if len(indices)>=2:
              print len(indices)
              C[i,i+j]=cor(x,y)
              C[i+j,i]=C[i,i+j]
            else:
              C[i,i+j]=None
              C[i+j,i]=None
    np.save('Correlation',C)
    return 0


def feature_cate(csv_name):
    "it prints out the percentage of categories appearing in each feature"
    import re
    #f = open('category_value','r')
    #pattern = re.compile(r'\'(\S+)\'')
    #category = re.findall(f)
    #f.close()
    f = open(csv_name,'r')
    ff = csv.reader(f)
    count = 0
    for row in ff:
        if count==0:
            feature=row[1:]
            fe = [{} for i in range(len(row)-1)]
        else:
            for i in range(len(row)):
                if i!=0 and row[i]!='':
                    if not row[i] in fe[i-1]:
                        fe[i-1][row[i]]=1
                    else:
                        fe[i-1][row[i]]+=1
        count+=1
    for i in range(len(fe)):
        if fe[i]=={}:
            fe[i]=None
        else:
            s = sum([fe[i][key] for key in fe[i]])
            for key in fe[i]:
                fe[i][key]=fe[i][key]/float(s)
    for i in range(len(fe)):
        print feature[i]+": "+str(fe[i])

def support(csv1,out):
    S = set()
    g = open(out,'w')
    f = open(csv1,'r')
    ff = csv.reader(f)
    count = 0
    for row in ff:
        if count == 0:
           feature = row
        else:
           for i in range(len(row)-1):
                 if row[i+1]!='':
                    S.add(feature[i+1]) 
        count+=1
    f.close()
    print "support number of features", len(S)
    print "total feature", len(feature)-1
    return 0

def transform(l):
    import re
    pat = re.compile('(\w+)_F')
    for i in range(len(l)-1):
        g = re.findall(pat,l[i+1])
        l[i+1]=g[0]
    return l

def prod_station(csv1,out):
    g = open(out,'w')
    f = open(csv1,'r')
    ff = csv.reader(f)
    gg = csv.writer(g)
    gg.writerow(['id','Station'])
    count = 0
    for row in ff:
        if count == 0:
            feature = transform(row[:-1])
        else:
            s=set()
            for i in range(len(row)-2):
                if row[i+1]!='':
                    s.add(feature[i+1])
            prod_station=[row[0]]+[item for item in s]
            gg.writerow(prod_station)
        count+=1
    g.close()
    f.close()
    return 0

def station_feature(csv1,out):
    """ calculate the line station statistics for all the products """
    f = open(csv1,'r')
    ff = csv.reader(f)
    s = {}
    count = 0
    for row in ff:
        pattern = set(row[1:])
        p = tuple(pattern)
        if p in s:
           s[p]+=1
        else:
           s[p]=1
        count+=1
    g = open(out,'w')
    gg = csv.writer(g)
    gg.writerow(['LS Pattern','Frequencey','Percentage'])
    m = 0
    w = 0
    for key in s:
        fre = float(s[key])/count
        if fre>0.0001:
           gg.writerow([set(key),s[key],fre])
           w+=fre
           m+=1
    print w
    print "model",m
    f.close()
    g.close()

station_feature("prod_linestation_numeric.csv","linestation_statistics_numeric.csv")
