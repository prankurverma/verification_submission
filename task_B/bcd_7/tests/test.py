import random
import cocotb

from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge

from cocotb.monitors import Monitor
from cocotb.drivers import BitDriver
from cocotb.binary import BinaryValue
from cocotb.regression import TestFactory
from cocotb.scoreboard import Scoreboard
from cocotb.result import TestFailure, TestSuccess

# ==============================================================================
@cocotb.test()
def bcd_7(dut):
    # Route signals from dut
    clk = dut.C
    clr = dut.CLR
    
    # generate clock signal using fork function
    cocotb.fork(Clock(clk, 100).start)

    # initialise bcd_7
    clr <= 1
    print("default zero")
    yield Timer(500)
    clr <= 0
    print("Starting the bcd to 7 seg")

    # Run 20 clock cycles
    for i in range(20):
        yield RisingEdge(clk)
        print("Count....%s%s%s%s" % (int(dut.Q3),int(dut.Q2),int(dut.Q1),int(dut.Q0)))
    
    # clear counter
    clr <= 1
    print("back to default zero")
    yield Timer(500)
    clr <= 0
    
    print("Starting the bcd to 7 seg - 2nd time")
    # Run 20 clock cycles
    for i in range(20):
        yield RisingEdge(clk)
        print("Count....%s%s%s%s" % (int(dut.Q3),int(dut.Q2),int(dut.Q1),int(dut.Q0)))
    
    print("Simulation ended")
# ==============================================================================


# ==============================================================================
class BitMonitor(Monitor):
    """Observes a single-bit input or output of DUT."""
    def __init__(self, name, signal, clock, callback=None, event=None):
        self.name = name
        self.signal = signal
        self.clock = clock
        Monitor.__init__(self, callback, event)
        
    @coroutine
    def _monitor_recv(self):
        clkedge = RisingEdge(self.clock)

        while True:
            # Capture signal at rising edge of clock
            yield clkedge
            vec = self.signal.value
            self._recv(vec)

# ==============================================================================
def input_gen():
    """Generator for input data applied by BitDriver"""
    while True:
        yield random.randint(1,5), random.randint(1,5)
        
# ==============================================================================
class BCD_7_TB(object):
    def __init__(self, dut, init_val):
        """
        Setup testbench.

        init_val signifies the BinaryValue which must be captured by the
        output monitor with the first rising clock edge. This is actually the initial 
        state of the flip-flop.
        """
        # Some internal state
        self.dut = dut
        self.stopped = False

        # Create input driver and output monitor
        self.input_drv = BitDriver(dut.d, dut.c, input_gen())
        self.output_mon = BitMonitor("output", dut.q, dut.c)
        
        # Create a scoreboard on the outputs
        self.expected_output = [ init_val ]
        self.scoreboard = Scoreboard(dut)
        self.scoreboard.add_interface(self.output_mon, self.expected_output)

        # Reconstruct the input transactions from the pins
        # and send them to our 'model'
        self.input_mon = BitMonitor("input", dut.d, dut.c,
                                    callback=self.model)

    def model(self, transaction):
        """Model the DUT based on the input transaction."""
        # Do not append an output transaction for the last clock cycle of the
        # simulation, that is, after stop() has been called.
        if not self.stopped:
            self.expected_output.append(transaction)

    def start(self):
        """Start generation of input data."""
        self.input_drv.start()

    def stop(self):
        """Stop generation of input data. 
        Also stop generation of expected output transactions.
        One more clock cycle must be executed afterwards so that the output of
        D-FF can be checked.
        """
        self.input_drv.stop()
        self.stopped = True

# ==============================================================================
@cocotb.coroutine
def run_test(dut):
    """Setup testbench and run a test."""

    cocotb.fork(Clock(dut.c, 5000).start())

    tb = BCD_7_TB(dut, BinaryValue(0, 1))

    clkedge = RisingEdge(dut.c)

    # Apply random input data by input_gen via BitDriver for 100 clock cycle.
    tb.start()
    for i in range(100):
        yield clkedge

    # Stop generation of input data. One more clock cycle is needed to capture
    # the resulting output of the DUT.
    tb.stop()
    yield clkedge

    # Print result of scoreboard.
    raise tb.scoreboard.result

# ==============================================================================
# Register the test.
factory = TestFactory(run_test)
factory.generate_tests()