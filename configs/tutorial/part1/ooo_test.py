from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

# 1. Setup the Cache Hierarchy
cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1d_size="32kB", l1i_size="32kB", l2_size="256kB"
)

# 2. Setup Memory
memory = SingleChannelDDR4_2400(size="2GB")

# 3. Setup the Processor (Using the O3 model where your code lives)
# We use CPUTypes.O3 to point to DerivO3CPU
processor = SimpleProcessor(cpu_type=CPUTypes.O3, isa=ISA.X86, num_cores=1)

# 4. Setup the Board
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# 5. Set the Workload (A simple Hello World)
board.set_se_binary_workload(obtain_resource("x86-hello64-static"))

# 6. Run the Simulation
simulator = Simulator(board=board)
print("Beginning ACE Analysis Simulation...")
simulator.run()
print("Simulation Complete. Check m5out/stats.txt for ACE results.")
