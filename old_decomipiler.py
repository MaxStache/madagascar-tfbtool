# use camera::op-code


cam_ref = p.readRef()  # type: ignore  # noqa: F821

trans_in_mode = CamTransitionInMode(p.readUint8())  # type: ignore # noqa: F821
trans_in_duration = p.readFloat()  # type: ignore # noqa: F821

trans_out_mode = CamTransitionOutMode(p.readUint8())  # type: ignore # noqa: F821

trans_out_duration = 0.0
if trans_out_mode != CamTransitionOutMode.no_transition:
    trans_out_duration = p.readFloat()  # type: ignore # noqa: F821


# cam_ref, transition in trans_in_mode
# for trans_in_duration seconds,
# transition out trans_out_mode for
# trans_out_duration seconds",
