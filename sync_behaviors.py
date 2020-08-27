"""
this tutorial tries to capture some subtleties
you might encounter when peeking at synchronous
logic.

These arrive from nMigen's use of Settle which
will likely be improved in future nMigen versions.

https://freenode.irclog.whitequark.org/nmigen/2020-08-27#27806940;
"""
from nmigen import *

class Simple(Elaboratable):
    def __init__(self):
        self.simple_in = Signal(range(4))
        self.simple_out = Signal(range(4))
    
    def elaborate(self,platform):
        m = Module()
        m.d.sync += self.simple_out.eq(self.simple_in)
        return m

m = Module()
simple = Simple()
m.submodules.simple = simple

from nmigen.back.pysim import Simulator, Delay, Settle
sim = Simulator(m)
sim.add_clock(1e-6)

def process():
    val = 2
    yield simple.simple_in.eq(val)
    yield
    # this will print simple_out = 0 which is the
    # reset value even though 
    # during this cycle, simple_out = 2
    # This is because as far as the simulator is concerned
    # we can't see changes until the edge right
    # before the next clock cycle
    print(f"simple_out = {(yield simple.simple_out)}")

    val = 3
    yield simple.simple_in.eq(val)
    yield
    yield Settle()
    # this will print out 3 as expected becuase
    # we use Settle() to advance right to the edge
    # before the next clock cycle
    print(f"simple_out = {(yield simple.simple_out)}")


sim_writer = sim.write_vcd(f"{__file__[:-3]}.vcd")

with sim_writer:
    sim.add_sync_process(process)
    sim.run()