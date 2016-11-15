from .general import *
import lasso.utils as _utils

if _utils.run_from_ipython():
    from IPython.core.getipython import get_ipython
    get_ipython().set_custom_exc((BaseException,), _utils.ipython_except_hook)
