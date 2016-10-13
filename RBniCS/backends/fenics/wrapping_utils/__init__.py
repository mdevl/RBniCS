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
## @file __init__.py
#  @brief Init file for auxiliary linear algebra module
#
#  @author Francesco Ballarin <francesco.ballarin@sissa.it>
#  @author Gianluigi Rozza    <gianluigi.rozza@sissa.it>
#  @author Alberto   Sartori  <alberto.sartori@sissa.it>

from RBniCS.backends.fenics.wrapping_utils.create_submesh import create_submesh, create_submesh_subdomains, mesh_dofs_to_submesh_dofs, submesh_dofs_to_mesh_dofs
from RBniCS.backends.fenics.wrapping_utils.dirichlet_bc import DirichletBC
from RBniCS.backends.fenics.wrapping_utils.dofs_parallel_io_helpers import build_dof_map_writer_mapping, build_dof_map_reader_mapping
from RBniCS.backends.fenics.wrapping_utils.get_form_name import get_form_name
from RBniCS.backends.fenics.wrapping_utils.get_form_argument import get_form_argument
from RBniCS.backends.fenics.wrapping_utils.parametrized_expression import ParametrizedExpression

__all__ = [
    'build_dof_map_reader_mapping',
    'build_dof_map_writer_mapping',
    'create_submesh',
    'create_submesh_subdomains',
    'DirichletBC',
    'get_form_name',
    'get_form_argument',
    'mesh_dofs_to_submesh_dofs',
    'ParametrizedExpression',
    'submesh_dofs_to_mesh_dofs'
]