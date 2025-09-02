import time
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key


class PynputMouseController:
    def __init__(self):
        self.mouse = MouseController()
        self.keyboard = KeyboardController()

    def get_mouse_position(self):
        """获取当前鼠标位置。"""
        x, y = self.mouse.position
        return {"x": int(x), "y": int(y)}

    def move_mouse(self, x:int, y:int):
        """将鼠标移动到指定位置。"""
        self.mouse.move(x, y)

    def click_mouse(self, button: str):
        """点击鼠标按钮。"""
        if button == "left click":
            self.mouse.click(Button.left)
        elif button == "right click":
            self.mouse.click(Button.right)
        elif button == "middle click":
            self.mouse.click(Button.middle)
        else:
            raise ValueError("Unsupported button type. Use 'left', 'right', or 'middle'.")
    
    def type_text(self, text: str, interval: float = 0.05):
        """
        模拟键盘输入文本。
        
        :param text: 要输入的文本
        :param interval: 字符之间的间隔时间（秒），默认0.05秒
        """
        for char in text:
            self.keyboard.type(char)
            time.sleep(interval)
    def press_key(self, key: str):
        special_keys = {
            'backspace': Key.backspace,
            'enter': Key.enter,
            'tab': Key.tab,
            'space': Key.space,
            'shift': Key.shift,
            'ctrl': Key.ctrl,
            'alt': Key.alt,
            'esc': Key.esc,
            'delete': Key.delete,
            # 可以添加更多特殊键映射...
        }
        # 转换为小写以便比较
        key_lower = key.lower()

        if key_lower in special_keys:
            # 按下并释放特殊键
            self.keyboard.press(special_keys[key_lower])
            self.keyboard.release(special_keys[key_lower])
        else:
            # 按下并释放普通键
            self.keyboard.press(key)
            self.keyboard.release(key)
