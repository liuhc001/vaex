import pytest
from common import *


def test_values(ds_local):
    ds = ds_local

    assert ds['x'].values.tolist() == ds.evaluate('x').tolist()
    assert ds['name'].tolist() == ds.evaluate('name', array_type='arrow').to_pylist()
    if 'obj' in ds:   # df_arrow does not have it
        assert ds['obj'].tolist() == ds.evaluate('obj').tolist()
    assert ds[['x', 'y']].values.tolist() == np.array([ds.evaluate('x'), ds.evaluate('y')]).T.tolist()
    assert ds[['x', 'y']].values.shape == (len(ds), 2)
    if '__x' in ds.column_names:  # this is the case for arrow, ar.filter does not copy the original masked out data
        assert ds[['m']].values[9][0] == 0.0
        assert ds[['m','x']].values[9][0] == 0
    else:
        assert ds[['m']].values[9][0] == 77777.0
        assert ds[['m','x']].values[9][0] == 77777
    # The missing values are included. This may not be the correct behaviour
    assert ds[['x', 'y', 'nm']].values.tolist(), np.array([ds.evaluate('x'), ds.evaluate('y'), ds.evaluate('nm')]).T.tolist()

@pytest.mark.skip(reason='TOFIX: obj is now recognized as str')
def test_object_column_values(ds_local):
    ds = ds_local
    with pytest.raises(ValueError):
        ds[['x', 'name', 'nm', 'obj']].values
