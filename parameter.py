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
	mp = auto()  # P max
	peep = auto()  # PEEP
	ast = auto()  # Alarm silence time
	mode = auto()  # Modo de operación


class OpModEnum(Enum):
	pcv = 0
	vcv = 1


PLOT_TIME_SCALES = [5, 20, 60]


def _overlay_current_value(param_name, current_values, params):
	return params[param_name].value if param_name not in current_values else current_values[param_name]['value']


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
	def calculate_param(cls, param_name, current_values, params):
		tvm = _overlay_current_value(ParamEnum.tvm.name, current_values, params)
		brpm = _overlay_current_value(ParamEnum.brpm.name, current_values, params)
		ier_i = _overlay_current_value(ParamEnum.ier_i.name, current_values, params)
		ier_e = _overlay_current_value(ParamEnum.ier_e.name, current_values, params)
		fio2 = _overlay_current_value(ParamEnum.fio2.name, current_values, params)
		mf = _overlay_current_value(ParamEnum.mf.name, current_values, params)
		peep = _overlay_current_value(ParamEnum.peep.name, current_values, params)
		mode = _overlay_current_value(ParamEnum.mode.name, current_values, params)
		brt = 60 / brpm
		ier = ier_i / ier_e
		if mode == OpModEnum.vcv.value:
			if param_name == ParamEnum.mf.name:
				mf = tvm * (1 + ier) / (ier * brt)
				return mf * 60 / 1000
			elif param_name == ParamEnum.tvm.name:
				mf = mf * 1000 / 60
				return mf * ier * brt / (1 + ier)
		raise NotImplementedError


class OpMode:

	def __init__(self, name):
		self.name = name
		self.adjustable_params = []
