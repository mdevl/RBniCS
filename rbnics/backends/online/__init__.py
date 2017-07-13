# Copyright (C) 2015-2017 by the RBniCS authors
#
# This file is part of RBniCS.
#
# RBniCS is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RBniCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RBniCS. If not, see <http://www.gnu.org/licenses/>.
#

import importlib
import sys
current_module = sys.modules[__name__]

# Get the online backend name
from rbnics.utils.config import config
online_backend = config.get("backends", "online backend")

# Import it
importlib.import_module("rbnics.backends.online." + online_backend)
importlib.import_module("rbnics.backends.online." + online_backend + ".wrapping")

# As set it as online backend in the factory
from rbnics.utils.factories import enable_backend, online_backend_factory, set_online_backend
enable_backend(online_backend)
set_online_backend(online_backend)
online_backend_factory(current_module)

# Clean up
del current_module
del online_backend
