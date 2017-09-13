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

from numbers import Number
import types
from dolfin import Expression
from rbnics.backends.dolfin.wrapping.parametrized_constant import is_parametrized_constant, parametrized_constant_to_float

# This ideally should be a subclass of Expression. However, dolfin manual
# states that subclassing Expression may be significantly slower than using 
# JIT-compiled expressions. To this end we avoid subclassing expression and
# just add the set_mu method using the types library
def ParametrizedExpression(truth_problem, parametrized_expression_code=None, *args, **kwargs):    
    if parametrized_expression_code is None:
        return None
    
    assert "mu" in kwargs
    mu = kwargs["mu"]
    assert mu is not None
    assert isinstance(mu, tuple)
    P = len(mu)
    for p in range(P):
        assert isinstance(parametrized_expression_code, (tuple, str))
        if isinstance(parametrized_expression_code, tuple):
            if isinstance(parametrized_expression_code[0], tuple):
                matrix_after_replacements = list()
                for row in parametrized_expression_code:
                    assert isinstance(row, tuple)
                    new_row = list()
                    for item in row:
                        assert isinstance(item, str)
                        new_row.append(item.replace("mu[" + str(p) + "]", "mu_" + str(p)))
                    new_row = tuple(new_row)
                    matrix_after_replacements.append(new_row)
                parametrized_expression_code = tuple(matrix_after_replacements)
            else:
                vector_after_replacements = list()
                for item in parametrized_expression_code:
                    assert isinstance(item, str)
                    vector_after_replacements.append(item.replace("mu[" + str(p) + "]", "mu_" + str(p)))
                parametrized_expression_code = tuple(vector_after_replacements)
        elif isinstance(parametrized_expression_code, str):
            parametrized_expression_code = parametrized_expression_code.replace("mu[" + str(p) + "]", "mu_" + str(p))
        else:
            raise AssertionError("Invalid expression type in ParametrizedExpression")
    
    # Detect mesh
    if "domain" in kwargs:
        mesh = kwargs["domain"]
    else:
        mesh = truth_problem.V.mesh()
    
    # Prepare a dictionary of mu
    mu_dict = {}
    for (p, mu_p) in enumerate(mu):
        assert isinstance(mu_p, (Expression, Number))
        if isinstance(mu_p, Number):
            mu_dict[ "mu_" + str(p) ] = mu_p
        elif isinstance(mu_p, Expression):
            assert is_parametrized_constant(mu_p)
            mu_dict[ "mu_" + str(p) ] = parametrized_constant_to_float(mu_p, point=mesh.coordinates()[0])
    del kwargs["mu"]
    kwargs.update(mu_dict)
    
    # Initialize expression
    expression = Expression(parametrized_expression_code, *args, **kwargs)
    expression.mu = mu # to avoid repeated assignments
    
    # Store ufl_domain
    expression._mesh = mesh
    def ufl_domain(self):
        return expression._mesh.ufl_domain()
    expression.ufl_domain = types.MethodType(ufl_domain, expression)
    
    # Keep mu in sync
    standard_set_mu = truth_problem.set_mu
    def overridden_set_mu(self, mu):
        standard_set_mu(mu)
        if expression.mu is not mu:
            assert isinstance(mu, tuple)
            assert len(mu) == len(expression.mu)
            for (p, mu_p) in enumerate(mu):
                setattr(expression, "mu_" + str(p), mu_p)
            expression.mu = mu
    truth_problem.set_mu = types.MethodType(overridden_set_mu, truth_problem)
    # Note that this override is different from the one that we use in decorated problems,
    # since (1) we do not want to define a new child class, (2) we have to execute some preprocessing
    # on the data, (3) it is a one-way propagation rather than a sync. 
    # For these reasons, the decorator @sync_setters is not used but we partially duplicate some code
    
    # Possibly also keep time in sync
    if hasattr(truth_problem, "set_time"):
        standard_set_time = truth_problem.set_time
        def overridden_set_time(self, t):
            standard_set_time(t)
            if hasattr(expression, "t"):
                if expression.t is not t:
                    expression.t = t
        truth_problem.set_time = types.MethodType(overridden_set_time, truth_problem)
    
    return expression

