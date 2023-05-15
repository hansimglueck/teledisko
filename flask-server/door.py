from gpiozero import Button

class Door:
    def __init__(self):

        self.button = Button(21)

    def wait_for_openening(self):
        self.button.wait_for_press()
        print("door closed")
        self.button.wait_for_release()
        print("door open")

    def wait_for_closing(self):
        self.button.wait_for_release()
        print("door open")
        self.button.wait_for_press()
        print("door closed")
