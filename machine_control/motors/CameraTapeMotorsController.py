import RPi.GPIO as gpio


class CameraTapeMotorsController:
    INPUT_1 = 17  # Input 1 for spinning direction
    INPUT_2 = 22  # Input 2 for spinning direction
    ENA = 27  # This is for controlling speed using Pulse Width Modulation

    def __init__(self):
        self.initialized = False

    """
    IN1 IN2 Spinning direction
     F   F      MOTOR OFF
     T   F       FORWARD
     F   T       BACKWARD
     F   F      MOTOR OFF
    """

    def setup(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(self.INPUT_1, gpio.OUT)
        gpio.setup(self.INPUT_2, gpio.OUT)
        gpio.setup(self.ENA, gpio.OUT)
        self.initialized = True

    def run(self, forward: bool = True, hz: int = 100, duty_cycle: int = 50):
        if self.initialized is False:
            self.setup()

        pwm_value = gpio.PWM(self.ENA, hz)
        pwm_value.start(duty_cycle)

        if forward:
            gpio.output(self.INPUT_1, False)
            gpio.output(self.INPUT_2, True)
        else:
            gpio.output(self.INPUT_1, True)
            gpio.output(self.INPUT_2, False)

    # def run_with_speed(self, hz: int = 100, duty_cycle: int = 50):
    #     pwm_value = gpio.PWM(self.ENA, hz)
    #     pwm_value.start(duty_cycle)

    def stop(self):
        gpio.cleanup()
        self.initialized = False
