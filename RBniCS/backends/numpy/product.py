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
## @file product.py
#  @brief product function to assemble truth/reduced affine expansions.
#
#  @author Francesco Ballarin <francesco.ballarin@sissa.it>
#  @author Gianluigi Rozza    <gianluigi.rozza@sissa.it>
#  @author Alberto   Sartori  <alberto.sartori@sissa.it>

from RBniCS.backends.numpy.affine_expansion_storage import AffineExpansionStorage
from RBniCS.backends.numpy.matrix import Matrix
from RBniCS.backends.numpy.vector import Vector
from RBniCS.backends.numpy.function import Function
from RBniCS.utils.decorators import backend_for, ThetaType

# product function to assemble truth/reduced affine expansions. To be used in combination with sum,
# even though this one actually carries out both the sum and the product!
@backend_for("NumPy", inputs=(ThetaType, AffineExpansionStorage, ThetaType + (None,)))
def product(thetas, operators, thetas2=None):
    order = operators.order()
    first_operator = None
    assert order in (1, 2)
    if order == 1: # vector storage of affine expansion online data structures (e.g. reduced matrix/vector expansions)
        first_operator = operators[0]
        assert isinstance(first_operator, (Matrix.Type(), Vector.Type(), Function.Type()))
        assert thetas2 is None
        assert len(thetas) == len(operators)
        # Single for loop version:
        output = 0
        for (theta, operator) in zip(thetas, operators):
            output += theta*operator
        '''
        # Vectorized version:
        # Profiling has reveleaded that the following vectorized (over q) version
        # introduces an overhead of 10%~20%
        from numpy import asmatrix
        output = asmatrix(thetas)*operators.as_matrix().transpose()
        assert output.shape == (1, 1)
        output = output.item(0, 0)
        '''
    elif order == 2: # matrix storage of affine expansion online data structures (e.g. error estimation ff/af/aa products)
        first_operator = operators[0, 0]
        assert isinstance(first_operator, (Matrix.Type(), Vector.Type(), float))
        assert thetas2 is not None
        # no checks here on the first dimension of operators should be equal to len(thetas), and
        # similarly that the second dimension should be equal to len(thetas2), because the
        # current operator interface does not provide a 2D len method
        '''
        # Double for loop version:
        # Profiling has revelead a sensible speedup for large values of N and Q 
        # when compared to the double/triple/quadruple for loop in the legacy version.
        # Vectorized version (below) provides an additional 25%~50% speedup when dealing with
        # the (A, A) Riesz representor products (case of quadruple loop),
        # while this version introduces overhead when for (F, F) Riesz 
        # representor products (case of double loop).
        output = 0.
        for i in range(len(thetas)):
            for j in range(len(thetas2)):
                output += thetas[i]*operators[i, j]*thetas2[j]
        # Thus we selected the following:
        '''
        # Vectorized version:
        from numpy import asmatrix
        thetas_vector = asmatrix(thetas)
        thetas2_vector = asmatrix(thetas2).transpose()
        output = thetas_vector*operators.as_matrix()*thetas2_vector
        assert output.shape == (1, 1)
        output = output.item(0, 0)
    else:
        raise AssertionError("product(): invalid operands.")
    
    # Store N (and M) in the output, since it is not preserved by sum operators
    if isinstance(first_operator, Matrix.Type()):
        output.M = first_operator.M
        output.N = first_operator.N
    elif isinstance(first_operator, Vector.Type()):
        output.N = first_operator.N
    elif isinstance(first_operator, float):
        pass # nothing to be done
    elif isinstance(first_operator, Function.Type()):
        raise NotImplementedError("product(): the case of Function operand has not been implemented yet.")
    else:
        raise AssertionError("product(): invalid operands.")
    # Store dicts also in the product output
    assert (operators._basis_component_index_to_component_name is None) == (operators._component_name_to_basis_component_index is None)
    assert (operators._component_name_to_basis_component_index is None) == (operators._component_name_to_basis_component_length is None)
    if operators._basis_component_index_to_component_name is not None:
        output._basis_component_index_to_component_name = operators._basis_component_index_to_component_name
        output._component_name_to_basis_component_index = operators._component_name_to_basis_component_index
        output._component_name_to_basis_component_length = operators._component_name_to_basis_component_length
    # Return
    return ProductOutput(output)
    
        
# Auxiliary class to signal to the sum() function that it is dealing with an output of the product() method
class ProductOutput(object):
    def __init__(self, sum_product_return_value):
        self.sum_product_return_value = sum_product_return_value
    
