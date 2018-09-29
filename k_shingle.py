# encoding:utf-8
__author__ = "li shi di"
import os
import chardet
import jieba

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
        shingle = set()
        for index in range(0, len(fileContent) - k + 1):
            shingle.add(fileContent[index:index + k])
        shingleList.append(shingle)
    return shingleList

if __name__ == '__main__':
    print('hhh',getShingleList('../Reduced', 3))
    # get_file_content('../Reduced/C000008/1036.txt')
