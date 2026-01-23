from m5.objects import (
    DerivO3CPU,
    TournamentBP,
)

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator


class MyOutOfOrderCore(BaseCPUCore):
    def __init__(self, width, rob_size, num_int_regs, num_fp_regs):
        super().__init__(DerivO3CPU(), ISA.X86)
        self.core.fetchWidth = width
        self.core.decodeWidth = width
        self.core.renameWidth = width
        self.core.issueWidth = width
        self.core.wbWidth = width
        self.core.commitWidth = width

        self.core.numROBEntries = rob_size

        self.core.numPhysIntRegs = num_int_regs
        self.core.numPhysFloatRegs = num_fp_regs

        self.core.branchPred = TournamentBP()

        self.core.LQEntries = 128
        self.core.SQEntries = 128


class MyOutOfOrderProcessor(BaseCPUProcessor):
    def __init__(self, width, rob_size, num_int_regs, num_fp_regs):
        cores = [MyOutOfOrderCore(width, rob_size, num_int_regs, num_fp_regs)]
        super().__init__(cores)


my_x86_ooo_processor = MyOutOfOrderProcessor(
    width=8, rob_size=192, num_int_regs=256, num_fp_regs=256
)

main_memory = SingleChannelDDR4_2400(size="2GB")

cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="16kB",
    l1d_assoc=8,
    l1i_size="16kB",
    l1i_assoc=8,
    l2_size="256kB",
    l2_assoc=16,
    num_l2_banks=1,
)
board = SimpleBoard(
    processor=my_x86_ooo_processor,
    memory=main_memory,
    cache_hierarchy=cache_hierarchy,
    clk_freq="3GHz",
)

board.set_se_binary_workload(obtain_resource("x86-hello64-static"))

simulator = Simulator(board)
simulator.run()
