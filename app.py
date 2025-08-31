import asyncio
import time

# from grpc_remote_control.controller import GrpcController
from controller import PynputMouseController

# from model import get_gravity_float, to_tensor, process_tensor

# from server import main


class App(PynputMouseController):
    def __init__(
        self,
        sensitivity: float = 300,
        attenuation_coefficient: float = 1,
        scale: float = 0.1,
    ):
        super().__init__()
        self.sensitivity = sensitivity
        self.scale = scale
        self.attenuation_coefficient = attenuation_coefficient

        self._last_data_timestamp = 0
        self._x = 0  # previous status
        self._y = 0  # previous status
        self._z = 0  # previous status
        self._alpha = 0  # previous status
        self._beta = 0  # previous status
        self._gamma = 0  # previous status
        self._last_acc_timestamp = 0

        self.v_x = 0  # 横轴上的速度
        self.v_y = 0  # 纵轴上的速度

    def update_data(
        self, x: float, y: float, z: float, alpha: float, beta: float, gamma: float
    ):
        data_timestamp = time.time()
        time_diff = data_timestamp - self._last_data_timestamp
        # a = to_tensor(x,y,z)
        # g = get_gravity_float(beta, gamma)
        # a_dash = a - g

        # # 需要：（用不了，飘逸太严重了。）
        # # 1.忽略<0.15的部分，这个是精度误差。
        # a_dash_dash = process_tensor(a_dash,.5)
        # # print(a_dash_dash[1].item(), time_diff, self.sensitivity)
        # # 2.测得的是这段时间内的平均加速度，因此需要乘以时间间隔得到速度。
        # self.v_x += a_dash_dash[0].item()*self.sensitivity
        # self.v_y += a_dash_dash[1].item()*self.sensitivity
        # # 3.速度应该有衰减系数。
        # self.v_x *= self.attenuation_coefficient
        # self.v_y *= self.attenuation_coefficient

        delta_x = alpha - self._alpha
        if delta_x < -300:
            delta_x += 360
        if delta_x > 300:
            delta_x -= 360
        delta_y = beta - self._beta    
        
        self.v_x = delta_x * self.sensitivity
        self.v_y = delta_y * self.sensitivity
        

        # print(self.v_x,a_dash_dash[0].item(), time_diff, self.sensitivity)
        # # print(self.v_x, self.v_y)

        # 参考https://github.com/TechTalkies/YouTube/blob/main/48%20ESP32%20Air%20Mouse/47_ESP32_AirMouse.ino
        # 直接是用

        # 善后处理
        self._x = x
        self._y = y
        self._z = z
        self._alpha = alpha
        self._beta = beta
        self._gamma = gamma
        self._last_data_timestamp = data_timestamp

    def update_mouse(self):
        # if self.v_x*self.scale > 10 or self.v_x*self.scale < -10:
        #     self.v_x = 0
        # if self.v_y*self.scale > 10 or self.v_y*self.scale < -10:
        #     self.v_y = 0
        # print((self.v_x) * self.scale, (self.v_y) * self.scale)
        self.move_mouse(-int(self.v_x * self.scale), -int(self.v_y * self.scale))


app = App()


def data_loop(x: float, y: float, z: float, alpha: float, beta: float, gamma: float):
    print(
        f"Received data: x={x:02f}, y={y:02f}, z={z:02f}, alpha={alpha:02f}, beta={beta:02f}, gamma={gamma:02f}"
    )


def get_data(x: float, y: float, z: float, alpha: float, beta: float, gamma: float):
    # data_loop(x,y,z,alpha,beta,gamma)
    app.update_data(x, y, z, alpha, beta, gamma)
    app.update_mouse()

def get_message(message: str):
    # print(f"message{message}")
    app.click_mouse(message)

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("\n服务器正在关闭。")
