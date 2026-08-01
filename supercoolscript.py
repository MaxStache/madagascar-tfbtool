from tfbscript import ScriptFile
from tfbscript import open_editor
from tfbscript.opcodes import OpPrescript, OpStartup, OpShutdown
from tfbscript.opcodes.op_behavior_implementation import OpBehaviorImplementation
from tfbscript.opcodes.op_check_value import OpCheckValue
from tfbscript.opcodes.op_set_behavior import OpSetBehavior
from tfbscript.reference import Reference
from tfbscript.rhs import Rhs
from tfbscript.string_table import StringTableEntry

script = ScriptFile()

LOCAL_REFS = [
    StringTableEntry(string="Idle::behavior"),
    StringTableEntry(string="Action 1::behavior"),
    StringTableEntry(string="Action 2::behavior"),
    StringTableEntry(string="Action 3::behavior"),
    StringTableEntry(string="Action 4::behavior"),
    StringTableEntry(string="controller 1::controller"),
]

script.local_refs.entries.extend(LOCAL_REFS)

i_prescript = OpPrescript()
script.instructions.append(i_prescript)

i_startup = OpStartup()
i_prescript.children.append(i_startup)

i_shutdown = OpShutdown()
i_prescript.children.append(i_shutdown)

# region behav idle
i_behv_idle = OpBehaviorImplementation()
i_behv_idle.behavior_entry = script.local_refs.entries[0]
script.instructions.append(i_behv_idle)

i_behv_idle_check_controller_1 = OpCheckValue()
i_behv_idle_check_controller_1.lhs = Reference.createSimple_local(
    script.local_refs, slot=5
)
i_behv_idle_check_controller_1.rhs = Rhs
i_behv_idle_check_controller_1.lhs.member = 0x01
i_behv_idle.children.append(i_behv_idle_check_controller_1)
# endregion

# region Action 1
i_behv_act1 = OpBehaviorImplementation()
i_behv_act1.behavior_entry = script.local_refs.entries[1]
i_behv_act1.flags.flow_control = 0  # Flow END
script.instructions.append(i_behv_act1)

behv_act1_i_setbehav = OpSetBehavior()
behv_act1_i_setbehav.behavior = Reference.createSimple_local(script.local_refs, slot=0)

i_behv_act1.children.append(behv_act1_i_setbehav)
# endregion

# region Action 2
i_behv_act2 = OpBehaviorImplementation()
i_behv_act2.behavior_entry = script.local_refs.entries[2]
i_behv_act2.flags.flow_control = 0  # Flow END
script.instructions.append(i_behv_act2)

behv_act2_i_setbehav = OpSetBehavior()
behv_act2_i_setbehav.behavior = Reference.createSimple_local(script.local_refs, slot=0)

i_behv_act2.children.append(behv_act2_i_setbehav)
# endregion

# region Action 3
i_behv_act3 = OpBehaviorImplementation()
i_behv_act3.behavior_entry = script.local_refs.entries[3]
i_behv_act3.flags.flow_control = 0  # Flow END
script.instructions.append(i_behv_act3)

behv_act3_i_setbehav = OpSetBehavior()
behv_act3_i_setbehav.behavior = Reference.createSimple_local(script.local_refs, slot=0)

i_behv_act3.children.append(behv_act3_i_setbehav)
# endregion

# region Action 4
i_behv_act4 = OpBehaviorImplementation()
i_behv_act4.behavior_entry = script.local_refs.entries[4]
i_behv_act4.flags.flow_control = 0  # Flow END
script.instructions.append(i_behv_act4)

behv_act4_i_setbehav = OpSetBehavior()
behv_act4_i_setbehav.behavior = Reference.createSimple_local(script.local_refs, slot=0)

i_behv_act4.children.append(behv_act4_i_setbehav)
# endregion

open_editor(script)
