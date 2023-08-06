import pytest
import shutil
import requests
from pathlib import Path

import zwutils.network as NET

class TestNetwork:
    def test_get_html(self):
        r = NET.get_html('http://www.baidu.com')
        assert r.startswith('<!DOCTYPE html><!--STATUS OK--><html>')
