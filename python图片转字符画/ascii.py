# -*- coding=utf-8 -*-

from PIL import Image
import argparse

#首先，构建命令行输入参数处理 ArgumentParser 实例
parser = argparse.ArgumentParser()

# 通过add_argument()方法添加各种参数。添加参数的过程就是，反复调用add_argument()方法，一次加入一个参数
# 定义输入文件、输出文件、输出字符画的宽和高
parser.add_argument('file')     #输入文件
parser.add_argument('-o', '--output')   #输出文件
parser.add_argument('-w', '--width', type = int, default = 80) #输出字符画宽
parser.add_argument('-he', '--height', type = int, default = 80) # 输出字符画高

# 解析并获取参数
args = parser.parse_args()

IMG = args.file  # 输入的图片文件路径
WIDTH = args.width  # 输出字符画的宽度
HEIGHT = args.height  # 输出字符画的高度
OUTPUT = args.output  # 输出字符画的路径

ascii_char = list("$@B%8&WM#*oAahHIkKbdDpPqQeEwmZO0Q23456790LCuUYXzcvVnNxrRsSjJfFgGtT/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# 将256灰度映射到70个字符上
def get_char(r,g,b,alpha = 256):
    #  alpha 值为 0 的时候表示图片中该位置为空白
    if alpha == 0:
        return ' '

    # 获取字符集的长度，这里为 70
    length = len(ascii_char)

     # 将 RGB 值转为灰度值 gray，灰度值范围为 0-255# 获取字符集的长度，这里为 70
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    # 灰度值范围为 0-255，而字符集只有 70
    # 需要进行如下处理才能将灰度值映射到指定的字符上
    # gary / 256 == x / len(ascii_char)
    # 防止分母为0，需加1
    unit = (256.0 + 1)/length

    # 返回灰度值对应的字符
    return ascii_char[int(gray/unit)]

if __name__ == '__main__':

    # 打开图片文件，获得对象im
    im = Image.open(IMG)  
    # 使用 PIL 库的 im.resize() 调整图片大小对应到输出的字符画的宽度和高度，注意这个函数第二个参数使用 Image.NEAREST，表示输出低质量的图片
    # NEAREST：最近滤波。从输入图像中选取最近的像素作为输出像素。它忽略了所有其他的像素
    im = im.resize((WIDTH,HEIGHT), Image.NEAREST)

    # 遍历图片中的每一行
    txt = ""

    # 遍历该行中的每一列
    for i in range(HEIGHT):
        # 遍历该行中的每一列
        for j in range(WIDTH):
            # 将 (j,i) 坐标的 RGB 像素转为字符后添加到 txt 字符串
            # im.getpixel(xy)：返回给定位置的像素。如果图像是多层图像，则此方法返回元组
            # im.getpixel((j,i)) 获取得到坐标 (j,i) 位置的 RGB 像素值（有的时候会包含 alpha 值），返回的结果是一个元组，例如 (1,2,3) 或者 (1,2,3,0)。我们使用 * 可以将元组作为参数传递给 get_char，同时元组中的每个元素都对应到 get_char 函数的每个参数
            txt += get_char(*im.getpixel((j,i))) 
        # 遍历完一行后需要增加换行符 
        txt += '\n'

    # 输出到屏幕
    print(txt)
    
    #字符画输出到文件
    if OUTPUT:
        with open(OUTPUT,'w') as f:
            f.write(txt)
    else:
        with open("output.txt",'w') as f:
            f.write(txt)