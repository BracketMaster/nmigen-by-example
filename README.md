# nMigen By Example
This repository is meant to be a useful reference for some advanced aspects of nMigen.

If you're not yet familiar with nMigen, you may find [Robert Baruch's tutorials](https://github.com/RobertBaruch/nmigen-tutorial) to be more accessible.

# What is [nMigen](https://github.com/nmigen/nmigen)?
nMigen is an RTL implemented as a Python DSL.

It has the following strengths:

 - Emits Yoysys RTLIL
 - Emits veilog through Yosys RTLIL
 - Clean interface to FOSS SymbiYosys formal verification suite.
 - Clean and natural idioms.
 - Built in Python RTL Simulator
 - Will soon be capable of using the speedy YosysCXX simulator backend
 - Allows for anything Python enabling sane management of large codebases
   - Unit tests
   - list comprehensions
   - the list goes on...
 - nMigen SOC comes with nice tools such as Wishbone.

# Dependencies

You can install the dependencies below
easily with:

```
pip3 install -r requirements.txt
```

 - [nMigen](https://github.com/nmigen/nmigen)
   - ```pip install git+https://github.com/nmigen/nmigen.git```
 - [nMigen SOC Harry Ho Branch](https://github.com/HarryMakes/nmigen-soc)
   - ```pip3 install git+https://github.com/HarryMakes/nmigen-soc/@wishbone_interconnect```
 - [GTKWave](http://gtkwave.sourceforge.net)
 - [OR Scansion](http://www.logicpoet.com/scansion/)

# Usage
 - ``python3 mem.py`` - example on how to use nMigen SRAM
 - ``python3 sram_wishbone.py`` - using nMigen SRAM with
  wishbone 
 - ``python3 sync_behaviors.py`` - documenting some subtle
  nMigen Settle() behaviors
 - ``python3 async_test.py`` - communication between clock
  domains with asynchronous Fifo

# TODO
 - [ ] Finish cache example
 - [ ] make [print_sig](https://github.com/BracketMaster/nmigen-by-example/blob/master/sram_wishbone.py#L24)
 a common utility
 - [x] remove ```import *```