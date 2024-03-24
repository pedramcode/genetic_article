

class Vector2D:
    __x: int
    __y: int

    def __init__(self, x: int, y: int) -> None:
        self.__x = x
        self.__y = y
    
    def set_x(self, x: int) -> None:
        self.__x = x
    
    def set_y(self, y: int) -> None:
        self.__y = y
    
    @property
    def x(self) -> int:
        return self.__x
    
    @property
    def y(self) -> int:
        return self.__y

