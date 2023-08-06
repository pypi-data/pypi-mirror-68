#求根公式 x = (-b±√(b²-4ac)) / 2a
import math
def quadratic_equation(a, b, c):
    #求平方根的方法
    t = math.sqrt(b * b - 4 * a * c)
    return (-b + t) / (2 * a),( -b - t )/ (2 * a)

