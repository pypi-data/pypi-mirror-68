#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for artellapipe-dccs-maya
"""

import os
import inspect
import logging.config


def init(do_reload=False, dev=False):
    """
    Initializes module
    """

    logging.config.fileConfig(get_logging_config(), disable_existing_loggers=False)

    from tpDcc.libs.python import importer

    class ArtellaMayaDcc(importer.Importer, object):
        def __init__(self, debug=False):
            super(ArtellaMayaDcc, self).__init__(module_name='artellapipe.dccs.maya', debug=debug)

        def get_module_path(self):
            """
            Returns path where tpNameIt module is stored
            :return: str
            """

            try:
                mod_dir = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
            except Exception:
                try:
                    mod_dir = os.path.dirname(__file__)
                except Exception:
                    return None

            return mod_dir

    packages_order = []

    artella_maya_lib = importer.init_importer(importer_class=ArtellaMayaDcc, do_reload=False, debug=dev)
    artella_maya_lib.import_packages(order=packages_order, only_packages=False)
    if do_reload:
        artella_maya_lib.reload_all()

    create_logger_directory()


def create_logger_directory():
    """
    Creates artellapipe-gui logger directory
    """

    artellapipe_logger_dir = os.path.normpath(os.path.join(os.path.expanduser('~'), 'artellapipe', 'logs'))
    if not os.path.isdir(artellapipe_logger_dir):
        os.makedirs(artellapipe_logger_dir)


def get_logging_config():
    """
    Returns logging configuration file path
    :return: str
    """

    create_logger_directory()

    return os.path.normpath(os.path.join(os.path.dirname(__file__), '__logging__.ini'))


def get_logging_level():
    """
    Returns logging level to use
    :return: str
    """

    if os.environ.get('ARTELLAPIPE_LIBS_MAYA_LOG_LEVEL', None):
        return os.environ.get('ARTELLAPIPE_LIBS_MAYA_LOG_LEVEL')

    return os.environ.get('ARTELLAPIPE_LIBS_MAYA_LOG_LEVEL', 'WARNING')
