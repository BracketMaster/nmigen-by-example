# still largely experimental
# from nmigen.sim.cxxsim import Simulator

from nmigen import Signal, Elaboratable, Module
from nmigen.back.pysim import Simulator

class Top(Elaboratable):
    def __init__(self):
        self.counter = Signal(range(10))
        self.other = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.counter.eq(self.counter + 1)

        return m

if __name__ == '__main__':
    def process():
        for tick in range(10):
            print(f"counter = {(yield dut.counter)}")
            yield
    
    dut = Top()
    sim = Simulator(dut)
    sim.add_clock(1e-6)
    sim.add_sync_process(process)
    sim.run()
