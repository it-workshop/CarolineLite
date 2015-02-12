# -*- coding: utf_8 -*-

import numpy as np
import numpy.linalg as linalg

# пример для матриц камеры

# координаты первой камеры относительно глобальной системы (-1, 0, 0)
# второй - (100, 0, 0)
# нет поворота относительно осей

focus_length = 1000
width = 640
height = 480

K1 = np.matrix([[focus_length, 0, width],[0,focus_length,height],[0,0,1]])
K2 = K1

# матрица внешних параметров. RT = [R | T], R = транспонированная матрица поворота,
# T = -1 * матрица поворота * вектор координат относительно глобальной системы
RT1 = np.matrix([[1, 0, 0, 1], [0, 1, 0, 0], [0, 0, 1, 0]])
RT2 = np.matrix([[1, 0, 0, -100], [0, 1, 0, 0], [0, 0, 1, 0]])
temp = [[1,0,0],[0,1,0],[0,0,1]]

# соответствующие точки на 1 и 2 картинке
# лежат на 1 прямой, лежащей в одной плоскости с прямой, проходящей через центры камер
# так что ответ будет тоже лежать в той - же плоскости (плоскость 0xz)
x1 = np.matrix([[800], [480], [1]])
x2 = np.matrix([[480], [480], [1]])

P1 = K1 * RT1
P2 = K2 * RT2

PROJ1 = linalg.pinv(P1) * x1
PROJ2 = linalg.pinv(P2) * x2

PROJ1 = PROJ1 / PROJ1[3]
PROJ2 = PROJ2 / PROJ2[3]

# точка пересечения прямых L1 = (X1, X1') и L2 = (X2, X2') - нужная точка в 3D.
# т.к они не пересекутся, то решаем d(L1, x)^2 + d(L2, x)^2 -> min (x из R^3)
print "X1 : coordinates of first point"
print [-1, 0, 0]
print "X1' : coordinates of first point in projective space, first 3 = point in R^3 (because x4 = 1)"
print PROJ1
print "X2 : coordinates of second point"
print [100, 0, 0]
print "X2' : coordinates of second point in projective space, first 3 = point in R^3 (x4 = 1)"
print PROJ2

# тут можно еще дотриангулировать.

