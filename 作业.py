from argparse import _MutuallyExclusiveGroup
import csv
import math
import os
from re import T
import jieba
from wsgiref import headers
jieba.setLogLevel(jieba.logging.INFO)

finallist=[]
cutscreen=[]#���Դ洢�ִʺ��ÿһ����Ļ����˫���б���ʽ�洢
stopwords=[]
datacsv = []
wordcount = {}
allvector = []
alldistance = []#nά˫���б�n����Ļ��������alldistance[i][j]��Ϊ��i����Ļ����j����Ļ��ŷ����þ��룬�Դ��ж��������ƶ�

###10-19Ϊ�����Ԥ����׶�(a = 'danmuku.csv',b = "D:\work\stopwords_list.txt")
def openfile(a,b):
    with open(a,encoding='UTF-8') as data:
        data_csv = csv.reader(data)
        headers = next(data_csv)  
        i = 0
        for row in data_csv:
            datacsv.append(row[0])
            i += 1
    for word in open(b,encoding='UTF-8'):
        stopwords.append(word.strip())

###19-28Ϊ����ͣ�ôʣ��ִʽ׶�
def screen_words():
    for i in range(0,10000):
    #for i in range(0,len(datacsv) - 1):
        #print(datacsv[i])
        seg_list = jieba.cut(datacsv[i], cut_all=False)
        #print("/ ".join(seg_list))
        #stayed_line=""
        tempscreen = []#cutscreen�����б�
        for word in seg_list:

            if word not in stopwords:
                tempscreen.append(word)
                #stayed_line=stayed_line+word+" "
                finallist.append(word)
        cutscreen.append(tempscreen)
        #print(stayed_line)
    #for i in range(0,len(finallist)):
    #    print(finallist[i])

def word_count():
    for word in finallist:
        wordcount[word] = wordcount.get(word,0)+1
    sortedhigh = sorted(wordcount.items(),key = lambda x :x[1],reverse= True)[:10]
    sortedlow = sorted(wordcount.items(),key = lambda x :x[1],reverse= False)[:10]
    return sortedhigh,sortedlow

    #�������м�����������Ľ��
    #for item in sortedhigh:
    #    print(item[0],item[1],sep = ":")
    #print('/////////') 
    #for item in sortedlow:
    #    print(item[0],item[1],sep = ":") 

def vector_get():
    for i in cutscreen:#�����iʵ���Ͼ��Ǳ��ִʵ�ĳһ����Ļ�����б����ʽ��ֵ��i
        #print('ha')
        vector = [0]*10
        countnum =  0
        #print('ha')
        for item in sortedhigh:
            countnum =countnum + 1
            #print('ha')
            if item[0] in i:
                #print('ha')
                vector[countnum - 1] = 1
        allvector.append(vector)

def distance_get():
    for i in allvector:
        templist = []#���Դ洢��i����Ļ�����൯Ļ��ŷ�Ͼ��룬��ʱ����
        for j in allvector:
            n = 0#ŷ�Ͼ����еı�������
            for k in range(0,9):
                n += pow((i[k]-j[k]),2)
            templist.append(math.sqrt(n))
        alldistance.append(templist)

#openfile�������ԣ�
openfile('danmuku.csv',"D:\work\stopwords_list.txt")
#print(len(datacsv))
#print(stopwords)

#screen_words�������ԣ�
screen_words()

length = len(cutscreen)
#word_count�������ԣ�
sortedhigh,sortedlow = word_count()

#vector_get�������ԣ�
vector_get()

#distance_get��������,
distance_get()
max = 0
for i in range(0,length - 1):
    for j in range(0,length - 1):
        tempnum = alldistance[i][j]
        #print(tempnum)
        if tempnum >= max:
            max = tempnum
            sentence1 = cutscreen[i]
            sentence2 = cutscreen[j]
#print(len(cutscreen[0]))
#����������������alldistance
#for m in range(0,length - 1):
#    for p in range (0,len(alldistance[m]) - 1):
#        print(alldistance[m][p])
for word1 in sentence1:
    print(word1,end = " ")
print("/")
for word2 in sentence2:
    print(word2,end = " ")        