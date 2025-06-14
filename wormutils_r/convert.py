import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    import rpy2.robjects as ro

from rpy2.robjects import pandas2ri
import numpy


def rpy2float(v):
    """
    Certain kinds of float can't be read by rpy2 (e.g. numpy.float64).
    This function converts non-base floats into base float to be accepted by rpy2.
    """
    
    if isinstance(v, list):
        v = [rpy2float(vi) for vi in v]
    
    if isinstance(v, dict):
        v = {k:rpy2float(vi) for k,vi in zip(v.keys(), v.values())}
    
    if isinstance(v, numpy.float64):
        v = float(v)
        
    return v


def pd_to_r_df(pandas_df):
    """
    Convert a pandas df to an R df
    """
    with (ro.default_converter + pandas2ri.converter).context():
        r_df = ro.conversion.get_conversion().py2rpy(pandas_df)
    return r_df


def r_df_to_pd(r_df):
    """
    Convert an R df to a pandas df
    """
    with (ro.default_converter + ro.pandas2ri.converter).context():
        pandas_df = ro.conversion.get_conversion().rpy2py(r_df)
    return pandas_df


def convert_to_RVector(value, force_Rvec=True):
    
    """
    Convert a value or list into an R vector of the appropriate type.
    
    Parameters
    ----------
    value : numeric or str, or list of numeric or str
        Value to be converted.
    
    force_Rvec : bool, default True
        If `value` is not a list, force conversion into a R vector?
        False will return an int, float, or str if value is non-list.
        True will always return an R vector.
    
    Returns
    -------
    int, float, str, or an rpy2 R vector
        A value or R vector of an appropriate data type.
    """

    if not isinstance(value, list) and not force_Rvec:
        return value
    elif not isinstance(value, list) and force_Rvec:
        value = [value]
    else:
        pass

    if all(isinstance(x, bool) for x in value):
        return ro.BoolVector(value)
    elif all(isinstance(x, int) for x in value):
        return ro.IntVector(value)
    elif all(isinstance(x, float) or isinstance(x, int) for x in value):
        return ro.FloatVector(value)
    else:
        return ro.StrVector([str(v) for v in value])