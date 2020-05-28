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

    @classmethod
    def get_dependents(cls, param, mode):
        if mode == OpModEnum.vcv.value:
            if param.name in (ParamEnum.tvm.name, ParamEnum.ier_i.name, ParamEnum.ier_e.name, ParamEnum.brpm.name):
                return [ParamEnum.mf.name]
            elif param.name == ParamEnum.mf.name:
                return [ParamEnum.tvm.name]
        return []

    @classmethod
    def set(cls, param, value, params):
        param.value = value
        mode = params[ParamEnum.mode.name].value
        if mode == OpModEnum.vcv.value:
            ier_i = params[ParamEnum.ier_i.name].value
            ier_e = params[ParamEnum.ier_e.name].value
            brt = 60 / params[ParamEnum.brpm.name].value
            ier = ier_i / ier_e
            if param.name in (ParamEnum.tvm.name, ParamEnum.ier_i.name, ParamEnum.ier_e.name, ParamEnum.brpm.name):
                tvm = params[ParamEnum.tvm.name].value
                mf = tvm * (1 + ier) / (ier * brt)
                params[ParamEnum.mf.name].value = mf*60/1000
            elif param.name == ParamEnum.mf.name:
                mf = params[ParamEnum.mf.name].value*1000/60
                params[ParamEnum.tvm.name].value = mf * ier * brt / (1 + ier)


class OpMode:
    def __init__(self, name):
        self.name = name
