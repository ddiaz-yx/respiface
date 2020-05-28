from enum import Enum, auto


class ParamEnum(Enum):
    """
    Los nombres deben coincidir con los del archivo de configuración.
    """
    tvm = auto()  # Volumen Tidal
    brpm = auto()  # Respiraciones por minuto
    ier = auto()  # Ratio I:E
    ier_i = auto()  # I del Ratio I:E
    ier_e = auto()  # E del Ratio I:E
    fio2 = auto()  # FiO2
    gscale = auto()  # Escala de tiempo del gráfico
    mf = auto()  # Flujo max
    peep = auto()  # PEEP
    ast = auto()  # Alarm silence time
    mode = auto()  # Modo de operación


class OpModEnum(Enum):
    pcv = 0
    vcv = 1


PLOT_TIME_SCALES = [5, 20, 60]


class Parameter:

    def __init__(self, name: str = "", screen_name="", units="", min_=None, max_=None, default=None, step=None, adjustable: bool = True, fmt=".1f", measured=False):
        self.name = name
        self.screen_name = screen_name
        self.units = units
        self.value_format = fmt
        self.value_step = step
        self.value_max = max_
        self.value_min = min_
        self.value_default = default
        self.value_as_index = False  #If true, the value is the index of Parameter.options
        self.adjustable = adjustable
        self.value = 0
        self.options = ()
        self.measured = measured


class OpMode:
    def __init__(self, name):
        self.name = name
