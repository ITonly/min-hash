# encoding:utf-8
__author__ = "li shi di"
import os
import chardet
import jieba
import math
import random
import sys

"""
此函数用于获得fileName文件中的内容，文件内容存放在字符串中返回
"""
def getFileContent(fileName):
    file=open(fileName,"rb")
    fileContent=file.read()
    fileContent = jieba.cut(fileContent)

    fileContent = ''.join(fileContent)
    fileContent=fileContent.replace("\t"," ")
    fileContent=fileContent.replace("\n"," ")
    fileContent=fileContent.replace("\r"," ").replace('\u3000', '').replace('&nbsp', '')
    file.close()

    return fileContent


"""
此函数用于获得fileName文件中的内容，文件内容存放在字符串中返回
"""


# def get_file_content(file_name):
    # bytes = min(32, os.path.getsize(file_name))
    # raw = open(file_name, 'rb').read(bytes)
    # result = chardet.detect(raw)
    # encoding = result['encoding']
    # # u = raw.decode('gb2312', 'ignore')
    # infile = open(file_name, 'r', encoding='gb18030', errors='ignore')
    # #
    # file_content = infile.read()
    # # u = file_content.decode('gb2312')  # 以文件保存格式对内容进行解码，获得unicode字符串
    #
    # '''下面我们就可以对内容进行各种编码的转换了'''
    # str = u.encode('utf-8')  # 转换为utf-8编码的字符串str

    # print(file_content)

    # file = open(file_name, "r",encoding="'utf-8-sig")
    # file_content = file.read()
    # s
    # file_content = str.replace("\t", " ")
    # file_content = file_content.replace("\n", " ")
    # file_content = file_content.replace("\r", " ")
    # infile.close()
    # # raw.close()
    # return file_content


"""
此函数用于获取dir文件夹中的文件的内容
"""


def get_files_name(dir_name):
    file_list = []
    t = os.walk(dir_name)

    for item in t:
        file = ''
        for name in item[2]:
            file = item[0] + '\\'
            file_list.append(file+name)
    return file_list


"""
此函数用于对各个文件中的内容进行k-shingle，然后对词条进行哈希（此处就用字典存储了）
其中dir是文件夹的名称字符串类型，k是int型
"""


def getShingleList(dir, k):
    fileList = get_files_name(dir)

    shingleList = list()
    for fileName in fileList:
        fileContent = getFileContent(fileName)
        fileContent = seg_sentence(fileContent)
        shingle = set()
        for index in range(0, len(fileContent) - k + 1):
            shingle.add(fileContent[index:index + k])
        shingleList.append(shingle)
    return shingleList


"""
此函数用于获得所有文档的最小哈希签名，signatureNum表示签名行数
"""
def getMinHashSignature(shingleList,signatureNum):
    #tatalSet用于存放所有集合的并集
    totalSet=shingleList[0]
    for i in range(1,len(shingleList)):
        totalSet=totalSet|shingleList[i]
    #randomArray用于模拟随机哈希函数
    randomArray=[]

    temp=int(math.sqrt(signatureNum))
    #signatureList用于存放总的哈希签名
    signatureList=[]
    maxNum=sys.maxsize
    for i in range(signatureNum):
        randomArray.append(random.randint(1,temp*2))
        randomArray.append(random.randint(1,temp*2))
    #buketNum用于记录所有元素的个数，作为随机哈希函数的桶号
    buketNum=len(totalSet)
    for i in range(signatureNum):
        """
        A用于代表随机哈希函数的系数，B代表常数，signature用于存放哈希函数产生的签名
        """
        A=randomArray[i*2]
        B=randomArray[i*2+1]
        signature=[]
        for shingleSet in shingleList:
            minHash=maxNum
            index=-1
            for item in totalSet:
                index+=1
                if item in shingleSet:
                    num=(A*index+B)%buketNum
                    minHash=min(minHash,num)
            signature.append(minHash)
        signatureList.append(signature)
    return signatureList


# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return set(stopwords)


# 对句子进行分词
def seg_sentence(sentence):
    outstr = ''
    sentence_seged = jieba.cut(sentence)
    stopwords = stopwordslist('./data/stop_words.txt')  # 这里加载停用词的路径

    for word in sentence_seged:
        if word.strip() not in stopwords and check_contain_chinese(word):
                outstr += word
                outstr += " "
    return outstr


def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
        else:
            return False


"""
此函数通过比较两个文档的最小哈希签名进行计算相似度，传入的参入是两个文档的最小哈希签名的集合，
存放在list中，最后结果返回相似度
"""


def calSimilarity(signatureSet1, signatureSet2):
    count = 0
    for index in range(len(signatureSet1)):
        if (signatureSet1[index] == signatureSet2[index]):
            count += 1
    return count / (len(signatureSet1) * 1.0)


def list_change(f_list):
    res = [[0 for col in range(len(f_list))] for row in range(len(f_list[0]))]
    for i, v1 in enumerate(f_list):
        for j, v2 in enumerate(v1):
            res[j][i]= v2
    return res

"""
此函数用于计算所有文档的相似度，并将结果存放在一个list中，结果用元组存放
"""


def calAllSimilarity(signature_list, filesName):
    signatureNum = len(signature_list)
    signature_list = list_change(signature_list)
    fileNum = len(filesName)
    s_result = []
    for index1, signatureSet1 in enumerate(signature_list):
        for index2, signatureSet2 in enumerate(signature_list):
            if (index1 < index2):
                s_result.append((calSimilarity(signatureSet1, signatureSet2), filesName[index1], filesName[index2]))
    return s_result



if __name__ == '__main__':
    dir_file = 'data/files'
    r = getShingleList(dir_file, 3)
    # print('hhh',getShingleList('data/', 3))
    signatureList = getMinHashSignature(r, 2)
    print('lsd', signatureList)

    # dir = "D://E07"  # 存放文档的文件夹路径
    filesName = get_files_name(dir_file)
    # shingleList = getShingleList(dir, 4)  # 此处数字控制取出的对比的字段的长度
    # signatureList = getMinHashSignature(shingleList, 100)  # 此处数字表示从代码中去的个数
    result = calAllSimilarity(signatureList, filesName)
    result.sort()
    result.reverse()
    for each in result:
        print('simi',each)

    # get_file_content('../Reduced/C000008/1036.txt')
