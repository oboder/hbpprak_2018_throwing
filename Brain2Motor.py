# Imported Python Transfer Function
import hbp_nrp_cle.tf_framework as nrp
from hbp_nrp_cle.robotsim.RobotInterface import Topic
import gazebo_msgs.msg
@nrp.MapSpikeSink("arm_1_forward_neuron", nrp.brain.motors[0], nrp.population_rate)
@nrp.MapSpikeSink("arm_1_back_neuron", nrp.brain.motors[1], nrp.population_rate)
@nrp.MapSpikeSink("arm_2_forward_neuron", nrp.brain.motors[2], nrp.population_rate)
@nrp.MapSpikeSink("arm_2_back_neuron", nrp.brain.motors[3], nrp.population_rate)
@nrp.MapSpikeSink("arm_3_forward_neuron", nrp.brain.motors[4], nrp.population_rate)
@nrp.MapSpikeSink("arm_3_back_neuron", nrp.brain.motors[5], nrp.population_rate)
@nrp.MapSpikeSink("arm_4_forward_neuron", nrp.brain.motors[6], nrp.population_rate)
@nrp.MapSpikeSink("arm_4_back_neuron", nrp.brain.motors[7], nrp.population_rate)
@nrp.MapSpikeSink("arm_5_forward_neuron", nrp.brain.motors[8], nrp.population_rate)
@nrp.MapSpikeSink("arm_5_back_neuron", nrp.brain.motors[9], nrp.population_rate)
@nrp.MapSpikeSink("arm_6_forward_neuron", nrp.brain.motors[10], nrp.population_rate)
@nrp.MapSpikeSink("arm_6_back_neuron", nrp.brain.motors[11], nrp.population_rate)
@nrp.MapSpikeSink("hand_neuron", nrp.brain.motors[12], nrp.population_rate)
@nrp.MapRobotPublisher('arm_1', Topic('/robot/arm_1_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher('arm_2', Topic('/robot/arm_2_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher('arm_3', Topic('/robot/arm_3_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher('arm_4', Topic('/robot/arm_4_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher('arm_5', Topic('/robot/arm_5_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher('arm_6', Topic('/robot/arm_6_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotSubscriber('command', Topic('/arm_robot/arm_commands', std_msgs.msg.String))
@nrp.MapRobotPublisher('hand_command', Topic('/arm_robot/hand_commands', std_msgs.msg.String))
@nrp.Neuron2Robot()
def Brain2Motor (t, arm_1_forward_neuron, arm_1_back_neuron, arm_2_forward_neuron, arm_2_back_neuron, arm_3_forward_neuron, arm_3_back_neuron, arm_4_forward_neuron, arm_4_back_neuron, arm_5_forward_neuron, arm_5_back_neuron, arm_6_forward_neuron, arm_6_back_neuron, arm_1, arm_2, arm_3, arm_4, arm_5, arm_6, command, hand_neuron, hand_command):
    if command.value is None:
        return
    else:
        command_str = command.value.data
    #clientLogger.info("neuro received:{}".format(command_str))
    if (command_str != "THROW"):
        return
    #clientLogger.info("neural arm")
    arm_1_position = arm_1_forward_neuron.rate
    arm_2_position = arm_2_forward_neuron.rate
    arm_3_position = arm_3_forward_neuron.rate
    arm_4_position = arm_4_forward_neuron.rate
    arm_5_position = arm_5_forward_neuron.rate
    arm_6_position = arm_6_forward_neuron.rate
    hand_release = hand_neuron.rate
    #if (arm_1_position != 0.0):
        #clientLogger.info(arm_1_position, arm_2_position, arm_3_position, arm_4_position, arm_5_position, arm_6_position)
    arm_1.send_message(std_msgs.msg.Float64(arm_1_position))
    arm_2.send_message(std_msgs.msg.Float64(arm_2_position))
    arm_3.send_message(std_msgs.msg.Float64(arm_3_position))
    arm_4.send_message(std_msgs.msg.Float64(arm_4_position))
    arm_5.send_message(std_msgs.msg.Float64(arm_5_position))
    arm_6.send_message(std_msgs.msg.Float64(arm_6_position))
    if (hand_release > 10.0):
        #clientLogger.info("RELEASE HAND!!!")
        hand_command.send_message(std_msgs.msg.String('RELEASE'))
