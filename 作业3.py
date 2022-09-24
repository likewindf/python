import re
import os
import jieba
import pylab as pl

data = []
anger = []
disgust = []
fear = []
joy = []
sadness =[]
cut_weibo = []
alldata = [data,anger,disgust,fear,joy,sadness]
stopwords = []
weibo_time = []#存储weibo发布时间
weibo_place = []#存储weibo发布地点
emotion_vector = []
time_dic = {}
for word in open('stopwords_list.txt',encoding='UTF-8'):
    stopwords.append(word.strip())

def readline_count(file_name):
    return len(open(file_name,'r',encoding = 'UTF-8').readlines())


def openfile(weibo,anger_,disgust_,fear_,joy_,sadness_):
    #print('1 is ok\n')
    address = [weibo,anger_,disgust_,fear_,joy_,sadness_]
    data0 = open(weibo,"r",encoding="UTF-8")
    anger0 = open(anger_,"r",encoding="UTF-8")
    disgust0 = open(disgust_,"r",encoding="UTF-8")
    fear0 = open(fear_,"r",encoding="UTF-8")
    joy0 = open(joy_,"r",encoding="UTF-8")
    sadness0 = open(sadness_,"r",encoding="UTF-8")
    alldata0 = [data0,anger0,disgust0,fear0,joy0,sadness0]
    #print('2 is ok\n')
    for i in range(0,6):
        length = readline_count(address[i])
        for j in range(0,length): 
            alldata[i].append((alldata0[i].readline()).strip())


    

def jieba_addword():
    address = ['weibo.txt','anger.txt','disgust.txt','fear.txt','joy.txt','sadness.txt']
    for i in range(1,6):
        for j in range(0,readline_count(address[i])):
            jieba.add_word(alldata[i][j]) 




def cut_wash():
    for r in range(0,len(data)):
        # 去除url
        s = re.sub(r'http[: ]+\S+', "", data[r])
        data[r] = s

    for i in range(0,len(data)):
    #for i in range(0,len(data) - 1):
        #print(data[i])
        seg_list = jieba.cut(data[i], cut_all=False)
        #print("/ ".join(seg_list))
        temp_cut_weibo = []#cut_weibo的子列表
        for word in seg_list:

            if word not in stopwords:
                temp_cut_weibo.append(word)
        cut_weibo.append(temp_cut_weibo)

#def emotion_count(sen,dicn):#接受两个变量，一个是被切分的句子来自cut_weibo,一个是情绪字典在alldata中的索引
#        count = 0
#        for k in range(0,len(sen)):
            #print(sen[k])
            #print(len(alldata[dicn]))
#            if sen[k] in alldata[dicn]:
#                #print("ok")
#                count += 1
#        return count

def emotion_vector_get():
    def emotion_count(sen,dicn):#接受两个变量，一个是被切分的句子来自cut_weibo,一个是情绪字典在alldata中的索引
        count = 0
        for k in range(0,len(sen)):
            #print(sen[k])
            #print(len(alldata[dicn]))
            if sen[k] in alldata[dicn]:
                #print("ok")
                count += 1
        return count

    for i in cut_weibo:
        temp_vector = [0]*5
        for j in range(1,6):
            temp_vector[j - 1] = emotion_count(i,j)
            #print(temp_vector)
        emotion_vector.append(temp_vector)



def re_find_time():#搜索data中的微博内容并找到时间的那部分/d：/d：/d存为列表
    for i in data:
        if re.findall(r'\d+:\d+:\d+',i) != []:
            weibo_time.append(re.findall(r'\d+:\d+:\d+',i)[0])
        else:
            weibo_time.append('notime')
            #这里尝试了很久很久，后来发现notime只有第一行location	text	user_id	weibo_created_at根本就不是一条微博
            #添加notime是为了weibo_time和data的索引能对上。后面遍历要range(1，len(data))
            #print(re.findall(r'\d+:\d+:\d+',i)[0])


def re_find_place():#搜索data中的微博内容并找到时间的那部分[(.*)]存为列表
    for i in data:
        if re.findall(r'[(.*)]',i) != []:
            weibo_place.append(re.findall(r'\d+.?\d+',i))#这里其实会把所有带小数点的数全部找出来，不过我后面只有用前两条数据
            #只用weibo_place[0][1]对应经纬度
        else:
            weibo_place.append('noplace')

def time_dic_get():
    #初始化
    for i in range(0,24):
        time_dic[i] = [0]*5
    #更新不同小时段情绪值
    for j in range(1,len(emotion_vector)):
        num = int(weibo_time[j].split(':')[0])
        for k in range(0,5):
            time_dic[num][k] += emotion_vector[j][k]

def place_visual():#北京位于东经115.7°—117.4°，北纬39.4°—41.6°，中心位于北纬39°54′20″，东经116°25′29″,weibo_place[n][0]是纬度，[n][1]是经度
    pl.xlim(39.5,40.25)
    pl.ylim(116,116.8)
    def color_get(list):
        index_ = list.index(max(list))
        dic = {0:"red",1:"blue",2:"black",3:"orange",4:"grey"}#anger,disgust,fear,joy,sadness
        return dic[index_]
    for i in range(1,len(weibo_place)):
        x = [float(weibo_place[i][0])]
        y = [float(weibo_place[i][1])]
        pl.scatter(x,y,s = 2,c = color_get(emotion_vector[i]))
    pl.title("emotional map") #设置标题
    pl.xlabel("latitude") #设置x轴标注
    pl.ylabel("longtitude") #设置y轴标注
    pl.text(39.51,116.77,s = 'anger(·)',fontsize = 10,c = 'red')
    pl.text(39.51,116.73,s = 'disgust(·)',fontsize = 10,c = 'blue')
    pl.text(39.51,116.69,s = 'fear(·)',fontsize = 10,c = 'black')
    pl.text(39.51,116.65,s = 'joy(·)',fontsize = 10,c = 'orange')
    pl.text(39.51,116.61,s = 'sadness(·)',fontsize = 10,c = 'grey')
    pl.show()



#下面几行测试readline_count()函数
#length = readline_count('weibo.txt')
#print(length)z

#下面测试openfile函数
openfile('weibo.txt','anger.txt','disgust.txt','fear.txt','joy.txt','sadness.txt')
#for i in alldata:
#        print("{}".format(len(i)))
#for i in alldata:
#    for j in i:
#        print(j)

#下面测试jieba_addword函数
jieba_addword()

#下面测试cut_wash函数
cut_wash()
#用于查看cut_weibo[]中的内容
#for i in cut_weibo:
#    print(i)
#    print(type(i))

#下面测试emotion_vector_get()
emotion_vector_get()
#for i in emotion_vector:
#    if i != [0]*5:
#        print(i,end = " ")
#下面检验五个情绪词典
#for i in range(1,6):
#    for j in alldata[i]:
#        print(j,end = " ")

re_find_time()
#下面检验weibo_time列表是否被正确添加
#for i in weibo_time:
    #print('{}:{}:{}'.format(i,type(i),len(i)),end = " ")
    #print(i,end = ' ')

re_find_place()
#下面检验weibo_place列表是否被正确添加
#for i in weibo_place:
#    print('{}:{}:{}'.format(i,type(i),len(i)),end = " ")
#    print(i,end = ' ')
    #print(i[0],end = ' ')
    #print(i[1],end = ' ')

time_dic_get()#得到不同小时段的情绪比例
#下面检验time_dic_get()是否被正确添加
#print(time_dic)

place_visual()
#下面检验place_visual()是否正确可视化



