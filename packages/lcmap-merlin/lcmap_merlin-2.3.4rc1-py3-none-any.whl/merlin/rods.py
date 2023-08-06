from functools import partial
from cytoolz import excepts
from cytoolz import thread_last
from merlin import chips
import numpy as np

def from_chips(chips):
    """Accepts sequences of chips and returns
    time series pixel rods organized by x, y, t for all chips.
    Chips should be sorted as desired before calling rods() as outputs
    preserve input order.

    Args:
        chips: sequence of chips with data as numpy arrays

    Returns:
        3d numpy array organized by x, y, and t.  Output shape matches
        input chip shape with the chip value replaced by
        another numpy array of chip time series values

    1. For each chip add data to master numpy array.
    2. Transpose the master array
    3. Horizontally stack the transposed master array elements
    4. Reshape the master array to match incoming chip dimensions
    5. Pixel rods are now organized for timeseries access by x, y, t

    >>> chip_one   = np.int_([[11, 12, 13],
                              [14, 15, 16],
                              [17, 18, 19]])
    >>> chip_two   = np.int_([[21, 22, 23],
                              [24, 25, 26],
                              [27, 28, 29]])
    >>> chip_three  = np.int_([[31, 32, 33],
                               [34, 35, 36],
                               [37, 38, 39]])
    >>> master = np.conj([chip_one, chip_two, chip_three])
    >>> np.hstack(master.T).reshape(3, 3, -1)
    array([[[ 11, 21, 31], [ 12, 22, 32], [ 13, 23, 33]],
           [[ 14, 24, 34], [ 15, 25, 35], [ 16, 26, 36]],
           [[ 17, 27, 37], [ 18, 28, 38], [ 19, 29, 39]]])
    """
    
    master = np.conj([c['data'] for c in chips])
    return np.hstack(master.T).reshape(*master[0].shape, -1)


def locate(rods, locations):
    """Combines location information with pixel rods.

    Args:
        rods: Chip shaped numpy array of rods
        locations:  Chip shaped numpy array of locations

    Returns:
        dict: (location):rod for each location and rod in the arrays.

    Incoming locations as 3d array:

    >>> array([[[0,0], [0,1], [0,2]],
               [[1,0], [1,1], [1,2]],
               [[2,0], [2,1], [2,2]]])

    Incoming rods also as 3d array:

    >>> array([[[110,110,234,664], [23,887,110,111], [110,464,223,112]],
               [[111,887,1,110],   [33,111,12,111],  [0,111,66,112]],
               [[12,99,112,110],   [112,87,231,111], [112,45,47,112]]])

    locrods converts locations to:

    >>> locations.reshape(locations.shape[0] * locations.shape[1], -1)
    array([[0, 0],
           [0, 1],
           [0, 2],
           [1, 0],
           [1, 1],
           [1, 2],
           [2, 0],
           [2, 1],
           [2, 2]])

    And rods to:

    >>> rods.reshape(rods.shape[0] * rods.shape[1], -1)
    array([[110, 110, 234, 664],
           [23,  887, 110, 111],
           [110, 464, 223, 112],
           [111, 887, 1,   110],
           [33,  111, 12,  111],
           [0,   111, 66,  112],
           [12,  99,  112, 110],
           [112, 87,  231, 111],
           [112, 45,  47,  112]])

    Then the locations and rods are zipped together via a dictionary
    comprehension and returned.

    >>> {
         (0,0): [110, 110, 234, 664],
         (0,1): [23,  887, 110, 111],
         (0,2): [110, 464, 223, 112],
         (1,0): [111, 887, 1,   110],
         (1,1): [33,  111, 12,  111],
         (1,2): [0,   111, 66,  112],
         (2,0): [12,  99,  112, 110],
         (2,1): [112, 87,  231, 111],
         (2,2): [112, 45,  47,  112]
        }
    """

    flat_locs = locations.reshape(locations.shape[0] * locations.shape[1], -1)
    flat_rods = rods.reshape(rods.shape[0] * rods.shape[1], -1)
    return {tuple(k): v for k, v in zip(flat_locs, flat_rods)}


def identify(rod, x, y):
    """Adds chip ids (chip_x, chip_y) to the key for a rod

    Args:
        rod: dict of (x, y): [values]
        x: x coordinate that identifies the source chip
        y: y coordinate that identifies the source chip
        
    Returns:
        dict: {(chip_x, chip_y, x, y): [values]}
    """

    return {(x, y, k[0], k[1]): v for k, v in rod.items()}


def create(x, y, chipseq, dateseq, locations, spec_index, decode_fn):
    """Transforms a sequence of chips into a sequence of rods
       filtered by date, deduplicated, sorted, located and identified.

       Args:
           x (int): x projection coordinate of chip
           y (int): y projection coordinate of chip
           chipseq (seq): sequence of chips
           dates (seq): sequence of dates that should be included in the rods
           locations (numpy.Array): 2d numpy array of pixel coordinates
           spec_index (dict): specs indexed by ubid
           decode_fn (fn): Function that accepts a chip and returns a decoded chip
                           (See chips.decode)

       Returns:
           dict: {(chip_x, chip_y, x, y): {'k1': [], 'k2': [], 'k3': [], ...}}
    """
    
    return thread_last(chipseq,
                       partial(chips.trim, dates=dateseq),
                       chips.deduplicate,
                       chips.rsort,
                       partial(map, decode_fn),
                       partial(chips.to_numpy, spec_index=spec_index),
                       excepts(ValueError, from_chips, lambda _: []),
                       excepts(AttributeError, partial(locate, locations=locations), lambda _: {}),
                       partial(identify, x=x, y=y))

