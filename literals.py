################################
# Local dependencies
################################
from nums_func import num_to_str

################################
# External imports
################################
from copy import copy

# =========================Constants=========================
MON_DICT = {"": 1}


def make_pol(number):
    return Pol([Mon(number)])


################################
# Exceptions
################################
class NonSimMonError(Exception):
    """Exception raised when trying to add or subtract two non-similar monomial"""
    pass


class ImpossibleDivError(Exception):
    """Exception raised when dividing two monomials and one of the exponents becomes negative"""
    pass


class NonIntPowError(Exception):
    """Exception raised when trying to make a non-integer power on a monomial"""
    pass


class NonIntRootError(Exception):
    """Exception raised when trying to calculate a negative root or that contains letters"""
    pass


################################
# Monomials
################################
class Mon:
    """Defines monomials and how they operate.
    The dunder methods defined are:
    __init__, __str__, __repr__, __add__, __sub__, __truediv__, __floordiv__, __mul__, __pow__, __eq__, __abs__, __neg__

    The custom methods are:
    is_similar(self, other) -> returns True if self.lt == other.lt
    is_opposite(self, other) -> returns True if self + other == Mon(0)
    grade(self) -> returns the sum of the exponents of the monomial
    """

    # =========================Custom methods=========================
    def is_similar(self, other) -> bool:
        return self.lt == other.lt

    def is_opposite(self, other) -> bool:
        return self + other == Mon(0)

    def grade(self) -> int:
        grade = 0
        for letter in self.lt:
            if letter != "": grade += self.lt[letter]

        return grade

    # =========================Dunder methods=========================
    def __init__(self, number: float, letters: dict = None):
        if letters is None: letters = MON_DICT

        self.num = number
        self.lt = letters

    def __str__(self):
        if self.num == 1:
            temp_str = ""

        elif self.num == -1:
            temp_str = "-"

        elif self.lt[""] != make_pol(1) and self.lt[""] != 1:
            temp_str = f"{num_to_str(self.num)}"

            if len(str(self.lt[""])) > 1:
                try:
                    int(str(self.lt[""]))
                    temp_str += f"^{self.lt['']}"

                except ValueError:
                    temp_str += f"^({self.lt['']})"

            else:
                temp_str += f"^{self.lt['']}"

        else:
            temp_str = num_to_str(self.num)

        in_order_letters = list(self.lt)
        in_order_letters.sort()

        for letter in in_order_letters:
            if letter == "":
                continue

            if self.lt[letter] != make_pol(0) and self.lt[letter] != 0:
                temp_str += letter

            if self.lt[letter] != make_pol(1) and self.lt[letter] != 1:
                if len(str(self.lt[letter])) > 1:
                    try:
                        int(str(self.lt[""]))
                        temp_str += f"^{self.lt[letter]}"

                    except ValueError:
                        temp_str += f"^({self.lt[letter]})"

                else:
                    temp_str += f"^{self.lt[letter]}"

        if temp_str == "": temp_str = "1"
        elif temp_str == "-": temp_str = "-1"

        return temp_str

    def __repr__(self):
        return f"Mon({self.num}, {self.lt})"

    def __add__(self, other):
        if not self.is_similar(other):
            raise NonSimMonError

        total = self.num + other.num

        return Mon(total, self.lt if total != 0 else MON_DICT)

    def __sub__(self, other):
        if self.lt != other.lt:
            raise NonSimMonError

        sub = self.num - other.num
        return Mon(sub, self.lt if sub != 0 else MON_DICT)

    def __truediv__(self, other):
        new_lt = MON_DICT

        if type(other) is Mon:
            for key in other.lt:
                try:
                    if key not in self.lt or other.lt[key] > self.lt[key]:
                        raise ImpossibleDivError
                except KeyError:
                    raise ImpossibleDivError

            for key in other.lt:
                if key == "": continue

                new_lt[key] = self.lt[key] - other.lt[key]
                if new_lt[key] == 0:
                    del new_lt[key]

            return Mon(self.num / other.num, new_lt)

        else: return Mon(self.num / other, self.lt)

    def __mul__(self, other):
        new_lt = self.lt.copy()

        for key in other.lt:
            if key != "":
                try:
                    new_lt[key] += other.lt[key]

                except KeyError:
                    new_lt[key] = other.lt[key]

        return Mon(self.num * other.num, new_lt)

    def __pow__(self, power, modulo=None):

        if type(power) is not Pol:
            return NonIntPowError

        elif len(power) == 1 and str(power.first_mon()).isdigit():
            pow_num = power.first_mon().num
            new_lt = self.lt.copy()

            for letter in new_lt:
                if letter != "":
                    new_lt[letter] *= pow_num

            return Mon(self.num ** pow_num, new_lt)

        else:
            new_lt = self.lt.copy()

            for letter in new_lt:
                new_lt[letter] *= power

            return Mon(self.num, new_lt)

    def __eq__(self, other):
        if type(other) is Mon:
            return self.num == other.num and self.lt == other.lt

        elif (type(other) is (float or int)) and self.lt == MON_DICT:
            return self.num == other

        else: return False

    def __abs__(self):
        return Mon(abs(self.num), self.lt)

    def __neg__(self):
        return Mon(-self.num, self.lt)

################################
# Polynomials
################################
class Pol:
    """Defines how polynomials operate.
    Polynomials can only operate between other polynomials.
    The dunder methods defined are:
    __init__, __str__, __repr__, __add__, __sub__, __mul__, __truediv__, __pow__, __neg__, __len__, __eq__, __int__

    The custom methods are:
    grade(self) -> the highest grade of a Monomial
    order(self, letter: str, reverse: bool = False) -> orders the monomials by exponent of the letter
    complete(self, letter: str) -> completes the powers (from 0 to the highest) of a certain letter
    normal(self) -> sums similar monomials inside the polynomial
    clean(self) -> removes any monomial that has 0 as the number
    append_mon(self) -> appends a monomial to the end of the list
    copy(self) -> makes a copy of itself without creating aliases
    first_mon(self) -> returns the first monomial of the list
    root(self, rad_pow) -> calculates the root of the monomial (like a the power, but divides the exponents and the
                           number is being elevated to rad_pow ** -1)
    """


    # =========================Custom methods=========================

    # The highest grade of the monomials that contains
    def grade(self) -> int:
        grade = 0
        for mon in self.mon:
            grade = mon.grade() if mon.grade() > grade else grade

        return grade

    # Makes the polynomials ordered by a letter
    def order(self, letter: str, reverse: bool = False):

        if len(self.mon) > 1:

            # A simple bubble sort, there is no need for something faster
            for i in range(len(self.mon) - 1):
                for mon in range(len(self.mon) - (i + 1)):

                    try:
                        if self.mon[mon].lt[letter] > self.mon[mon + 1].lt[letter]:
                            self.mon[mon], self.mon[mon + 1] = self.mon[mon + 1], self.mon[mon]

                    except KeyError:
                        pass

        if reverse:
            self.mon.reverse()

    def complete(self, letter: str):
        self.order(letter)
        for mon in range(len(self.mon)):
            pass

    # Deletes any duplicates
    def normal(self):
        new_pl = self.copy()
        new_pl += Pol([])
        return new_pl

    def clean(self):
        for i in range(len(self.mon) - 1, -1, -1):
            if self.mon[i].num == 0:
                del self.mon[i]

        if not self.mon: self.mon = [Mon(0)]

    def append_mon(self, mon):
        self.mon.append(mon)

    def copy(self):
        return Pol(self.mon.copy())

    def first_mon(self):
        return self.mon[0]

    def root(self, rad_pow):  # Radical power

        if type(rad_pow) is not Pol or \
             len(self) != 1 or \
             int(rad_pow.first_mon().num) != rad_pow.first_mon().num:
            raise NonIntRootError

        if len(rad_pow) == 1 and rad_pow.first_mon().lt == MON_DICT:
            rad_pow_num = int(rad_pow.first_mon().num)

            if rad_pow_num == 0:
                return make_pol(1)

            else:
                result = copy(self.first_mon())
                for key in result.lt:
                    if key == "": result.num **= 1 / rad_pow_num
                    else        : result.lt[key] /= rad_pow_num

                return Pol([result])

        elif len(self) == 1:
            return Pol([self.first_mon() ** (1 / rad_pow)])

        else:
            raise NonIntRootError


    # =========================Dunder methods=========================

    def __init__(self, monomials: list):
        self.mon = monomials

    def __str__(self):
        output_string = ""

        for monomial in self.mon:
            if monomial.num >= 0 and output_string == "":
                output_string += str(abs(monomial))

            elif monomial.num < 0 and output_string == "":
                output_string += str(monomial)

            elif monomial.num >= 0:
                output_string += " + " + str(monomial)

            else:
                output_string += " - " + str(abs(monomial))

        return output_string

    def __repr__(self):
        return f"Pol({self.mon})"

    def __add__(self, other):
        new_pl = self.mon.copy() + other.mon.copy()

        for index in range(len(new_pl) - 1, -1, -1):
            monomial_calculated = 0
            for mon in range(index - 1, -1, -1):
                try:
                    new_pl[index - monomial_calculated] += new_pl[mon]
                    del new_pl[mon]
                    monomial_calculated += 1

                except NonSimMonError:
                    pass

        return Pol(new_pl)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        new_pl = Pol([])
        for mon in self.mon:
            for other_mon in other.mon:
                new_pl.append_mon(mon * other_mon)

        return new_pl.normal()

    def __truediv__(self, other):
        if len(self) == 1:
            if type(other) is Pol and len(other) == 1:
                return Pol([self.mon[0] / other.mon[0]])

            else: return Pol([self.mon[0] / other])

        else: raise ImpossibleDivError

    def __pow__(self, power, modulo=None):
        if type(power) is not Pol or \
             int(power.first_mon().num) != power.first_mon().num:  # Prevents floats from being powers
            raise NonIntPowError

        if len(power) == 1 and power.first_mon().lt == MON_DICT:
            pow_num = int(power.first_mon().num)

            if pow_num == 0:
                return make_pol(1)

            else:
                result = self.copy()
                for _ in range(pow_num - 1):
                    result *= self

                return result

        elif len(self) == 1:
            return Pol([self.first_mon() ** power])

        else:
            raise NonIntPowError

    def __neg__(self):
        for i in range(len(self.mon)):
            self.mon[i] = -self.mon[i]

        return self

    def __len__(self):
        return len(self.mon)

    def __eq__(self, other):
        if type(other) is not Pol:
            return False

        return self.mon == other.mon

    def __gt__(self, other):
        if len(self) != 1 or self.first_mon().lt != MON_DICT: return False

        if type(other) is float:
            return self.first_mon().num > other


        elif len(other) == 1 and other.first_mon().lt == MON_DICT:
            return self.first_mon().num > other.first_mon().num

        else: return False
