from common import *

def test_state_get_set(ds_local):
    ds = ds_local

    ds_copy = ds.copy()

    ds['v'] = ds.x + 1

    state = ds.state_get()
    ds_copy.state_set(state)
    assert ds_copy.v.values.tolist() == ds.v.values.tolist()
    
    # making a copy when the state is set should work as well
    assert ds_copy.copy().v.values.tolist() == ds.v.values.tolist()
    assert 'v' in ds_copy.get_column_names()

def test_state_variables(df_local_non_arrow, tmpdir):
    filename = str(tmpdir.join('state.json'))
    df = df_local_non_arrow
    df_copy = df.copy()
    t_test = np.datetime64('2005-01-01')
    df.add_variable('dt_var', t_test)
    variables = df.variables.copy()

    # this virtual column will add a variable (the timedelta)
    df['seconds'] = df.timedelta / np.timedelta64(1, 's')
    assert len(df.variables) == len(variables) + 1
    var_name = list(set(df.variables) - set(variables))[0]

    df.state_write(filename)

    df_copy.state_load(filename)
    assert isinstance(df_copy.variables[var_name], np.timedelta64)
    assert df.seconds.tolist() == df_copy.seconds.tolist()
    assert df_copy.variables['dt_var'] == t_test
