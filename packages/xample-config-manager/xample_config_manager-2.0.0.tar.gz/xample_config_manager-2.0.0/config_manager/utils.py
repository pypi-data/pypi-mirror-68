# -*- coding: utf-8 -*-
"""
Xample SARL

Author: stephane
Date: 06.04.16
"""

import json
import os

from config_manager.exceptions import SettingsMissing, BadSetting, ConfigMissing, BadConfig

settings_path = os.environ.get("SECRETS_FILE", "")
dj_secrets = {}


def set_settings(path=None):
    """
    Configure the settings
    :param path: a path to the setting
    :return: None
    """
    global settings_path
    global dj_secrets
    if path:
        settings_path = path
    if not settings_path:
        settings_path = os.path.expanduser("~/settings.json")

    if not os.path.exists(settings_path):
        raise SettingsMissing("Settings file not found at %s!" % settings_path)

    with open(settings_path) as f:
        try:
            dj_secrets = json.loads(f.read())
        except Exception as err:
            raise SettingsMissing("Settings file is corrupted")


def get_secret(setting, secrets=None):
    """
    Get a secret from the configuration
    """
    global dj_secrets
    if secrets is None:
        secrets = dj_secrets
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Missing key %s in settings" % setting
        raise BadSetting(error_msg)

myconfig = {}
config_path = os.environ.get("CONFIG_PATH", "")


def set_config(path=None):
    """
    Configure the config.json path
    :param path: the path to the config.json of this project
    :return: None
    """
    global config_path
    global myconfig

    if path:
        config_path = path

    if not config_path:
        config_path = os.path.expanduser("~/config.json")

    if not os.path.exists(config_path):
        raise ConfigMissing("Configuration file not found at %s" % config_path)

    with open(config_path) as f:
        try:
            myconfig = json.loads(f.read())
        except Exception as err:
            raise ConfigMissing("Configuration file is corrupted")


def get_config(setting, default=None, config=None):
    """
    Get some installation configuration parameters
    :param string setting: the setting key one wants to access
    :param object default: a default value in case it's not found
    :param dict config: a config dict
    :return: the value for the setting
    """
    global myconfig
    if not config:
        config = myconfig
    try:
        return config[setting]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "Missing key %s in local configuration" % setting
            raise BadConfig(error_msg)
