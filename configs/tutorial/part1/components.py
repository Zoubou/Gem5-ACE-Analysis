# configs/tutorial/part1/components.py

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

#
# 1. Cache Hierarchy (Ruby MESI two-level)
#
cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="16KiB",
    l1d_assoc=8,
    l1i_size="16KiB",
    l1i_assoc=8,
    l2_size="256KiB",
    l2_assoc=16,
    num_l2_banks=1,
)

#
# 2. Memory System (Single channel DDR4 2400)
#
memory = SingleChannelDDR4_2400()

#
# 3. Processor (X86, single core, Timing CPU)
#
processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, isa=ISA.X86, num_cores=1)

#
# 4. Board (SE Mode)
#
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

#
# 5. Workload – X86 SE-mode executable
#    We use "x86-hello64-static" which is available from gem5 resources.
#
board.set_se_binary_workload(obtain_resource("x86-hello64-static"))

#
# 6. Simulator
#
simulator = Simulator(board=board)
simulator.run()
