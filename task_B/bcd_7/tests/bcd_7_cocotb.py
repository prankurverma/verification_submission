import random
import cocotb
from bcd_7_model import bcd_7_model
from cocotb.triggers import Timer
from cocotb.result import TestFailure, TestSuccess


##================================================================

@cocotb.test()
def bcd_7_test(dut):
    yield Timer(2)

    for i in range(10):
        d = random.randint(0, 9)
        

        dut.d = d

        yield Timer(2)

        if int(dut.seg) != int(bcd_7_model(d),2):
            raise TestFailure(
                "Randomised test failed with: %s : %s" %
                (int(dut.d), int(dut.seg)))
        else:
            dut._log.info("Ok!")

##================================================================

