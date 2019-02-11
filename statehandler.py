# Imported Python Transfer Function
from std_msgs.msg import String


@nrp.MapVariable("last_command", initial_value=None)
@nrp.MapVariable("destination_time", initial_value=None)
@nrp.MapRobotSubscriber('reset_command', Topic('/arm_robot/reset_command', std_msgs.msg.Bool))
def statehandler(t, last_command, destination_time, reset_command):
    command = None
    if destination_time.value is None:
        destination_time.value = t
    import rospy
    time = destination_time.value
    arm_state = rospy.Publisher(
        '/arm_robot/arm_commands', String, latch=True, queue_size=10)
    hand_state = rospy.Publisher(
        '/arm_robot/hand_commands', String, latch=True, queue_size=10)
    last = last_command.value
    # clientLogger.info(reset_command.value)
    if reset_command.value and reset_command.value.data is True:
        clientLogger.info('I like to reset')
        time = t + 2.
        command = 'APPROACH'
        arm_state.publish(command)
        reset_state = rospy.Publisher(
            '/arm_robot/reset_command', std_msgs.msg.Bool, latch=True, queue_size=10)
        reset_state.publish(False)
    if last == 'APPROACH' and time <= t:
        time = t + 2.
        command = 'GRASP'
        arm_state.publish(command)
    elif last == 'GRASP' and time <= t:
        time = t + 2.
        command = 'HAND_GRASP'
        hand_state.publish('GRASP')
    elif last == 'HAND_GRASP' and time <= t:
        time = t + 2.
        command = 'PTHROW'
        arm_state.publish(command)
    elif last == 'PTHROW' and time <= t:
        time = t + 3.
        command = 'APTHROW'
        arm_state.publish(command)
    elif last == 'APTHROW' and time <= t:
        time = t + 2.
        command = 'THROW'
        arm_state.publish(command)
    elif last == 'THROW' and time <= t:
        time = t + 2.
        command = 'RESET'
        arm_state.publish(command)
    elif last == 'RESET' and time <= t:
        time = t + 2.
        command = 'DONE'
        arm_state.publish(command)
    # else:
    # command = last_command.value
    destination_time.value = time
    # clientLogger.info(t, time, last)
    if command is not None:
        last_command.value = command
