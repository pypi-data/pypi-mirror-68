# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Minimal Flask application example for development.

SPHINX-START

First install Invenio-UserProfiles, setup the application and load fixture data
by running:

.. code-block:: console

   $ pip install -e .[all]
   $ cd examples
   $ ./app-setup.sh
   $ ./app-fixtures.sh

You should also have the `Redis` running on your machine. To know how
to install and run `redis`, please refer to the
`redis website <https://redis.io/>`_.

Next, start the development server:

.. code-block:: console

   $ export FLASK_APP=app.py FLASK_DEBUG=1
   $ flask run

and open the example application in your browser:

.. code-block:: console

    $ open http://127.0.0.1:5000/

Choose a user to login:

    - user info@inveniosoftware.org password 123456
    - user another@inveniosoftware.org password 123456

You can check the administration page opening the page:

    $ open http://127.0.0.1:5000/admin

Note that, as defined in our fixtures, only `info@inveniosoftware.org` user
can enter.

To uninstall and purge the example app, run:

.. code-block:: console

    $ ./app-teardown.sh

SPHINX-END
"""

from __future__ import absolute_import, print_function

import os

import pkg_resources
from flask import Flask, redirect, url_for
from flask_babelex import Babel
from invenio_access import InvenioAccess
from invenio_accounts import InvenioAccounts
from invenio_accounts.views import blueprint
from invenio_admin import InvenioAdmin
from invenio_admin.views import blueprint as blueprint_admin_ui
from invenio_db import InvenioDB
from invenio_i18n import InvenioI18N
from invenio_mail import InvenioMail
from wtforms.i18n import messages_path

from invenio_userprofiles import InvenioUserProfiles
from invenio_userprofiles.views import blueprint as blueprint2
from invenio_userprofiles.views import blueprint_api_init, blueprint_ui_init

try:
    pkg_resources.get_distribution('invenio_assets')
    from invenio_assets import InvenioAssets
    INVENIO_ASSETS_AVAILABLE = True
except pkg_resources.DistributionNotFound:
    INVENIO_ASSETS_AVAILABLE = False

try:
    pkg_resources.get_distribution('invenio_theme')
    from invenio_theme import InvenioTheme
    INVENIO_THEME_AVAILABLE = True
except pkg_resources.DistributionNotFound:
    INVENIO_THEME_AVAILABLE = False


# Create Flask application
app = Flask(__name__)
app.config.update(
    ACCOUNTS_USE_CELERY=False,
    BABEL_DEFAULT_LOCALE='en',
    I18N_TRASNLATION_PATHS=[messages_path()],
    MAIL_SUPPRESS_SEND=True,
    SECRET_KEY='CHANGE_ME',
    SQLALCHEMY_DATABASE_URI=os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db'
    ),
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    WTF_CSRF_ENABLED=False,
)
Babel(app)
InvenioMail(app)
InvenioI18N(app)
InvenioDB(app)
if INVENIO_ASSETS_AVAILABLE:
    InvenioAssets(app)
if INVENIO_THEME_AVAILABLE:
    InvenioTheme(app)
InvenioAccess(app)
InvenioAccounts(app)
app.register_blueprint(blueprint)
InvenioUserProfiles(app)
app.register_blueprint(blueprint2)
app.register_blueprint(blueprint_api_init)
app.register_blueprint(blueprint_ui_init)

InvenioAdmin(app)
app.register_blueprint(blueprint_admin_ui)


@app.route('/')
def index():
    """Example index page route."""
    return redirect(url_for('invenio_userprofiles.profile'))
