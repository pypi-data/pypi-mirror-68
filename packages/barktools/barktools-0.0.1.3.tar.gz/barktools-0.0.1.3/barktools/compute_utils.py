#import numpy as np
import pandas as pd

class MultiBaseNumber:
    """ Class representing a 'multi-base number', i.e. a number whose digits stem from different bases

        E.g. number 1020 with multi-base [2,2,3,4] would be equal to 32

        Parameters
        ---------------
        bases : sequence
            Ordered collection of bases.
            bases[0] is the leftmost base
        digits : sequence
            Digits of the number
            digits[0] is the leftmost digit
    """

    def __init__(self, bases, digits=None):
        if self.__check_bases(bases):
            self.bases = bases
        else:
            raise ArithmeticError('Provided bases are not eligible')

        if digits is None:
            self.digits = [0]*len(self.bases)
        else:
            if self.__check_digits(digits):
                self.digits = digits
            else:
                raise ArithmeticError('Provided digits not compatible with specified bases')

    def __check_bases(self, bases):
        return all([base > 0 for base in bases])

    def __check_digits(self, digits):
        """ Checks if 'digits' is compatible with 'bases'

            Parameters
            ---------------
            digits : sequence 
                Digits of the number

            Returns : bool
                True of digits are compatible with bases, False otherwise
        """
        if len(digits) != len(self.bases): return False
        return all([digits[i] < self.bases[i] for i in range(len(digits))])

    def __eq__(self, other):
        return self.base_10() == other.base_10()

    def __ne__(self, other):
        return self.base_10() != other.base_10()

    def __lt__(self, other):
        return self.base_10() < other.base_10()

    def __gt__(self, other):
        return self.base_10() > other.base_10()

    def __le__(self, other):
        return self.base_10() <= other.base_10()

    def __ge__(self, other):
        return self.base_10() >= other.base_10()

    def base_10(self):
        """ Return the base 10 value of the MultiBaseNumber

            Returns : int
        """
        n, b = 0, 1
        for i in reversed(range(len(self.digits))):
            n = n + b*self.digits[i]
            b = b*self.bases[i]
        return n

class MinusInf:
    def __eq__(self, other):
        return False
    def __ne__(self, other):
        return True
    def __lt__(self, other):
        return True
    def __gt__(self, other):
        return False
    def __le__(self, other):
        return True
    def __ge__(self, other):
        return False
    def __str__(self):
        return '-inf'

class PlusInf():
    def __eq__(self, other):
        return False
    def __ne__(self, other):
        return True
    def __lt__(self, other):
        return False
    def __gt__(self, other):
        return True
    def __le__(self, other):
        return False
    def __ge__(self, other):
        return True
    def __str__(self):
        return '+inf'

def get_brackets(df, col, bracket_edges):
    brackets = pd.Series(np.nan, index=df.index)
    n_brackets = len(bracket_edges)+1
    for iBracket in range(n_brackets):
        lower = bracket_edges[iBracket-1] if (iBracket > 0) else MinusInf()
        upper = bracket_edges[iBracket] if (iBracket < n_brackets-1) else PlusInf()
        brackets.loc[(lower<df[col]) & (df[col]<upper)] = iBracket
    return brackets

#TODO: Enable include_beyond functionality
def conditional_group_by(df, col, bracket_edges, include_beyond='both'):
    ''' Returns a groupby object for df where rows with col in bins defined by bracket_edges grouped together
    
        Parameters
        ------------
        col : str
            The single column for which to produce brackets w.r.t
        bracket_edges : list
            Ordered values (ascending) defining the bracket edges of the column specified by col
        include_beyond : {'none', 'left', 'right', 'both'}
            'left' => samples with col value < bracket_edges[0] will be included
            'right' => samples with col value > bracket_edges[-1] will be included
            'both' => both 'left' and 'right'
    '''
    brackets = get_brackets(df, col, bracket_edges, include_beyond=include_beyond)    
    return df.groupby(brackets)