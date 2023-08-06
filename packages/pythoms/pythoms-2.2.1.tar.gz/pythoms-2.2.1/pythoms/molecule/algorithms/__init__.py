from .multiplicative import isotope_pattern_multiplicative
from .combinatoric import isotope_pattern_combinatoric, isotope_pattern_hybrid
from .simulated import gaussian_isotope_pattern
from .isospec import isotope_pattern_isospec
from .bar import bar_isotope_pattern, VALID_DROPMETHODS, VALID_GROUP_METHODS

# valid isotope pattern generation methods
VALID_IPMETHODS = [
    'combinatorics',
    'multiplicative',
    'hybrid',
    'isospec',  # uses isospecpy package
    # 'cuda',
]

__all__ = [
    'VALID_IPMETHODS',
    'VALID_DROPMETHODS',
    'VALID_GROUP_METHODS',
    'isotope_pattern_multiplicative',
    'isotope_pattern_combinatoric',
    'isotope_pattern_hybrid',
    'gaussian_isotope_pattern',
    'isotope_pattern_isospec',
    'bar_isotope_pattern',
]
