import sys
from unittest import mock

sys.modules['app.server'] = mock.Mock()
sys.modules['app.model'] = mock.Mock()
