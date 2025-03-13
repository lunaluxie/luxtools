from decimal import Decimal

class NumericResult():
    def __init__(self, value:float, uncertainty:float=0, unit:str=""):
        """Initialize NumericResult with value, uncertainty and unit.

        Args:
            value (float): Value of your measurement
            uncertainty (float, optional): Uncertainty of your measurement
            unit (str, optional): Unit of measurement. Defaults to "".
        """
        self.value = Decimal(value).normalize()
        self.uncertainty = Decimal(uncertainty).normalize()
        self.unit = unit


        adjustment = self.uncertainty.adjusted()
        self.exponent = self.value.adjusted() # exponent so value has 1 digit before comma

        # skip if uncertainty is zero: just use all the precision in value.
        # a bit of a hack TODO: Fix.
        if self.uncertainty == Decimal(0):
            quantize_amount = Decimal(f"1e{self.exponent-1}")#.normalize()
            self.quantized_value = (self.value*Decimal(10**(-self.exponent))).quantize(quantize_amount)
            self.quantized_uncertainty = Decimal(0)
            return

        exponent_difference = Decimal(adjustment-self.exponent)

        if exponent_difference > 0:
            """If the significant digits of the uncertainty are greater than the significant digits of the value,
               we round to the exponent of the uncertainty."""
            self.exponent = adjustment
            exponent_difference = Decimal(0)


        quantize_amount = Decimal(f"1e{adjustment}").normalize()

        rounded_value = self.value.quantize(quantize_amount)
        self.quantized_value = (rounded_value*Decimal(10**(-adjustment))).to_integral()*Decimal(10**exponent_difference)

        rounded_uncertainty = Decimal(self.uncertainty.quantize(quantize_amount))
        self.quantized_uncertainty = (rounded_uncertainty*Decimal(10**(-adjustment))).to_integral()*Decimal(10**exponent_difference)

    def __repr__(self):
        return self.__str__()

    def __str__(self):

        if self.exponent == 0:
            return f"({self.quantized_value} ± {self.quantized_uncertainty}) {self.unit}".strip()
        else:
            return f"({self.quantized_value} ± {self.quantized_uncertainty})*10^({self.exponent}) {self.unit}".strip()

    def safe_str(self):
        if self.exponent == 0:
            return f"({self.quantized_value} +/- {self.quantized_uncertainty}) {self.unit}".strip()
        else:
            return f"({self.quantized_value} +/- {self.quantized_uncertainty})*10^({self.exponent}) {self.unit}".strip()

    def latex(self, delimiter:str=""):

        if self.exponent == 0:
            return f"{delimiter}({self.quantized_value} \\pm {self.quantized_uncertainty}) {self.unit}{delimiter}".strip()
        else:
            return f"{delimiter}({self.quantized_value} \\pm {self.quantized_uncertainty})\\cdot 10^{'{'+str(self.exponent)+'}'} {self.unit}{delimiter}".strip()


if __name__=="__main__":



    unit = ""
    tests = [
        (1.23456789e-9, 9.87654321e-11, "(1.2 +/- 0.1)*10^(-9)"),
    ]

    print(NumericResult(*tests[0][:2]).latex(delimiter="$"))

    # for value, uncertainty, expected in tests:
    #     result = NumericResult(value, uncertainty, unit)
    #     print(result)
    #     assert result.safe_str() == expected, f"Expected {expected} but got {result.safe_str()}"