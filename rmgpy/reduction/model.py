#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################
#
#   RMG - Reaction Mechanism Generator
#
#   Copyright (c) 2002-2010 Prof. William H. Green (whgreen@mit.edu) and the
#   RMG Team (rmg_dev@mit.edu)
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the 'Software'),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#
################################################################################

from collections import Counter

class ReductionReaction(object):
    """
    A class that enhances RMG-Py's  Reaction object
    by providing storage for the forward (kf) and backward
    (kb) rate coefficient.

    Once k is computed, it is stored and fetched
    when requested.

    """
    def __init__(self, rmg_reaction):
        super(ReductionReaction, self).__init__()
        self.rmg_reaction = rmg_reaction
        self.reactants = rmg_reaction.reactants
        self.products = rmg_reaction.products
        self.kf = None
        self.kb = None
        self.stoichio = {}
        self.create_stoichio()
    
    def __str__(self):
        return str(self.rmg_reaction)

    def __reduce__(self):
        """
        A helper function used when pickling an object.
        """
        return (self.__class__, (self.rmg_reaction, ))


    def getRateCoefficient(self, T,P):
        if self.kf is None:
            self.kf = self.rmg_reaction.getRateCoefficient(T,P)
            return self.kf
        else: return self.kf
    
    def getReverseRateCoefficient(self, T, P):
        if self.kb is None:
            kf = self.getRateCoefficient(T,P) 
            self.kb = kf / self.rmg_reaction.getEquilibriumConstant(T)
            return self.kb
        else: return self.kb
    
    def create_stoichio(self):
        c_reactants = Counter([mol.label for mol in self.reactants])
        self.stoichio['reactant'] = c_reactants

        c_products = Counter([mol.label for mol in self.products])
        self.stoichio['product'] = c_products

    def get_stoichiometric_coefficient(self, spc_i, reactant_or_product):       
        return self.stoichio[reactant_or_product][spc_i.label]