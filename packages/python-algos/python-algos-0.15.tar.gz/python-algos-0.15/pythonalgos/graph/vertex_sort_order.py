from enum import Enum

""" Enum class that determines the order on which algortihms acces vertices """


class VertexSortOrder(Enum):
    ASC = "asc"
    DESC = "desc"
    NATURAL = "natural"
