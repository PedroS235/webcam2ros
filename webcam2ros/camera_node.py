import rclpy
from rclpy.node import Node
import cv2
import cv_bridge
from sensor_msgs.msg import Image


class CameraNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.publisher = self.create_publisher(Image, "camera/image_raw", 10)
        self.bridge = cv_bridge.CvBridge()
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.create_timer(0.01, self.read_frame)

    def read_frame(self):
        _, frame = self.camera.read()
        image = self.bridge.cv2_to_imgmsg(frame, "bgr8")
        image.header.stamp = self.get_clock().now().to_msg()
        self.publisher.publish(image)


def main(args=None):
    rclpy.init(args=args)
    node = CameraNode("camera_node")
    rclpy.spin(node)
    rclpy.shutdown()
