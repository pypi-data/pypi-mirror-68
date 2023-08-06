import enum

class SortType(enum.Enum):
    BRIGHTNESS = enum.auto()
    AVG        = enum.auto()

    # RGB modes
    RGB        = enum.auto()
    RBG        = enum.auto()
    BRG        = enum.auto()
    BGR        = enum.auto()
    GRB        = enum.auto()
    GBR        = enum.auto()

    # RGB modes with clipping
    RGBC       = enum.auto()
    RBGC       = enum.auto()
    BRGC       = enum.auto()
    BGRC       = enum.auto()
    GRBC       = enum.auto()
    GBRC       = enum.auto()

# TODO
#     LAB        = enum.auto()
#     LBA        = enum.auto()
#     BLA        = enum.auto()
#     BAL        = enum.auto()
#     ABL        = enum.auto()
#     ALB        = enum.auto()
#
#     HSV        = enum.auto()
#     HVS        = enum.auto()
#     VHS        = enum.auto()
#     VSH        = enum.auto()
#     SVH        = enum.auto()
#     SHV        = enum.auto()

    @staticmethod
    def from_str(sort_type: str) -> 'SortType':
        return getattr(SortType, sort_type.upper())

_CLIPS = {
    SortType.RGBC: SortType.RGB,
    SortType.RBGC: SortType.RBG,
    SortType.BGRC: SortType.BGR,
    SortType.BRGC: SortType.BRG,
    SortType.GRBC: SortType.GRB,
    SortType.GBRC: SortType.GBR,
}

def is_clip(sort_type: SortType) -> bool:
    return sort_type in _CLIPS.keys()

def unclip(sort_type: SortType) -> SortType:
    return _CLIPS.get(sort_type, sort_type)
