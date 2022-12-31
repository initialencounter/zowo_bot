from os.path import exists
from PIL import Image
from random import randint
from time import time,gmtime,strftime
from io import BytesIO
class Klotsk:

    def __init__(self, mode):
        self.cmd_strs = ''
        self.theme = []
        if exists(f'./src/plugins/klotsk/theme/{mode}{mode}.png'):
            img = Image.open(f'./src/plugins/klotsk/theme/{mode}{mode}.png')
        else:
            img = Image.open(f'./theme/{mode}{mode}.png')
        self.sl = 720 / mode
        for i in range(mode):                               # 剪切图片
            for j in range(mode):
                self.theme.append(img.crop((j * self.sl, i * self.sl, (j + 1) * self.sl, (i + 1) * self.sl)))
        self.drctn_dist = {'U': [-1, 0], 'D': [1, 0], 'L': [0, -1], 'R': [0, 1]}
        self.drctn_list = ['U', 'D', 'L', 'R']
        self.mode = mode
        self.klotsk = []
        self.num = 1
        self.crtpuzzle = []
        for i in range(self.mode):  # 生成数组
            tmp = []
            for j in range(self.mode):
                tmp.append(self.num)
                self.num += 1
            self.crtpuzzle.append(tmp[:])
            self.klotsk.append(tmp[:])
        self.crtpuzzle[-1][-1] = 0
        self.klotsk[-1][-1] = 0
        self.start_time = time()                   #计时开始
        self.end_time = 0
        self.shfl()

    def find_0(self):
        for i in range(self.mode):                      # 找出空的位置
            for j in range(self.mode):
                if self.klotsk[i][j] == 0:
                    return [i, j]

    def move(self, drctn):                          # 移动0
        pstn = self.find_0()
        r, c = pstn
        if r == 0 and drctn == 'U':  # 判断是否可以移动
            return ''
        elif r == self.mode - 1 and drctn == 'D':
            return  ''
        elif c == 0 and drctn == 'L':
            return ''
        elif c == self.mode - 1 and drctn == 'R':
            return  ''
        self.klotsk[r][c], self.klotsk[r + self.drctn_dist[drctn][0]][c + self.drctn_dist[drctn][1]] = \
            self.klotsk[r + self.drctn_dist[drctn][0]][c + self.drctn_dist[drctn][1]], self.klotsk[r][c]
        return drctn
    def check(self):
        for i in range(self.mode):                          # 生成数组
            for j in range(self.mode):
                if self.klotsk[i][j]!=self.crtpuzzle[i][j]:
                    return False
        return True
    def move_sqnc(self, sqnc):                      #移动命令序列，并判断是否还原
        self.cmd_strs=''
        for i in sqnc:
            com_str = self.move(i)
            self.cmd_strs+=com_str
            if self.check():
                dt = self.duration()
                print(f'已还原,用时{dt}')
                self.printf()
                return True
        for i in self.klotsk:
            print(i)
        print('\n\n---------------\n\n')
        return False

    def shfl(self):                             # 打乱puzzle
        for i in range(1000):
            rd = randint(0,3)
            self.move(self.drctn_list[rd])

    def printf(self):
        for i in self.klotsk:
            for j in i:
                print(j,end=' ')
            print()

    def duration(self) -> str:                  #计时方法
        dt = time() - self.start_time
        ms = str(dt).split('.')[1][:3]
        return strftime('%H:%M:%S:', gmtime(dt)) + ms

    def Draw_puzzle(self):                              #画图
        self.canvas = Image.new('RGB', (720, 720))
        for i in range(self.mode*self.mode):
            y = i%self.mode
            x = i//self.mode
            xx = int(x*self.sl)
            yy = int(y*self.sl)
            self.canvas.paste(self.theme[self.klotsk[y][x]-1],(xx,yy))

    def toJson(self):                           #img转数据流
        self.Draw_puzzle()
        image = self.canvas
        buf = BytesIO()
        image.save(buf, format='png')

        return buf
if __name__ == '__main__':
    k = Klotsk(5)
    k.printf()
    k.Draw_puzzle()
    k.canvas.save('./theme/test1.png')
    k.move_sqnc('R')
    k.Draw_puzzle()
    k.canvas.save('./theme/test2.png')
    # 定义一个函数，用于判断数码华容道是否有解
