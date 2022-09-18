from argparse import _MutuallyExclusiveGroup
import csv
import math
import os
from re import T
import jieba
from wsgiref import headers
jieba.setLogLevel(jieba.logging.INFO)

finallist=[]
cutscreen=[]#用以存储分词后的每一条弹幕，以双重列表形式存储
stopwords=[]
datacsv = []
wordcount = {}
allvector = []
alldistance = []#n维双重列表，n即弹幕总数量，alldistance[i][j]意为第i条弹幕到第j条弹幕的欧几里得距离，以此判断语义相似度

###10-19为读入和预处理阶段(a = 'danmuku.csv',b = "D:\work\stopwords_list.txt")
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

###19-28为过滤停用词，分词阶段
def screen_words():
    for i in range(0,10000):
    #for i in range(0,len(datacsv) - 1):
        #print(datacsv[i])
        seg_list = jieba.cut(datacsv[i], cut_all=False)
        #print("/ ".join(seg_list))
        #stayed_line=""
        tempscreen = []#cutscreen的子列表
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

    #下面四行检验两种排序的结果
    #for item in sortedhigh:
    #    print(item[0],item[1],sep = ":")
    #print('/////////') 
    #for item in sortedlow:
    #    print(item[0],item[1],sep = ":") 

def vector_get():
    for i in cutscreen:#这里的i实际上就是被分词的某一条弹幕，以列表的形式赋值给i
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
        templist = []#用以存储第i条弹幕到其余弹幕的欧氏距离，随时更新
        for j in allvector:
            n = 0#欧氏距离中的被开方项
            for k in range(0,9):
                n += pow((i[k]-j[k]),2)
            templist.append(math.sqrt(n))
        alldistance.append(templist)

#openfile函数测试，
openfile('danmuku.csv',"D:\work\stopwords_list.txt")
#print(len(datacsv))
#print(stopwords)

#screen_words函数测试，
screen_words()

length = len(cutscreen)
#word_count函数测试，
sortedhigh,sortedlow = word_count()

#vector_get函数测试，
vector_get()

#distance_get函数测试,
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
#下面三行用来检验alldistance
#for m in range(0,length - 1):
#    for p in range (0,len(alldistance[m]) - 1):
#        print(alldistance[m][p])
for word1 in sentence1:
    print(word1,end = " ")
print("/")
for word2 in sentence2:
    print(word2,end = " ")        