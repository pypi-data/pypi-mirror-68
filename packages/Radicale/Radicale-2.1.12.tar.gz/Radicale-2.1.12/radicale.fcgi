#!/usr/bin/env python3
#
# This file is part of Radicale Server - Calendar Server
# Copyright © 2011-2017 Guillaume Ayoub
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Radicale.  If not, see <http://www.gnu.org/licenses/>.

"""
Radicale FastCGI Example.

Launch a Radicale FastCGI server according to configuration.

This script relies on flup but can be easily adapted to use another
WSGI-to-FastCGI mapper.

"""

from flup.server.fcgi import WSGIServer
from radicale import application


WSGIServer(application).run()
