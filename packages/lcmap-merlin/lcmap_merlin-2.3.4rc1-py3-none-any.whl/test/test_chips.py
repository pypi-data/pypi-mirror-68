from base64 import b64decode
from base64 import b64encode
from cytoolz import concat
from cytoolz import drop
from cytoolz import first
from cytoolz import filter
from merlin import cfg
from merlin import chips
from merlin import specs
from functools import partial
from functools import reduce
from itertools import product
from numpy.random import randint
import numpy as np
import test

   
def test_locations():
    params = {'x': 0,
              'y': 0,
              'cw': 2,
              'ch': 2,
              'rx': 1,
              'ry': -1,
              'sx': 60,
              'sy': 60}

    locs = np.array([[[0, 0], [30, 0]], [[0, -30], [30, -30]]])
    assert np.array_equal(locs, chips.locations(**params))
    

def test_dates():
    inputs = list()
    inputs.append({'acquired': '2015-04-01'})
    inputs.append({'acquired': '2017-04-01'})
    inputs.append({'acquired': '2017-01-01'})
    inputs.append({'acquired': '2016-04-01'})
    assert set(chips.dates(inputs)) == set(map(lambda d: d['acquired'], inputs))


def test_trim():
    inputs = list()
    inputs.append({'include': True, 'acquired': '2015-04-01'})
    inputs.append({'include': True, 'acquired': '2017-04-01'})
    inputs.append({'include': False, 'acquired': '2017-01-01'})
    inputs.append({'include': True, 'acquired': '2016-04-01'})
    included = chips.dates(filter(lambda d: d['include'] is True, inputs))
    trimmed = chips.trim(dates=included, chips=inputs)
    assert len(list(trimmed)) == len(included)
    assert set(included) == set(map(lambda x: x['acquired'], trimmed))


def test_decode():
    input_data  = b'[1, 2, 3, 4]'
    input_chip  = {'data': b64encode(input_data)}
    output_chip = chips.decode(input_chip)
    assert input_data == output_chip['data']

    
def test_chip_to_numpy():
    data_type = 'int16'
    data_shape = [2, 2]

    input_data = np.array([1, 2, 3, 4], dtype=data_type).reshape(data_shape)
    input_chip = {'data': input_data}
    
    output_chip = chips.chip_to_numpy(chip=input_chip,
                                      chip_spec={'data_shape': data_shape,
                                                 'data_type': data_type})
    output_data = output_chip.get('data')
    
    assert np.array_equal(input_data, output_data)
   

def test_to_numpy():
    """ Builds combos of shapes and numpy data types and tests
        chipmunk.to_numpy() with all of them """

    def _ubid(dtype, shape):
        return dtype + str(shape)

    def _chip(dtype, shape, ubid):
        limits = np.iinfo(dtype)
        length = reduce(lambda accum, v: accum * v, shape)
        matrix = randint(limits.min, limits.max, length, dtype).reshape(shape)
        return {'ubid': ubid, 'data': matrix}

    def _spec(dtype, shape, ubid):
        return {'ubid': ubid, 'data_shape': shape, 'data_type': dtype.upper()}

    def _check(npchip, spec_index):
        spec = spec_index[npchip['ubid']]
        assert npchip['data'].dtype.name == spec['data_type'].lower()
        assert npchip['data'].shape == spec['data_shape']
        return True

    # Test combos of dtypes/shapes to ensure data shape and type are unaltered
    combos = tuple(product(('uint8', 'uint16', 'int8', 'int16'),
                           ((3, 3), (1, 1), (100, 100))))

    # generate the chip_specs and chips
    _chips = [_chip(*c, _ubid(*c)) for c in combos]
    _specs = [_spec(*c, _ubid(*c)) for c in combos]
    _spec_index = specs.index(_specs)

    # run assertions
    checker = partial(_check, spec_index=_spec_index)
    all(map(checker, chips.to_numpy(spec_index=_spec_index, chips=_chips)))


def test_identity():
    chip = {'x': 1, 'y': 2, 'acquired': '1980-01-01', 'ubid': 'a/b/c/d'}
    assert chips.identity(chip) == tuple([chip['x'], chip['y'],
                                          chip['ubid'], chip['acquired']])


def test_deduplicate():
    inputs = [{'x': 1, 'y': 2, 'acquired': '1980-01-01', 'ubid': 'a/b/c/d'},
              {'x': 1, 'y': 2, 'acquired': '1980-01-01', 'ubid': 'a/b/c/d'},
              {'x': 2, 'y': 2, 'acquired': '1980-01-01', 'ubid': 'a/b/c/d'},
              {'x': 1, 'y': 3, 'acquired': '1980-01-01', 'ubid': 'a/b/c/d'},
              {'x': 1, 'y': 2, 'acquired': '1980-01-02', 'ubid': 'a/b/c/d'},
              {'x': 1, 'y': 2, 'acquired': '1980-01-01', 'ubid': 'a/b/c'}]

    assert chips.deduplicate(inputs) == tuple(drop(1, inputs))


@test.vcr.use_cassette(test.cassette)
def test_mapped():
    _cfg = cfg.get('chipmunk-ard', env=test.ard_env)
    
    chipmap = chips.mapped(x=test.x,
                           y=test.y,
                           acquired=test.ard_acquired,
                           specmap=specs.mapped(ubids=cfg.ubids.get('chipmunk-ard'),
                                                specs=_cfg.get('registry_fn')()),
                           chips_fn=_cfg.get('chips_fn'))

    assert len(chipmap) > 0
    assert all(map(lambda x: type(x) is dict, concat(chipmap.values())))
    assert len(list(concat(chipmap.values()))) > 0


def test_rsort():
    chipseq = [{'acquired': 3}, {'acquired': 1}, {'acquired': 2}]
    assert [3, 2, 1] == list(map(lambda x: x['acquired'], chips.rsort(chipseq)))
