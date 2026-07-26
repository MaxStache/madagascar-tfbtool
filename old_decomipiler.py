# use camera::op-code
cam_ref = p.readRef()
trans_in_mode = p.readUint8()
trans_in_duration = p.readFloat()
trans_out_mode = p.readUint8()
if trans_out_mode != 0:
     trans_out_duration = p.readFloat()

_ = (
    "USE CAMERA",
    f"{(cam_ref)}, transition in {(trans_in_mode)} for {(trans_in_duration)} seconds, transition out {(trans_out_mode)} for {(trans_out_duration) if trans_out_mode != 0 else 'N/A'} seconds",
)