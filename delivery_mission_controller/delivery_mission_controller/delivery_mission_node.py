import time
import rclpy
from rclpy.action import ActionServer, CancelResponse
from rclpy.node import Node
from geometry_msgs.msg import Twist
from delivery_mission_interfaces.action import DeliveryMission

class DeliveryMissionController(Node):
    def __init__(self):
        super().__init__('delivery_mission_node')
        
        # Publisher for velocity commands
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Action Server
        self._action_server = ActionServer(
            self,
            DeliveryMission,
            'delivery_mission',
            execute_callback=self.execute_callback,
            cancel_callback=self.cancel_callback
        )
        self.get_logger().info('Delivery Mission Controller is ready.')

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Received cancel request. Stopping robot...')
        self.stop_robot()
        return CancelResponse.ACCEPT

    def stop_robot(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.cmd_vel_pub.publish(msg)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing delivery mission...')
        goal = goal_handle.request
        feedback = DeliveryMission.Feedback()
        result = DeliveryMission.Result()
        
        start_time = time.time()
        simulate_pickup_duration = 3.0 # Defined fixed duration for Phase 2
        total_mission_time = goal.pickup_duration + simulate_pickup_duration + goal.delivery_duration

        # --- Phase 1: Drive to pickup ---
        self.get_logger().info(f'Phase 1: Driving to pickup for {goal.pickup_duration}s at {goal.speed}m/s')
        vel_msg = Twist()
        vel_msg.linear.x = float(goal.speed)
        
        phase1_start = time.time()
        while time.time() - phase1_start < goal.pickup_duration:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.stop_robot()
                result.success = False
                result.message = "Mission canceled during Phase 1."
                return result
            
            if time.time() - start_time > goal.timeout:
                goal_handle.abort()
                self.stop_robot()
                result.success = False
                result.message = "Mission aborted: Timeout exceeded."
                return result

            self.cmd_vel_pub.publish(vel_msg)
            feedback.remaining_time = total_mission_time - (time.time() - start_time)
            feedback.pickup_progress = 0.0
            goal_handle.publish_feedback(feedback)
            time.sleep(0.1)

        # --- Phase 2: Simulate Pickup ---
        self.get_logger().info('Phase 2: Stopping for pickup simulation.')
        self.stop_robot()
        
        phase2_start = time.time()
        while time.time() - phase2_start < simulate_pickup_duration:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.success = False
                result.message = "Mission canceled during Phase 2."
                return result
                
            if time.time() - start_time > goal.timeout:
                goal_handle.abort()
                result.success = False
                result.message = "Mission aborted: Timeout exceeded."
                return result

            elapsed_phase2 = time.time() - phase2_start
            feedback.remaining_time = total_mission_time - (time.time() - start_time)
            feedback.pickup_progress = (elapsed_phase2 / simulate_pickup_duration) * 100.0
            goal_handle.publish_feedback(feedback)
            time.sleep(0.1)

        # --- Phase 3: Drive to delivery ---
        self.get_logger().info(f'Phase 3: Driving to delivery for {goal.delivery_duration}s')
        
        phase3_start = time.time()
        while time.time() - phase3_start < goal.delivery_duration:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.stop_robot()
                result.success = False
                result.message = "Mission canceled during Phase 3."
                return result
                
            if time.time() - start_time > goal.timeout:
                goal_handle.abort()
                self.stop_robot()
                result.success = False
                result.message = "Mission aborted: Timeout exceeded."
                return result

            self.cmd_vel_pub.publish(vel_msg)
            feedback.remaining_time = total_mission_time - (time.time() - start_time)
            feedback.pickup_progress = 100.0
            goal_handle.publish_feedback(feedback)
            time.sleep(0.1)

        # --- Mission Complete ---
        self.stop_robot()
        goal_handle.succeed()
        self.get_logger().info('Mission Completed Successfully!')
        
        result.success = True
        result.message = "Delivery mission executed successfully."
        return result

def main(args=None):
    rclpy.init(args=args)
    node = DeliveryMissionController()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()