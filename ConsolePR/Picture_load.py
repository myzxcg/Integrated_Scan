# _*_coding:utf-8 _*_
# 随机加载图片
import random
import sys
from pyfiglet import Figlet


class ProgressBar:
    def __init__(self, count=0, total=0, width=50):
        self.count = count
        self.total = total
        self.width = width

    def move(self):
        self.count += 1

    def log(self, s):
        sys.stdout.write(' ' * (self.width + 9) + '\r')
        sys.stdout.flush()
        sys.stdout.write(s + '\r')
        sys.stdout.flush()
        progress = self.width * self.count / self.total
        sys.stdout.write('{0} / 100% '.format(s))
        sys.stdout.write('<' + '*' * progress + '-' * (self.width - progress) + '>' + '\r')

        if progress == self.width:
            sys.stdout.write('\n')
        sys.stdout.flush()


def picture():
    font = ['letters', 'banner', 'doh', 'cricket', 'slant', 'univers', 'starwars', 'rounded', 'roman', 'puffy',
            'pebbles', 'larry3d', 'epic']
    i = random.randint(0, len(font) - 1)
    fig = Figlet(font[i])
    print(fig.renderText('Integ.Scan'))
