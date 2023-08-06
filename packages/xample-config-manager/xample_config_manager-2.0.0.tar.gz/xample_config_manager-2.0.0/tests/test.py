# -*- coding: utf-8 -*-
"""
© 2012 - 2016 Xample Sàrl

Author: Stephane Poss
Date: 18.07.16
"""
import os
import tempfile
import unittest
import json

from config_manager.utils import set_config, get_config, set_settings, get_secret


class TestConfig(unittest.TestCase):
    def setUp(self):
        fd, self.config = tempfile.mkstemp()
        cfg = {"SOME_OPTION": "SOME_VALUE"}
        with open(self.config, "w") as cfg_f:
            cfg_f.write(json.dumps(cfg))

        fd, self.settings = tempfile.mkstemp()
        cfg = {"SOME_OPTION": "SOME_VALUE"}
        with open(self.settings, "w") as cfg_f:
            cfg_f.write(json.dumps(cfg))

    def test_get_config(self):
        set_config(self.config)
        res = get_config("SOME_OPTION", None)
        self.assertEqual(res, "SOME_VALUE")

    def test_get_secret(self):
        set_settings(self.settings)
        res = get_secret("SOME_OPTION")
        self.assertEqual(res, "SOME_VALUE")

    def tearDown(self):
        os.unlink(self.config)
        os.unlink(self.settings)


class TestSetup(unittest.TestCase):
    def setUp(self):
        fd, self.settings = tempfile.mkstemp()
        cfg = {"SOME_OPTION": "SOME_VALUE"}
        with open(self.settings, "w") as cfg_f:
            cfg_f.write(json.dumps(cfg))
        set_settings(self.settings)

    def test_get_secret(self):
        res = get_secret("SOME_OPTION")
        self.assertEqual(res, "SOME_VALUE")

    def tearDown(self):
        os.unlink(self.settings)
