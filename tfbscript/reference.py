import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar, override

from tfbscript.ansi import builtin, variable, variable_global
from tfbscript.string_table import StringTable, StringTableEntry

if TYPE_CHECKING:
    from tfbscript.binary import BinaryReader
    from tfbscript.opcodes.base import ParserContext, Opcode

_OpcodeT = TypeVar("_OpcodeT", bound="Opcode")

LOCAL_BASE = 0x3FC0D
BUILTIN_BASE = 0x3FFFA
NULL_REF = 0xFFFFFFFF

BUILTINS = {
    # comment = type resolving implemented
    0x3FFFF: "self", # yes
    0x3FFFE: "[~controlled]", # yes
    0x3FFFD: "[~current in for each]", # no (see comment)
    0x3FFFC: "[~subset]", # yes
    0x3FFFB: "[~message value]", # yes
    0x3FFFA: "[~found variable]", # yes
}

BINDINGS = {
    "actor": {
        0x01: {"name": "health", "type": "value"},
        0x02: {"name": "waypoints", "type": "set"},  # set::actor
        0x03: {"name": "origin", "type": "value"},
        0x04: {"name": "destination (point)", "type": "value"},
        0x05: {"name": "heading (OBSOLETE)", "type": "value"},
        0x06: {"name": "facing (OBSOLETE)", "type": "value"},
        0x07: {"name": "current speed", "type": "value"},
        0x08: {"name": "altitude", "type": "value"},
        0x09: {"name": "attach points", "type": "set"},  # set::actor
        0x0A: {"name": "activation range fade percent", "type": "value"},
        0x0B: {"name": "activation range", "type": "value"},
        0x0C: {"name": "deactivation range", "type": "value"},
        0x0D: {"name": "clones", "type": "set"},  # set::actor
        0x0E: {"name": "ground top speed", "type": "value"},
        0x0F: {"name": "ground turn rate", "type": "value"},
        0x10: {"name": "ground acceleration", "type": "value"},
        0x11: {"name": "ground deceleration", "type": "value"},
        0x12: {"name": "move type", "type": "value"},
        0x13: {"name": "air top speed", "type": "value"},
        0x14: {"name": "air turn rate", "type": "value"},
        0x15: {"name": "air acceleration", "type": "value"},
        0x16: {"name": "air deceleration", "type": "value"},
        0x17: {"name": "jump delay", "type": "value"},
        0x18: {"name": "initial jump velocity", "type": "value"},
        0x19: {"name": "jump coast frames", "type": "value"},
        0x1A: {"name": "up top speed", "type": "value"},
        0x1B: {"name": "up acceleration", "type": "value"},
        0x1C: {"name": "down top speed", "type": "value"},
        0x1D: {"name": "down acceleration", "type": "value"},
        0x1E: {"name": "animation rate multiplier", "type": "value"},
        0x1F: {"name": "weight", "type": "value"},
        0x20: {"name": "bounce restitution", "type": "value"},
        0x21: {"name": "X offset", "type": "value"},  # Extend box X
        0x22: {"name": "Y offset", "type": "value"},  # Extend box Y
        0x23: {"name": "Z offset", "type": "value"},  # Extend box Z
        0x24: {"name": "W extend", "type": "value"},  # Extend box W extend
        0x25: {"name": "L extend", "type": "value"},  # Extend box L extend
        0x26: {"name": "H extend", "type": "value"},  # Extend box H extend
        0x27: {"name": "cone angle", "type": "value"},
        0x28: {"name": "cone length", "type": "value"},
        0x29: {"name": "cone sweep offset", "type": "value"},
        0x2A: {"name": "blip color", "type": "value"},
        0x2B: {"name": "cone color", "type": "value"},
        0x2C: {"name": "solid collision", "type": "value"},
        0x2D: {"name": "wall collision", "type": "value"},
        0x2E: {"name": "visible on radar", "type": "value"},
        0x2F: {"name": "wall climber", "type": "value"},
        0x30: {"name": "cut-scene ignore", "type": "value"},
        0x31: {"name": "ignore ground color", "type": "value"},
        0x32: {"name": "tilts with ground", "type": "value"},
        0x33: {"name": "no shadow", "type": "value"},
        0x34: {"name": "ID", "type": "value"},
        0x35: {"name": "mesh collider", "type": "value"},
        0x36: {"name": "triangles collide", "type": "value"},
        0x37: {"name": "tint color", "type": "value"},
        0x38: {"name": "turrets", "type": "set"},
    },
    "camera": {
        0x01: {"name": "look from", "type": "value"},
        0x02: {"name": "look from horizontal offset", "type": "value"},
        0x03: {"name": "look from vertical offset", "type": "value"},
        0x04: {"name": "look from heading offset", "type": "value"},
        0x05: {"name": "look from heading relative", "type": "value"},
        0x06: {"name": "look at", "type": "value"},
        0x07: {"name": "look at horizontal offset", "type": "value"},
        0x08: {"name": "look at vertical offset", "type": "value"},
        0x09: {"name": "look at heading offset", "type": "value"},
        0x0A: {"name": "look at heading relative", "type": "value"},
        0x0B: {"name": "field of view", "type": "value"},
        0x0C: {"name": "laziness", "type": "value"},
        0x0D: {"name": "percent complete", "type": "value"},
        0x0E: {"name": "time remaining", "type": "value"},
        0x0F: {"name": "Vertical Follow At", "type": "value"},
        0x10: {"name": "Horizontal Follow", "type": "value"},
        0x11: {"name": "Current Facing", "type": "value"},
        0x12: {"name": "Vertical Follow From", "type": "value"},
        0x13: {"name": "pitch control", "type": "value"},
        0x14: {"name": "roll", "type": "value"},
    },
    "sprite": {  # TODO: confirm labels
        0x01: {"name": "content", "type": "value"},
        0x02: {"name": "location", "type": "value"},  # Pair16, sub 1 = x, sub 2 = y
        0x03: {"name": "scale", "type": "value"},
        0x04: {"name": "rotation", "type": "value"},
        0x05: {"name": "tint color", "type": "value"},
        0x06: {"name": "justification", "type": "value"},
        0x07: {"name": "visible", "type": "value"},
        0x08: {"name": "clones", "type": "set"},  # set::sprite
        0x09: {"name": "priority", "type": "value"},  # z-order!?
        0x0A: {
            "name": "pixel extends",
            "type": "value",
        },  # Pair16, sub 1 = x, sub 2 = y
    },
    "sound": {
        0x01: {"name": "volume", "type": "value"},
        0x02: {"name": "pitch", "type": "value"},
        0x03: {"name": "elapsed time", "type": "value"},
        0x04: {"name": "remaining time", "type": "value"},
    },
    "controller": {
        0x01: {"name": "circle button", "type": "value"},
        0x02: {"name": "triangle button", "type": "value"},
        0x03: {"name": "X button", "type": "value"},
        0x04: {"name": "square button", "type": "value"},
        0x05: {"name": "select button", "type": "value"},
        0x06: {"name": "start button", "type": "value"},
        0x07: {"name": "L1 button", "type": "value"},
        0x08: {"name": "R1 button", "type": "value"},
        0x09: {"name": "L2 button", "type": "value"},
        0x0A: {"name": "R2 button", "type": "value"},
        0x0B: {"name": "DPad left", "type": "value"},
        0x0C: {"name": "DPad right", "type": "value"},
        0x0D: {"name": "DPad up", "type": "value"},
        0x0E: {"name": "DPad down", "type": "value"},
        0x0F: {"name": "analog1 left", "type": "value"},
        0x10: {"name": "analog1 right", "type": "value"},
        0x11: {"name": "analog1 up", "type": "value"},
        0x12: {"name": "analog1 down", "type": "value"},
        0x13: {"name": "analog2 left", "type": "value"},
        0x14: {"name": "analog2 right", "type": "value"},
        0x15: {"name": "analog2 up", "type": "value"},
        0x16: {"name": "analog2 down", "type": "value"},
        0x17: {"name": "analog1 heading", "type": "value"},
        0x18: {"name": "analog1 magnitude", "type": "value"},
        0x19: {"name": "analog2 heading", "type": "value"},
        0x1A: {"name": "analog2 magnitude", "type": "value"},
        0x1B: {"name": "connection", "type": "value"},
    },
    "MOTION BLUR": {
        0x01: {"name": "amount", "type": "value"},
        0x02: {"name": "offset-x", "type": "value"},
        0x03: {"name": "offset-y", "type": "value"},
        0x04: {"name": "scale x-axis", "type": "value"},
        0x05: {"name": "scale y-axis", "type": "value"},
        0x06: {"name": "scale", "type": "value"},
        0x07: {"name": "angle", "type": "value"},
    },
    "animation mapping": {
        0x01: {"name": "ambient", "type": "value"},
        0x02: {"name": "slowest move", "type": "value"},
        0x03: {"name": "slow move", "type": "value"},
        0x04: {"name": "fast move", "type": "value"},
        0x05: {"name": "jump", "type": "value"},
        0x06: {"name": "fall", "type": "value"},
        0x07: {"name": "youch", "type": "value"},
        0x08: {"name": "slide", "type": "value"},
        0x09: {"name": "attack 1", "type": "value"},
        0x0A: {"name": "attack 2", "type": "value"},
        0x0B: {"name": "tumble", "type": "value"},
        0x0C: {"name": "extra 1", "type": "value"},
        0x0D: {"name": "extra 2", "type": "value"},
        0x0E: {"name": "extra 3", "type": "value"},
        0x0F: {"name": "extra 4", "type": "value"},
        0x10: {"name": "extra 5", "type": "value"},
        0x11: {"name": "extra 6", "type": "value"},
        0x12: {"name": "extra 7", "type": "value"},
        0x13: {"name": "extra 8", "type": "value"},
        0x14: {"name": "extra 9", "type": "value"},
        0x15: {"name": "extra 10", "type": "value"},
        0x16: {"name": "extra 11", "type": "value"},
        0x17: {"name": "extra 12", "type": "value"},
        0x18: {"name": "extra 13", "type": "value"},
        0x19: {"name": "extra 14", "type": "value"},
        0x1A: {"name": "extra 15", "type": "value"},
        0x1B: {"name": "extra 16", "type": "value"},
        0x1C: {"name": "extra 17", "type": "value"},
        0x1D: {"name": "extra 18", "type": "value"},
        0x1E: {"name": "extra 19", "type": "value"},
        0x1F: {"name": "extra 20", "type": "value"},
        0x20: {"name": "extra 21", "type": "value"},
        0x21: {"name": "extra 22", "type": "value"},
        0x22: {"name": "extra 23", "type": "value"},
        0x23: {"name": "extra 24", "type": "value"},
        0x24: {"name": "extra 25", "type": "value"},
        0x25: {"name": "extra 26", "type": "value"},
        0x26: {"name": "extra 27", "type": "value"},
        0x27: {"name": "extra 28", "type": "value"},
        0x28: {"name": "extra 29", "type": "value"},
        0x29: {"name": "extra 30", "type": "value"},
        0x2A: {"name": "extra 31", "type": "value"},
        0x2B: {"name": "extra 32", "type": "value"},
        0x2C: {"name": "left turn", "type": "value"},
        0x2D: {"name": "right turn", "type": "value"},
        0x2E: {"name": "jump land slow", "type": "value"},
        0x2F: {"name": "jump land running", "type": "value"},
        0x30: {"name": "jump land hard", "type": "value"},
        0x31: {"name": "stop from full speed", "type": "value"},
        0x32: {"name": "stop from slow speed", "type": "value"},
        0x33: {"name": "running 180 change", "type": "value"},
        0x34: {"name": "player 9", "type": "value"},
        0x35: {"name": "player 10", "type": "value"},
        0x36: {"name": "player 11", "type": "value"},
        0x37: {"name": "player 12", "type": "value"},
        0x38: {"name": "player 13", "type": "value"},
        0x39: {"name": "player 14", "type": "value"},
        0x3A: {"name": "lean left slow", "type": "value"},
        0x3B: {"name": "lean left medium", "type": "value"},
        0x3C: {"name": "lean left fast", "type": "value"},
        0x3D: {"name": "lean right slow", "type": "value"},
        0x3E: {"name": "lean right medium", "type": "value"},
        0x3F: {"name": "lean right fast", "type": "value"},
    },
    "particle": {
        0x01: {"name": "output rate", "type": "value"},
        0x02: {"name": "output rate spread", "type": "value"},
        0x03: {"name": "lifetime", "type": "value"},
        0x04: {"name": "lifetime spread", "type": "value"},
        0x05: {"name": "clones (list)", "type": "set"},
        0x06: {"name": "activation range", "type": "value"},
        0x07: {"name": "deactivation range", "type": "value"},
        0x08: {"name": "primary start velocity", "type": "value"},
        0x09: {"name": "primary start velocity spread", "type": "value"},
        0x0A: {"name": "primary start gravity", "type": "value"},
        0x0B: {"name": "primary start drag", "type": "value"},
        0x0C: {"name": "primary start color", "type": "value"},
        0x0D: {"name": "primary start color spread", "type": "value"},
        0x0E: {"name": "primary start size", "type": "value"},
        0x0F: {"name": "primary start size spread", "type": "value"},
        0x10: {"name": "primary end velocity", "type": "value"},
        0x11: {"name": "primary end velocity spread", "type": "value"},
        0x12: {"name": "primary end gravity", "type": "value"},
        0x13: {"name": "primary end drag", "type": "value"},
        0x14: {"name": "primary end color", "type": "value"},
        0x15: {"name": "primary end color spread", "type": "value"},
        0x16: {"name": "primary end size", "type": "value"},
        0x17: {"name": "primary end size spread", "type": "value"},
        0x18: {"name": "emitter spread x", "type": "value"},
        0x19: {"name": "emitter spread y", "type": "value"},
        0x1A: {"name": "emitter spread z", "type": "value"},
        0x1B: {"name": "angular spread x", "type": "value"},
        0x1C: {"name": "angular spread y", "type": "value"},
        0x1D: {"name": "visual radius", "type": "value"},
        0x1E: {"name": "cut-scene ignore", "type": "value"},
    },
    "MATH OPS": {
        0x01: {"name": "Normalized Angle", "type": "value"},
    },
    "MemCard": {
        0x01: {"name": "Unplugged", "type": "value"},
        0x02: {"name": "Free Space", "type": "value"},
        0x03: {"name": "Status", "type": "value"},
        0x04: {"name": "Auto-Save", "type": "value"},
        0x05: {"name": "Auto-Load", "type": "value"},
        0x06: {"name": "Current Slot", "type": "value"},
        0x07: {"name": "Current Slot Size", "type": "value"},
        0x08: {"name": "Auto-Format", "type": "value"},
        0x09: {"name": "Auto-Delete", "type": "value"},
        0x0A: {"name": "Saved Language", "type": "value"},
        0x0B: {"name": "Current Slot Percent Complete", "type": "value"},
        0x0C: {"name": "Auto-Create", "type": "value"},
        0x0D: {"name": "Current Slot Game Time", "type": "value"},
        0x0E: {"name": "Changed State", "type": "value"},
    },
    "FOG": {
        0x01: {"name": "vertex fog distance", "type": "value"},
        0x02: {"name": "vertex fog color", "type": "value"},
        0x03: {"name": "pixel fog/DOF distance", "type": "value"},
        0x04: {"name": "pixel fog/DOF cutoff intensity", "type": "value"},
        0x05: {"name": "pixel fog toggle", "type": "value"},
        0x06: {"name": "DOF bluriness factor", "type": "value"},
        0x07: {"name": "pixel fog/DOF color", "type": "value"},
        0x08: {"name": "bloom toggle", "type": "value"},
        0x09: {"name": "bloom add factor", "type": "value"},
        0x0A: {"name": "bloom halo size", "type": "value"},
    },
    "rumble": {
        0x01: {"name": "low frequency", "type": "value"},
        0x02: {"name": "high frequency", "type": "value"},
        0x03: {"name": "duration", "type": "value"},
        0x04: {"name": "radius", "type": "value"},
        0x05: {"name": "attenuation", "type": "value"},
        0x06: {"name": "time remaining", "type": "value"},
    },
}


@dataclass
class Reference:
    raw: int = 0x00  # the 32-bit little-endian value R
    index: int = 0  # R >> 14
    member: int = 0  # (R >> 8) & 0x3F  -- field within the target
    scope: int = 0  # (R >> 6) & 3
    sub: int = 0  # R & 0x3F
    kind: str = "null"  # 'null' | 'builtin' | 'global' | 'local'
    slot: int | None = None  # table index used for the lookup (None for null/builtin)
    name: str = "<null>"  # resolved name (or descriptive placeholder)
    entry: StringTableEntry | None = None  # resolved entry (None for null/builtin)
    context: "ParserContext | None" = (
        None  # script's parser context (for resolving builtin types)
    )

    @classmethod
    def read(
        cls,
        reader: "BinaryReader",
        global_refs: StringTable,
        local_refs: StringTable,
        context: "ParserContext | None" = None,
    ) -> "Reference":
        """Parse a 4-byte TFB-Script variable reference.

        Args:
            reader: BinaryReader positioned at the reference.
            global_refs: the script's 2nd string table (globals) for name resolution.
            local_refs: the script's 3rd string table (locals) for name resolution.
            context: the script's parser context, used to resolve the type of
                some builtins (e.g. "[~subset]") from prior opcodes.
        Returns:
            A Reference with the decoded bit-fields and a resolved `name`.
        """
        if reader.size_remaining() < 4:
            raise ValueError("a reference is 4 bytes")

        raw = reader.read_u32()
        fields = {
            "raw": raw,
            "index": raw >> 14,
            "member": (raw >> 8) & 0x3F,
            "scope": (raw >> 6) & 3,
            "sub": raw & 0x3F,
        }
        index = fields["index"]

        if raw == NULL_REF:
            return cls(
                **fields,
                kind="null",
                slot=None,
                name="<null>",
                entry=None,
                context=context,
            )

        if index >= BUILTIN_BASE:
            name = BUILTINS.get(index, f"builtin@{index:#x}")
            return cls(
                **fields,
                kind="builtin",
                slot=None,
                name=name,
                entry=None,
                context=context,
            )

        if index < LOCAL_BASE:
            entry = global_refs.get(index)
            name = entry.string if entry is not None else f"unk_global#{index}"
            return cls(
                **fields,
                kind="global",
                slot=index,
                name=name,
                entry=entry,
                context=context,
            )

        slot = index - LOCAL_BASE
        entry = local_refs.get(slot)
        name = entry.string if entry is not None else f"local#{slot}"
        return cls(
            **fields, kind="local", slot=slot, name=name, entry=entry, context=context
        )

    @override
    def __str__(self) -> str:
        if self.kind == "null":
            return "<null>"

        if self.kind == "global":
            s = variable_global(f"global::{self.name}")
        elif self.kind == "local" and self.entry is not None:
            s = variable(self.name)
        elif self.kind == "builtin":
            s = builtin(self.name)
        else:
            s = self.name

        if self.member:
            s += self._get_member_string() or ""

        if self.sub:
            s += f".sub[{self.sub:#04x}]"
        if self.scope:
            s += f"@{self.scope}"  # set index for example
        return s

    def _get_member_string(self) -> str | None:
        my_type = self.get_resolved_type()

        if my_type is not None:
            my_bindings = BINDINGS.get(my_type)

            if my_bindings is not None:
                my_field = my_bindings.get(self.member)

                if my_field is not None:
                    label = my_field.get("name")
                    type_ = my_field.get("type")

                    if type_ == "set":
                        return f".[{label}]"
                    else:
                        return f".{label}"
                else:
                    print(
                        "WARN: cant resolve binding for",
                        my_type,
                        "member",
                        hex(self.member),
                        "entry",
                        self.entry,
                        file=sys.stderr,
                    )

            else:
                print(
                    "WARN: cant resolve bindings for \"",
                    my_type,
                    "\" entry",
                    self.entry,
                    file=sys.stderr,
                )
                #raise ValueError(
                #    f"Reference {self.name} has no bindings for type '{my_type}'"
                #)

        return f".field[{self.member:#04x}]"

    def get_resolved_type(self) -> str | None:
        if self.kind == "null":
            return "null"

        if self.kind == "builtin":
            if self.name == "self":
                return "actor"
            elif self.name == "[~subset]":
                from tfbscript.opcodes.op_check_fov import OpCheckFOV
                from tfbscript.opcodes.op_find_subset import OpFindSubset

                producer = self._builtin_find_producer((OpCheckFOV, OpFindSubset))

                if isinstance(producer, OpFindSubset):
                    return producer.set_ref.get_resolved_type()
                else:
                    return producer.target_ref.get_resolved_type()
                
            elif self.name == "[~message value]":
                return "value" # TODO: maybe we can resolve here??? seems kinda hard to do, since the message value is set by the sender and we don't have that context here

            elif self.name == "[~found variable]":
                # Not tested on real scripts cus couldnt find one
                from tfbscript.opcodes.op_find_variable import OpFindVariable

                producer = self._builtin_find_producer(OpFindVariable)
                return producer.var_ref.get_resolved_type()

            elif self.name == "[~current in for each]":
                from tfbscript.opcodes.op_for_each import OpForEach

                producer = self._builtin_find_producer(OpForEach)
                return producer.set_ref.get_resolved_type()

            elif self.name == "[~controlled]":
                from tfbscript.opcodes.op_control import OpControl
                from tfbscript.opcodes.op_spawn_actor import OpSpawnActor

                producer = self._builtin_find_producer((OpControl, OpSpawnActor))

                if isinstance(producer, OpControl):
                    return producer.target.get_resolved_type()
                else:
                    return producer.clone_ref.get_resolved_type()
            
            else: # 43 fail
                raise ValueError(self.name)
                return None  # TODO resolve other builtins to their types if possible

        if self.kind == "global" or self.kind == "local":  # variable
            if self.entry is not None:
                return self.entry.type
            else:
                raise ValueError(f"Reference {self.name} has no entry to resolve type")

        return None  # Should never reach here

    def _builtin_find_producer(self, opcode_types: type[_OpcodeT] | tuple[type[_OpcodeT], ...]):
        if self.context is None:
            raise ValueError(
                f"Reference {self.name} is a builtin (and a field on it is used) but has no context to resolve its type"
            )
        producer = self.context.nearest_ancestor(opcode_types)
        if producer is None:
            raise ValueError(
                f"Reference {self.name} is a builtin (and a field on it is used) but has no enclosing op to resolve its type"
            )

        return producer
