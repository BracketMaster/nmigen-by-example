from nmigen import *

mem = Memory(width=32, depth=16)
rp = mem.read_port()
wp = mem.write_port()

m = Module()
m.submodules.rp = rp
m.submodules.wp = wp

class Check(Elaboratable):
    def __init__(self):
        self.check_in = Signal(range(4))
        self.check_out = Signal(range(4))
    
    def elaborate(self,platform):
        m = Module()
        m.d.sync += self.check_out.eq(self.check_in)
        return m

check = Check()
m.submodules.check = check

from nmigen.back.pysim import Simulator, Delay, Settle
sim = Simulator(m)
sim.add_clock(1e-6)

def peekmem():
    for slot in range(4):
        #set address
        yield rp.addr.eq(slot)
        yield check.check_in.eq(slot)
        yield
        yield Settle()
        print(f"ADDR = {(yield rp.addr)}")
        #print data
        print(f"mem[{slot}] = {(yield rp.data)}")

def pokemem():
    yield wp.en.eq(1)

    for slot in range(4):
        #set address
        yield wp.addr.eq(slot)
        #write data
        yield wp.data.eq(slot)
        yield

    yield wp.en.eq(0)
    yield

sim_writer = sim.write_vcd(f"{__file__[:-3]}.vcd")

with sim_writer:
    sim.add_sync_process(peekmem)
    sim.run()

    sim.add_sync_process(pokemem)
    sim.run()

    sim.add_sync_process(peekmem)
    sim.run()