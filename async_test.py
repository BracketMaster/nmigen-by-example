from nmigen import Signal, Elaboratable, Module
from nmigen import DomainRenamer, ClockDomain
from nmigen.lib.fifo import AsyncFIFOBuffered

class Producer(Elaboratable):
    def __init__(self, data_shape):

        # inputs
        self.w_rdy_i = Signal()

        # outputs
        self.w_en_o = Signal()
        self.w_data_o = Signal(data_shape)

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
    def __init__(self, data_shape):

        # inputs
        self.r_rdy_i = Signal()
        self.r_data_i = Signal(data_shape)

        # outputs
        self.r_en_o = Signal()
        self.data = Signal(data_shape)

    def elaborate(self, platform):
        m = Module()

        data = self.data

        with m.If(self.r_rdy_i):
            m.d.comb += self.r_en_o.eq(1)
            m.d.comb += data.eq(self.r_data_i)
        with m.Else():
            m.d.comb += self.r_en_o.eq(0)
            m.d.comb += data.eq(0)
        
        return m


class Top(Elaboratable):
    def __init__(self, data_width):
        # instantiate submodules
        self.producer = DomainRenamer("producer")\
            (Producer(data_width))
        self.consumer = DomainRenamer("consumer")\
            (Consumer(data_width))
        self.fifo = AsyncFIFOBuffered(width=data_width,
            depth=data_width, w_domain="producer", 
            r_domain="consumer")

    def elaborate(self, platform):
        m = Module()

        # create domains for the producer and consumer
        m.domains.producer = ClockDomain()
        m.domains.consumer = ClockDomain()

        # attach submodules
        m.submodules.producer = producer = self.producer
        m.submodules.consumer = consumer = self.consumer
        m.submodules.fifo = fifo = self.fifo

        # producer <> fifo
        m.d.comb += producer.w_rdy_i.eq(fifo.w_rdy)
        m.d.comb += fifo.w_en.eq(producer.w_en_o)
        m.d.comb += fifo.w_data.eq(producer.w_data_o)

        # consumer <> fifo
        m.d.comb += consumer.r_rdy_i.eq(fifo.r_rdy)
        m.d.comb += consumer.r_data_i.eq(fifo.r_data)
        m.d.comb += fifo.r_en.eq(consumer.r_en_o)
        
        return m

if __name__ == "__main__":
    from nmigen.back.pysim import Simulator, Tick
    
    top = Top(data_width=4)
    sim = Simulator(top)
    sim.add_clock(3e-6, domain="producer")
    sim.add_clock(5e-6, domain="consumer")

    
    sim_writer = sim.write_vcd(f"{__file__[:-3]}.vcd")

    # run simulation and write to VCD
    with sim_writer:

        def process():
            for tick in range(10):
                print(f"consumer.data = {yield top.consumer.data}")
                yield Tick(domain="consumer")

        # change to add process
        sim.add_process(process)
        sim.run()