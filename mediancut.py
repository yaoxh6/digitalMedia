
from PIL import Image
#导入的是已经写好的cube.py包
from cube import ColorCube

#使用下面两个全局变量，cubes是为了位置信息，colorTable是为了颜色信息，这两个文件是有映射关系的
cubes = []#记录着所有的颜色方块的所有信息，最终结果是排好8次序的5元组，包含位置信息，也就是整个图片的所有信息都在
colorTable = []#记录着颜色表，一共记录着256种颜色

#自己重新写了得到颜色的函数，直接用getcolors的话会得到类似((该种颜色的数量(R1,G1,B1)),......)数据结构，没有存储位置信息
#所以抛弃了这种写法，而是整个遍历一遍得到每个像素的RGB以及位置信息，并且作为5元组放到color中
def get_colors(image):
    color = []
    h = image.size[0]
    w = image.size[1]
    for i in range(0,h):
        for j in range(0,w):
            color.append(image.getpixel((i,j))+(i,j))
    return color

#中位切割法
def medianCut(image):
    colors = get_colors(image)
    global cubes
    cubes = [ColorCube(*colors)]
    tempCube = cubes#先把cubes赋值给tempCube，因为用的是分割，如果直接在cubes上操作，会造成序号混乱
    for time in range(0,9):#循环9次，原因是第8次循环结束，没有cubes = tempCube，所以还需要一次
        if((time+1)%3 == 1):
            chooseColor = 0#如果是循环第0，3，6次，按照红色排序
        elif((time+1)%3 == 2):
            chooseColor = 1#如果是循环第1，4，7次，按照绿色排序
        else:
            chooseColor = 2#如果是循环第2，5次，按照蓝色排序
        cubes = tempCube
        for next in range(0,len(cubes)):#next表示将要做分割的颜色块的序号，可以看成是二叉树
            split_box = cubes[next]#得到将要做分割的颜色块
            cube_a, cube_b = split_box.split(chooseColor)#将颜色块做分割，得到的两块是cube_a,cube_b
            #将分离的两块拼接到tempCube中，而不是拼接到cubes中，同样分割的时候是分割cubes，而不是tempCube
            #另外一个是tempCube[:next]，不包含next，tempCube[next+2]，包含next+2，所以中间空出两个位置给刚分裂的两个
            #为什么不用next序号，因为分裂之后next自动加一，本身又占有一个位置，所以如果再分裂直接用刚分裂完的位置向下分裂
            #否则会造成颜色的覆盖，运行时间也会变成十倍
            tempCube = tempCube[:next] + [cube_a, cube_b] + tempCube[next + 2:]
    return [c.average for c in cubes]#返回的256个颜色块的每块的RGB平均值

#利用中位切割定理修改图片
def changeImage(Image):
    global colorTable
    colorTable = medianCut(Image)
    h = Image.size[0]
    w = Image.size[1]
    for i in range(0,len(cubes)):
        for j in range(0,len(cubes[i].colors)):
            #位置信息是cubes中color成员的后两位，因为color是5元组，所以第3和第4位是位置
            #颜色信息是colorTable的三位，分别是RGB的值，也就是说很多不同的位置，对应着相同的颜色
            #这个相同的颜色是由这么多不同位置的颜色平均得到的
            Image.putpixel((cubes[i].colors[j][3],cubes[i].colors[j][4]),(colorTable[i][0],colorTable[i][1],colorTable[i][2]))
            #Image.putpixel((cubes[i].colors[j][3],cubes[i].colors[j][4]),(cubes[i].colors[j][0],cubes[i].colors[j][1],cubes[i].colors[j][2])) #原图，如果想显示原图，使用此行

def main():
    img = Image.open('redapple.jpg')
    changeImage(img)
    img.show()
    img.save('result.jpg')
main()