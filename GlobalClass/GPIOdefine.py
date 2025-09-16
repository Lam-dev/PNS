import enum

class GPIOdefine(enum.Enum):
    SimReset        = 13          # reset module sim
    SimPowerOn      = 22        # Bat nguon sim     
    ModulePowerOn   = 26     # bat nguon module sim
    EncoderIn       = 6       # Tin hieu xung tu encoder
    LedRedPWM       = 22   # pwm dieu khien led do
    LedGreen        = 10   # led xanh
    RFcardPower     = 23   # nguon rf card
    PowerControl    = 4
    ScreenPower     = 1
    CameraPower     = 0
    PowerButton     = 11

