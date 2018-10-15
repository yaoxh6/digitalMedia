#文件来自https://github.com/mvanveen/mcut
#cube.py文件主要声明了ColorCube的数据结构以及一些基本的方法
#主要的成员就是_color，用来表示一个颜色方块的所有颜色
#主要方法average，计算一个颜色方块RGB三种颜色的平均值
#主要方法split，将一个颜色方块按照某个颜色排序，并从中间一分为二
#因为这个文件比较简单，所以没有太多的修改，mediancut.py几乎重新写了
#所以主要还是看mediancut.py，主要的算法也在mediancut.py

from operator import itemgetter#导入的这个库，方便sorted函数使用排序

class ColorCube(object):
    _rmax = 255.#默认最大红色255
    _rmin = 0.#默认最小红色0
    _gmax = 255.#默认最大绿色255
    _gmin = 0.#默认最小绿色0
    _bmax = 255.#默认最大蓝色255
    _bmin = 0.#默认最小蓝色0

    def __init__(self, *colors):
        self._colors = colors or []
        self.resize()

    @property
    def colors(self):
        return self._colors

    @property
    def rsize(self):
        return self._rmax - self._rmin

    @property
    def gsize(self):
        return self._gmax - self._gmin

    @property
    def bsize(self):
        return self._bmax - self._bmin

    @property
    def size(self):
        return self.rsize, self.gsize, self.bsize

    def _average(self, col, length):
        return sum(col) / length

    #分别得到颜色方块中RGB的值
    def color_columns(self):
        return [
            [_[0] for _ in self.colors],
            [_[1] for _ in self.colors],
            [_[2] for _ in self.colors],
        ]

    #计算颜色方块中RGB的平均值，为了方便取整
    @property
    def average(self):
        length = len(self.colors)
        cols = self.color_columns()
        r, g, b = [self._average(col, length) for col in cols]
        return int(r), int(g), int(b)

    def resize(self):
        col_r, col_g, col_b = self.color_columns()
        self._rmin = min(col_r)
        self._rmax = max(col_r)
        self._gmin = min(col_g)
        self._gmax = max(col_g)
        self._bmin = min(col_b)
        self._bmax = max(col_b)

    def split(self, axis):
        self.resize()
        #axis是排序的参数，因为color是一个5元组(RGBij),i和j表示位置
        #所以axis可以取值0-4，分别对应按RGBij排序
        self._colors = sorted(self.colors, key=itemgetter(axis))

        #找到中间位置，必须使用"//"符号，否则会报错
        med_idx = len(self.colors) // 2

        #分割成两块
        return (
            ColorCube(*self.colors[:med_idx]),
            ColorCube(*self.colors[med_idx:]
        ))
