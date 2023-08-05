# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test example app."""

import json
import os
import signal
import subprocess
import time
from os.path import abspath, dirname, join

import pytest


@pytest.yield_fixture
def example_app():
    """Example app fixture."""
    current_dir = os.getcwd()

    # Go to example directory
    project_dir = dirname(dirname(abspath(__file__)))
    exampleapp_dir = join(project_dir, 'examples')
    os.chdir(exampleapp_dir)

    # Setup application
    assert subprocess.call('./app-setup.sh', shell=True) == 0

    # Setup fixtures
    assert subprocess.call('./app-fixtures.sh', shell=True) == 0

    # Start example app
    webapp = subprocess.Popen(
        'FLASK_APP=app.py FLASK_DEBUG=1 flask run',
        stdout=subprocess.PIPE, preexec_fn=os.setsid, shell=True)
    time.sleep(3)
    yield webapp

    # Stop server
    os.killpg(webapp.pid, signal.SIGTERM)

    # Tear down example app
    subprocess.call('./app-teardown.sh', shell=True)

    # Return to the original directory
    os.chdir(current_dir)


def test_example_app(example_app):
    """Test example app."""
    cmd = 'curl http://0.0.0.0:5000/records/?q=title:Test'
    output = json.loads(
        subprocess.check_output(cmd, shell=True).decode('utf-8'))
    assert output == {'title': 'Test'}
    cmd = ('curl http://0.0.0.0:5000/records/?q=title:Test '
           '-H Accept:application/xml')
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')
    expected = ("""<?xml version="1.0" encoding="utf-8"?>\n"""
                """<title>Test</title>""")
    assert output == expected
