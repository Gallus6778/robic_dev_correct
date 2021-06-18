#!/usr/bin/python

from wsgiref.handlers import CGIHandler
# from yourapplication import app

import app
CGIHandler().run(app)