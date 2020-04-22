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
    flujoaire = auto()  # Flujo de aire
    peep = auto()  # PEEP
    ast = auto()  # Alarm silence time
    mode = auto()  # Modo de operación


class Parameter:
    def __init__(self, name: str = "", screen_name="", units="", min_=None, max_=None, default=None, step=None, adjustable: bool = True, fmt=".1f"):
        self.name = name
        self.screen_name = screen_name
        self.units = units
        self.value_format = fmt
        self.value_step = step
        self.value_max = max_
        self.value_min = min_
        self.value_default = default
        self.adjustable = adjustable
        self.value = 0
        if name == ParamEnum.ier.name:
            self.value = (0, 0)
