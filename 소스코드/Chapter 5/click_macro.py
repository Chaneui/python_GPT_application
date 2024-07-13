import sys
import time
from pynput import keyboard, mouse

class ClickMacro:
    def __init__(self):
        self.click_speed = 1
        self.click_number = 0
        self.click_count = 0
        self.click_position = (0, 0)
        self.running = False

        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.start()

        self.mouse_controller = mouse.Controller()

        print("클릭 매크로가 실행됩니다. F5를 눌러 클릭 좌표를 설정하시요, F6를 누르면 시작됩니다.")

    def on_press(self, key):
        try:
            if key == keyboard.Key.f5:
                self.click_position = self.mouse_controller.position
                print(f"클릭 좌표 설정 완료: {self.click_position}")
            elif key == keyboard.Key.f6:
                self.start_macro()
        except AttributeError:
            pass

    def start_macro(self):
        try:
            self.click_speed = float(input("초당 클릭 횟수 설정: "))
            self.click_number = int(input("총 클릭 횟수 설정: "))
        except ValueError:
            print("잘못된 수치를 입력했습니다")
            return
        
        self.click_count = 0
        self.running = True

        self.run_macro()

    def run_macro(self):
        for i in range(self.click_number):
            if not self.running:
                break
            self.mouse_controller.position = self.click_position
            self.mouse_controller.click(mouse.Button.left, 1)
            self.click_count += 1
            print(f"클릭 횟수: {self.click_count}")
            time.sleep(1 / self.click_speed)
        print("총 클릭 횟수 도달, 클릭 종료")

if __name__ == "__main__":
    click_macro = ClickMacro()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("프로그램이 종료됩니다.")