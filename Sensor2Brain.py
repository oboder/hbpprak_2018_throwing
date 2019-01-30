# Imported Python Transfer Function
import numpy as np
import cv2
@nrp.MapSpikeSource("cylinder_x", nrp.brain.sensors[0], nrp.dc_source)
@nrp.MapSpikeSource("cylinder_y", nrp.brain.sensors[1], nrp.dc_source)
@nrp.MapSpikeSource("cylinder_z", nrp.brain.sensors[2], nrp.dc_source)
@nrp.Robot2Neuron()
def Sensor2Brain (t, cylinder_x, cylinder_y, cylinder_z):
    from rospy import ServiceProxy
    from gazebo_msgs.srv import GetModelState
    model_name = 'cylinder'
    state_proxy = ServiceProxy('/gazebo/get_model_state',
                                    GetModelState, persistent=False)
    cylinder_state = state_proxy(model_name, "world")
    if cylinder_state.success:
        current_position = cylinder_state.pose.position
        cylinder_x.voltage = np.abs(current_position.x) * (np.random.rand() - 1) * 2
        cylinder_y.voltage = np.abs(current_position.y) * (np.random.rand() - 1) * 2
        cylinder_z.voltage = np.abs(current_position.z) * (np.random.rand() - 1) * 2
        #clientLogger.info(current_position.x, current_position.y, current_position.z)
        #clientLogger.info(cylinder_x.voltage, cylinder_y.voltage, cylinder_z.voltage)
