import RPi.GPIO as gpio


class SplittingConveyorController:
    DEFAULT_FREQUENCY = 20

    INPUT_1 = 23  # Input 1 for spinning direction
    INPUT_2 = 24  # Input 2 for spinning direction
    ENA = 25  # This is for controlling speed using Pulse Width Modulation

    def __init__(self):
        self.initialized = False
        self.pwm = None

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

        self.pwm = gpio.PWM(self.ENA, self.DEFAULT_FREQUENCY)
        self.initialized = True

    def run(self, forward: bool = False, hz: int = DEFAULT_FREQUENCY, duty_cycle: int = 40):
        if self.initialized is False:
            self.setup()

        self.pwm.ChangeFrequency(hz)
        self.pwm.start(duty_cycle)

        if forward:
            gpio.output(self.INPUT_1, True)
            gpio.output(self.INPUT_2, False)
        else:
            gpio.output(self.INPUT_1, False)
            gpio.output(self.INPUT_2, True)

    # def run_with_speed(self, hz: int = 100, duty_cycle: int = 50):
    #     pwm_value = gpio.PWM(self.ENA, hz)
    #     pwm_value.start(duty_cycle)

    def stop(self):
        if self.pwm is not None:
            self.pwm.stop()

        gpio.cleanup([self.INPUT_1, self.INPUT_2, self.ENA])
        self.initialized = False
