"""
Hexagonal Lattice
Data Structure of Coordinates

@Author: LZK
@Date: 2023-5-31
"""
from collections import OrderedDict

# Class declarations
class CubeCoordinate: pass
class OffsetCoordinate: pass
class RingCoordinate: pass

# Class implementations
class Coordinate:
    
    def __init__(self, coordinate_type: str, value: list) -> None:
        if coordinate_type == 'cube':
            self._value = CubeCoordinate(value=value)
        elif coordinate_type == 'offset':
            value = OffsetCoordinate(value=value)
            self._value = value.to_cube()
        else:
            raise ValueError(f"Invalid coordinate type: {coordinate_type}")
        
        if not self._check_value():
            raise ValueError(f"Input value is invalid: [{coordinate_type}, {value}].")

    def _check_value(self) -> bool:
        return self._value._check_value()

    @property
    def value(self) -> list:
        return self.value
    
    def __str__(self) -> str:
        return self._value.__str__()


class CubeCoordinate:

    def __init__(self, x: int = None, y: int = None, z: int = None, value: list = None) -> None:
        """
        Data structure of the cube coordinate of hexagonal lattice

        Input
        -----
        x: int, namely q, from bottom-left to top-right
        y: int, namely s, from bottom-right to top-left
        z: int, namely r, from top to bottom
        value: list of int, (x, y, z)
        """
        if value:
            self._x, self._y, self._z = list(map(int, value))
        else:
            self._x = int(x)
            self._y = int(y)
            self._z = int(z)
        if not self._check_value():
            raise ValueError(f"Input value is invalid: ({self._x}, {self._y}, {self._z})")
    
    def _check_value(self) -> bool:
        return self._x + self._y + self._z == 0

    @property
    def x(self) -> int:
        return self._x
    
    @property
    def y(self) -> int:
        return self._y
    
    @property
    def z(self) -> int:
        return self._z
    
    @property
    def direction_vectors_dict(self) -> OrderedDict:
        # Normalized vectors at six directions
        return OrderedDict(tuple((
            ('bottom-right', CubeCoordinate( 0, -1, +1)),
            ('bottom-left' , CubeCoordinate(-1,  0, +1)),
            ('left'        , CubeCoordinate(-1, +1,  0)),
            ('top-left'    , CubeCoordinate( 0, +1, -1)),
            ('top-right'   , CubeCoordinate(+1,  0, -1)),
            ('right'       , CubeCoordinate(+1, -1,  0))
        )))

    def to_list(self) -> list:
        return [self._x, self._y, self._z]

    def to_offset(self) -> OffsetCoordinate:
        col = self._x + (self._z - (self._z & 1)) / 2
        row = self._z
        return OffsetCoordinate(r=row, c=col)
    
    def to_ring(self) -> RingCoordinate:
        r = (abs(self._x) + abs(self._y) + abs(self._z)) / 2  # Manhattan distance to the original point

        if r == 0:
            return RingCoordinate(r=0, k=0)
        
        k = 0
        for _ in self.get_ring():
            if _ == self:
                break
            k += 1
        
        return RingCoordinate(r=r, k=k)
    
    def get_all_neighbours(self) -> list:
        res = list()
        for directon_vector in self.direction_vectors_dict.values():
            res.append(self + directon_vector)
        return res
    
    def get_neighbour(self, direction: CubeCoordinate or list or str) -> CubeCoordinate:
        """
        Get the neighnour coordinate at given direction

        Input
        -----
        direction: CubeCoordinate or list or str, the directon vector, which can be
        ```python
        {
            ('bottom-right', CubeCoordinate( 0, -1, +1)),
            ('bottom-left' , CubeCoordinate(-1,  0, +1)),
            ('left'        , CubeCoordinate(-1, +1,  0)),
            ('top-left'    , CubeCoordinate( 0, +1, -1)),
            ('top-right'   , CubeCoordinate(+1,  0, -1)),
            ('right'       , CubeCoordinate(+1, -1,  0))
        }
        ```
        """
        if type(direction) is list:
            direction = CubeCoordinate(value=direction).normalize()
        elif type(direction) is str:
            direction = self.direction_vectors_dict[direction]
        
        # Check direction
        is_valid = False
        for standard_direction in self.direction_vectors_dict.values():
            if direction == standard_direction:
                is_valid = True
                break
        if not is_valid:
            raise ValueError(f"{direction} is not a valid direction vector.")

        return self + direction

    def get_ring(self) -> list:
        """
        Get the coordinates at given ring

        Result Order
        ------------
        ```
          6  1
        5      2
          4  3
        ```
        """
        ring = int((abs(self._x) + abs(self._y) + abs(self._z)) / 2)  # Manhattan distance to the original point
        
        if ring == 0:
            return [self]
        
        next_ = ring * self.direction_vectors_dict['top-right']
        direction_vectors_list = list(self.direction_vectors_dict.values())

        res = list()
        for i in range(0, 6):
            for k in range(0, ring):
                res.append(next_)
                next_ = next_.get_neighbour(direction=direction_vectors_list[i])

        return res

    def __str__(self) -> str:
        return f"CubeCoordinate({self._x}, {self._y}, {self._z})"
    
    def __eq__(self, other: CubeCoordinate) -> bool:
        if self._x != other.x: return False
        if self._y != other.y: return False
        if self._z != other.z: return False
        return True
    
    def __add__(self, other: CubeCoordinate) -> CubeCoordinate:
        return CubeCoordinate(
            x = self._x + other.x,
            y = self._y + other.y,
            z = self._z + other.z
        )
    
    def __rmul__(self, factor: int) -> CubeCoordinate:
        return CubeCoordinate(
            x = factor * self._x,
            y = factor * self._y,
            z = factor * self._z
        )

    def normalize(self) -> CubeCoordinate:
        return CubeCoordinate(
            x = self._x / abs(self._x) if self._x != 0 else 0,
            y = self._y / abs(self._z) if self._y != 0 else 0,
            z = self._z / abs(self._z) if self._z != 0 else 0
        )


class OffsetCoordinate:

    def __init__(self, r: int = None, c: int = None, value: list = None) -> None:
        """
        Data structure of the offset coordinate

        Input
        -----
        r: int, the row number
        c: int, the column number
        value: list of int, (r, c)
        """
        if value:
            self._r, self._c = list(map(int, value))
        else:
            self._r = int(r)
            self._c = int(c)

    @property
    def r(self) -> int:
        return self._r
    
    @property
    def c(self) -> int:
        return self._c

    def to_cube(self) -> CubeCoordinate:
        x = self._c - (self._r - (self._r & 1)) / 2
        z = self._r
        y = - x - z
        return CubeCoordinate(x=x, y=y, z=z)
    
    def __str__(self) -> str:
        return f"OffsetCoordinate({self._r}, {self._c})"


class RingCoordinate:

    def __init__(self, r: int = None, k: int = None, value: list = None) -> None:
        if value:
            self._r, self._k = list(map(int, value))
        else:
            self._r = int(r)
            self._k = int(k)
    
    @property
    def r(self) -> int:
        return self._r
    
    @property
    def k(self) -> int:
        return self._k
    
    def to_cube(self) -> CubeCoordinate:
        start_point = CubeCoordinate(
            x = +self._r,
            y = 0,
            z = -self._r
        )
        for cube_coor in start_point.get_ring():
            ring_coor = cube_coor.to_ring()
            if self == ring_coor:
                return cube_coor

    def __str__(self) -> str:
        return f"RingCoordinate({self._r}, {self._k})"

    def __eq__(self, other: RingCoordinate) -> bool:
        if self._r != other.r: return False
        if self._k != other.k: return False
        return True
