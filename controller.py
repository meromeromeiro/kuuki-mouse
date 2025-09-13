import time
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key


class PynputMouseKeyboardController(MouseController, KeyboardController):
    special_keys = {
        "backspace": Key.backspace,
        "enter": Key.enter,
        "tab": Key.tab,
        "space": Key.space,
        "shift": Key.shift,
        "ctrl": Key.ctrl,
        "alt": Key.alt,
        "esc": Key.esc,
        "delete": Key.delete,
        # 可以添加更多特殊键映射...
    }
    mouse_buttons = {
        "left": Button.left,
        "right": Button.right,
        "middle": Button.middle,
        # 兼容性
        "left click": Button.left,
        "right click": Button.right,
        "middle click": Button.middle,
    }

    def __init__(self):
        self.mouse = MouseController()
        self.keyboard = KeyboardController()

    def get_mouse_position(self):
        """获取当前鼠标位置。"""
        x, y = self.mouse.position
        return {"x": int(x), "y": int(y)}

    def move_mouse(self, x: int, y: int):
        """将鼠标移动到指定位置。"""
        self.mouse.move(x, y)

    def click_mouse(self, button: str):
        """点击鼠标按钮。"""
        button = PynputMouseKeyboardController.mouse_buttons.get(button)
        if button:
            self.mouse.click(button)
        else:
            raise ValueError(
                "Unsupported button type. Use 'left', 'right', or 'middle'."
            )

    def type_text(self, text: str, interval: float = 0.05):
        """
        模拟键盘输入文本。

        :param text: 要输入的文本
        :param interval: 字符之间的间隔时间（秒），默认0.05秒
        """
        for char in text:
            self.keyboard.type(char)
            time.sleep(interval)

    def tap_key(self, key: str):
        # 转换为小写以便比较
        key = PynputMouseKeyboardController.special_keys.get(key.lower(), key.lower())
        self.keyboard.tap(key)

    def key_down(self, key: str):
        key = PynputMouseKeyboardController.special_keys.get(key.lower(), key.lower())
        self.keyboard.press( key)

    def key_up(self, key: str):
        key = PynputMouseKeyboardController.special_keys.get(key.lower(), key.lower())
        self.keyboard.release(key)


if __name__ == "__main__":
    c = PynputMouseKeyboardController()
    c.type_text("bbb")
