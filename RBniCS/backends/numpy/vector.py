# Copyright (C) 2015-2016 by the RBniCS authors
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
## @file online_vector.py
#  @brief Type of online vector
#
#  @author Francesco Ballarin <francesco.ballarin@sissa.it>
#  @author Gianluigi Rozza    <gianluigi.rozza@sissa.it>
#  @author Alberto   Sartori  <alberto.sartori@sissa.it>

from numpy import matrix

class _Vector_Type(matrix): # inherit to make sure that matrices and vectors correspond to two different types
    pass

from numpy import zeros as _VectorContent_Base
from RBniCS.utils.decorators import backend_for

@backend_for("NumPy", inputs=(int, ))
def Vector(N):
    return _Vector_Type(_VectorContent_Base((N))).transpose() # as column vector

Vector.Type = _Vector_Type