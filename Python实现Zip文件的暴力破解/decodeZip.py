import zipfile
import argparse
import os
from os.path import *

"""
这种方法的成功率比较依赖密码字典文件。虽然这只是一种初级的方法不过确实有的时候是非常有效的，通常情况下我们在遇到加密的Zip文件我们首先会尝试这种方法，如果实在破解不了，那就算了吧！Zip的加密形式还是比较复杂的，想要通过技术手段破解确实很难！
"""


def tryZipPwd(zipFile, savePath, password):
    """
    解压函数
    zipFile表示一个ZipFile对象
    savePath表示解压后文件存储的路径
    password表示解压ZipFile的密码
    这个函数在尝试密码之后会返回一个布尔值，如果解压成功会返回True，如果失败则会返回False
    """
    try:
        zipFile.extractall(path=savePath, pwd=password.encode('utf-8'))
        print('[+] Zip File decompression success,password: %s' % (password))
        return True
    except:
        print('[-] Zip File decompression failed,password: %s' % (password))
        return False


def main():
    # 这里用描述创建了ArgumentParser对象
    parser = argparse.ArgumentParser(description='Brute Crack Zip')
    # 添加-H命令dest可以理解为咱们解析时获取-H参数后面值的变量名,help是这个命令的帮助信息
    parser.add_argument('-f', dest='zFile', type=str, help='The zip file path.')
    parser.add_argument('-w', dest='pwdFile', type =str, help='Password dictionary file.')
    zFilePath = None
    pwdFilePath = None
    try:
        options = parser.parse_args()
        zFilePath = options.zFile      # 待解压文件路径
        pwdFilePath = options.pwdFile  # 密码文件路径
    except:
        print(parser.parse_args(['-h']))
        exit(0)

    if zFilePath == None or pwdFilePath == None:
        print(parser.parse_args(['-h']))
        exit(0)

    with zipfile.ZipFile(zFilePath) as zFile:  #  创建待解压对象
        with open(pwdFilePath) as f:
            for pwd in f.readlines():
                p,f = os.path.split(zFilePath)  # 获得文件存储路径与文件名称
                dirName = f.split('.')[0]      # 获得解压目录名称
                dirPath = os.path.join(p, dirName)  # 拼出解压路径
                try:
                    os.mkdir(dirPath) # 创建解压后文件存储的路径
                except:
                    pass
                # 调用函数tryZipPwd(解压对象，解压后文件存储的路径，解压密码))，解压成功返回True，失败返回False
                ok = tryZipPwd(zFile, dirPath, pwd.strip('\n')) # 
                if ok:
                    break
if __name__ == '__main__':
    main()