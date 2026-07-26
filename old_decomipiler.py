class CheckFOVMode(IntEnum):
    """Mode for OpCheckFOV."""

    ignore_obstructions = 0

    consider_obstructions = 1





elif op_name == "check fov::op-code":
        """
        Is there an actor from target_ref within arc_width°
        of angle_base, whose distance to me satisfies
        "distance range_relop range°",
        and if mode == consider_obstructions,
        i have a clear line of sight to them?
        """
        p = OpParser(instr["payload"])

        angle_base = p.readRHS()
        arc_width = p.readRHS()
        target_ref = p.readRef()
        range_relop = RelOp(p.readUint8())  # how angle compares to range
        range = p.readRHS()
        mode = CheckFOVMode(p.readUint8())

        line = BUILD_LINE(
            prefix,
            "CHECK FOV",
            f"{(target_ref)} is within a {(arc_width)}° cone centered on heading {(angle_base)}, distance {(range_relop)} {(range)}, {(mode)}",
        )



elif op_name == "use camera::op-code":
        p = OpParser(instr["payload"])

        cam_ref = p.readRef()
        trans_in_mode = p.readUint8()
        trans_in_duration = p.readFloat()
        trans_out_mode = p.readUint8()
        if trans_out_mode != 0:
             trans_out_duration = p.readFloat()

        line = BUILD_LINE(
            prefix,
            "USE CAMERA",
            f"{(cam_ref)}, transition in {(trans_in_mode)} for {(trans_in_duration)} seconds, transition out {(trans_out_mode)} for {(trans_out_duration) if trans_out_mode != 0 else 'N/A'} seconds",
        )