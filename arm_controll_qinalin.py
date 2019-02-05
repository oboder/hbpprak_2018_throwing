# Imported Python Transfer Function
import numpy as np
approach_conf = np.array([-0.5178, -0.9, 1.1781, -0.0345, -0.6, 0.0])
grasp_conf = np.array([-0.58, -0.9, 1.1781, -0.0345, -0.6, 0.0])
throw_conf = np.array([0, 1, 0, -0.0345, -0.6, 0.0])
prepare_throw_conf = np.array([0, 1.25, 1.1781, -0.0345, -0.6, 1.5])
again_prepare_throw_conf = np.array([0, 1.0, -2, -0.0, 1.6, 1.5])
# throw_conf = np.array([0, -1.0, 3, -0.0, -2,1.5])
# config_best
# throw_conf = np.array([-0.5178, 1.0, -1.1781, 0.0345, 0.6, 0.0])
# throw_conf = np.array([0, 0, 0, 0, 0, 0])
reset_conf = np.zeros(6)
# reset_conf = np.array([0, 0, 0, 0, 0, 1.0])
@nrp.MapRobotPublisher("topic_arm_1", Topic('/robot/arm_1_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_arm_2", Topic('/robot/arm_2_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_arm_3", Topic('/robot/arm_3_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_arm_4", Topic('/robot/arm_4_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_arm_5", Topic('/robot/arm_5_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_arm_6", Topic('/robot/arm_6_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotSubscriber('command', Topic('/arm_robot/arm_commands', std_msgs.msg.String))
@nrp.MapVariable("last_command_executed", initial_value=None)
@nrp.MapVariable("approach_conf", initial_value=approach_conf)
@nrp.MapVariable("grasp_conf", initial_value=grasp_conf)
@nrp.MapVariable("prepare_throw_conf", initial_value=prepare_throw_conf)
@nrp.MapVariable("again_prepare_throw_conf", initial_value=again_prepare_throw_conf)
@nrp.MapVariable("throw_conf", initial_value=throw_conf)
@nrp.MapVariable("reset_conf", initial_value=reset_conf)
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
@nrp.Neuron2Robot()
def arm_controll_qinalin(t,
                         command, last_command_executed,
                         approach_conf,
                         grasp_conf,
                         prepare_throw_conf,
                         again_prepare_throw_conf,
                         throw_conf,
                         reset_conf,
                         topic_arm_1, topic_arm_2,
                         topic_arm_3, topic_arm_4,
                         topic_arm_5, topic_arm_6,
                         arm_1_forward_neuron, arm_1_back_neuron,
                         arm_2_forward_neuron, arm_2_back_neuron,
                         arm_3_forward_neuron, arm_3_back_neuron,
                         arm_4_forward_neuron, arm_4_back_neuron,
                         arm_5_forward_neuron, arm_5_back_neuron,
                         arm_6_forward_neuron, arm_6_back_neuron):
    def send_joint_config(topics_list, config_list):
        for topic, value in zip(topics_list, config_list):
            topic.send_message(std_msgs.msg.Float64(value))
    def get_throw_config(neurons_arm):
        # arm_1_position = 2*(arm_1_forward_neuron.rate - arm_1_back_neuron.rate)
        # arm_2_position = 2*(arm_2_forward_neuron.rate - arm_2_back_neuron.rate)
        # arm_3_position = 2*(arm_3_forward_neuron.rate - arm_3_back_neuron.rate)
        # arm_4_position = 2*(arm_4_forward_neuron.rate - arm_4_back_neuron.rate)
        # arm_5_position = 2*(arm_5_forward_neuron.rate - arm_5_back_neuron.rate)
        # arm_6_position = 2*(arm_6_forward_neuron.rate - arm_6_back_neuron.rate)
        # if (arm_1_position != 0.0):
        #    clientLogger.info(arm_1_position, arm_2_position, arm_3_position, arm_4_position, arm_5_position, arm_6_position)
        # topic_arm_1.send_message(std_msgs.msg.Float64(arm_1_position))
        # topic_arm_2.send_message(std_msgs.msg.Float64(arm_2_position))
        # topic_arm_3.send_message(std_msgs.msg.Float64(arm_3_position))
        # topic_arm_4.send_message(std_msgs.msg.Float64(arm_4_position))
        # topic_arm_5.send_message(std_msgs.msg.Float64(arm_5_position))
        # topic_arm_6.send_message(std_msgs.msg.Float64(arm_6_position))
        return [neuron.rate for neuron in neurons_arm]
    import collections
    if command.value is None:
        return
    else:
        command_str = command.value.data
    if command_str == last_command_executed.value:
        return
    # clientLogger.info("ARM received:{}".format(command_str))
    # if (command_str == "THROW"):
    #     return
    topics_arm = [topic_arm_1, topic_arm_2,
                  topic_arm_3, topic_arm_4, topic_arm_5, topic_arm_6]
    neurons_arm = [arm_1_forward_neuron, arm_2_forward_neuron, arm_3_forward_neuron, arm_4_forward_neuron,
                  arm_5_forward_neuron, arm_6_forward_neuron]
    commands_confs = collections.defaultdict(None, {
        "APPROACH": approach_conf.value,
        "GRASP": grasp_conf.value,
        "PTHROW": prepare_throw_conf.value,
        "APTHROW": again_prepare_throw_conf.value,
        "THROW": throw_conf.value,
        "RESET": reset_conf.value
    }
                                             )
    split_command = command_str.split('_')
    action = split_command[0]
    new_config = commands_confs[action]
    clientLogger.info('actioN ' + action)
    if action == 'THROW':
        new_config = get_throw_config(neurons_arm)
        clientLogger.info(new_config)
    if new_config is not None:
        last_command_executed.value = command_str
        send_joint_config(topics_arm, new_config)
