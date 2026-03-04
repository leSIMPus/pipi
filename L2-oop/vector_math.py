import math
from numbers import Number

class Vector:
    def __init__(self, *args):
        if not args:
            raise ValueError("Вектор не может быть пустым.")

        for coordinate in args:
            if not isinstance(coordinate, Number):
                raise TypeError("Координаты должны быть числами.")

        self.coordinates = list(args)

    def __str__(self):
        coordianates_str = ', '.join(str(coordinate) for coordinate in self.coordinates)
        return  f"Вектор({coordianates_str})"

    def __len__(self):
        return len(self.coordinates)

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Можно складывать только векторы.")

        if len(self) != len(other):
            raise ValueError("Векторы разной размерности.")

        result_coordinates = [a+b for a,b in zip(self.coordinates, other.coordinates)]
        return Vector(*result_coordinates)

    def __mul__(self, other):
        if isinstance(other, Number):
            result_coordinates = [coordinate * other for coordinate in self.coordinates]
            return Vector(*result_coordinates)

        elif isinstance(other, Vector):
            if len(self) != len(other):
                raise ValueError("Векторы разной размерности.")

            scalar = sum(a*b for a,b in zip(self.coordinates, other.coordinates))
            return scalar

        else:
            raise TypeError("Можно умножать только на вектор или число.")

    @property
    def norm(self):
        return math.sqrt(sum(coordinate**2 for coordinate in self.coordinates))

    