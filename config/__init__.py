import sys
import os

if 'unittest' in sys.modules.keys():
    from .test_config import *

if os.getenv('FLASK_ENVIRONMENT') == 'development':
    from .dev_config import *
