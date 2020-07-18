from nmigen import Signal, Elaboratable, Module
from nmigen import DomainRenamer, ClockDomain
from nmigen.lib.fifo import AsyncFIFOBuffered

class Producer(Elaboratable):
    def __init__(self, w_rdy_i, w_en_o, w_data_o):

        # inputs
        self.w_rdy_i = w_rdy_i

        # outputs
        self.w_en_o = w_en_o
        self.w_data_o = w_data_o

    def elaborate(self, platform):
        m = Module()

        data = Signal(4)

        with m.If(self.w_rdy_i):
            m.d.comb += self.w_en_o.eq(1)
            m.d.comb += self.w_data_o.eq(data)
            m.d.sync += data.eq(data + 1)
        with m.Else():
            m.d.comb += self.w_en_o.eq(0)

        return m

class Consumer(Elaboratable):
    def __init__(self, r_rdy_i, r_data_i, r_en_o):

        # inputs
        self.r_rdy_i = r_rdy_i
        self.r_data_i = r_data_i

        # outputs
        self.r_en_o = r_en_o
        self.data = Signal(4)

    def elaborate(self, platform):
        m = Module()

        data = self.data

        with m.If(self.r_rdy_i):
            m.d.comb += self.r_en_o.eq(1)
            m.d.sync += data.eq(self.r_data_i)
        with m.Else():
            m.d.comb += self.r_en_o.eq(0)
            m.d.sync += data.eq(0)
        
        return m


class Top(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        # create domains for the producer and consumer
        m.domains.producer = ClockDomain()
        m.domains.consumer = ClockDomain()

        # create FIFO shared between producer and consumer
        m.submodules.fifo = fifo = AsyncFIFOBuffered(
            width=4, depth=4, w_domain="producer", r_domain="consumer"
            )

        # create producer
        self.producer = m.submodules.producer = DomainRenamer("producer")(
            Producer(
                w_rdy_i = fifo.w_rdy, w_en_o = fifo.w_en, w_data_o= fifo.w_data
                )
            )

        # create consumer 
        self.consumer = m.submodules.consumer = DomainRenamer("consumer")(
            Consumer(
                r_rdy_i = fifo.r_rdy, r_data_i = fifo.r_data, r_en_o = fifo.r_en
                )
            )
        
        return m

if __name__ == "__main__":
    from nmigen.back.pysim import Simulator, Tick
    
    top = Top()
    sim = Simulator(top)
    sim.add_clock(1e-6, domain="producer")
    sim.add_clock(5e-6, domain="consumer")

    
    sim_writer = sim.write_vcd(f"{__file__[:-3]}.vcd")

    # run simulation and write to VCD
    with sim_writer:

        def process():
            for tick in range(10):
                print(f"consumer.data = {yield top.consumer.data}")
                yield Tick(domain="consumer")

        sim.add_sync_process(process, domain="consumer")
        sim.run()