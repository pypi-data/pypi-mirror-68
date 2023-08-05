import os
import mxdevtool as mx
import numpy as np
from datetime import datetime
import tempfile

def npzee_view(arg):
    if isinstance(arg, np.ndarray):
        tempfile = os.path.join(tempfile.gettempdir(), 'temp_' + datetime.utcnow().strftime('%Y%m%d%H%M%S%f') + '.npz')
        np.savez(tempfile, data=arg)
        os.startfile(tempfile)
    elif isinstance(arg, str):
        if os.path.exists(arg):
            os.startfile(arg)
        else:
            raise Exception('file does not exist')
    elif isinstance(arg, mx.ScenarioResultReader):
        filename = arg.filename()
        if os.path.exists(filename):
            os.startfile(filename)
        else:
            raise Exception('file does not exist')
    else:
        print('unknown')
