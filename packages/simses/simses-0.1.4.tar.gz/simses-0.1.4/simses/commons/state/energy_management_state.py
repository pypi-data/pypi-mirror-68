from simses.commons.state.state import State


class EnergyManagementState(State):
    """
    Current State of the Energy Management (PV, Load, etc..)
    """

    LOAD_POWER = 'Load in W'
    PV_POWER = 'PV Generation in W'
    FCR_MAX_POWER = 'Power reserved for FCR in W'
    IDM_POWER = 'Power delivered for IDM in W'
    SOC_OVERSHOOT = 'SOC over target in p.u.'
    FORECAST_ERROR_SIGMA = 'Rolling standard deviation of load forecasting error in W'
    FORECAST_ERROR_MU = 'Rolling expected value of load forecasting error in W'

    def __init__(self):
        super().__init__()
        self._initialize()

    @property
    def load_power(self) -> float:
        return self.get(self.LOAD_POWER)

    @load_power.setter
    def load_power(self, value: float) -> None:
        self.set(self.LOAD_POWER, value)

    @property
    def pv_power(self) -> float:
        return self.get(self.PV_POWER)

    @pv_power.setter
    def pv_power(self, value: float) -> None:
        self.set(self.PV_POWER, value)

    @property
    def fcr_max_power(self) -> float:
        return self.get(self.FCR_MAX_POWER)

    @fcr_max_power.setter
    def fcr_max_power(self, value: float) -> None:
        self.set(self.FCR_MAX_POWER, value)

    @property
    def idm_power(self) -> float:
        return self.get(self.IDM_POWER)

    @idm_power.setter
    def idm_power(self, value: float) -> None:
        self.set(self.IDM_POWER, value)

    @property
    def soc_overshoot(self) -> float:
        return self.get(self.SOC_OVERSHOOT)

    @soc_overshoot.setter
    def soc_overshoot(self, value: float) -> None:
        self.set(self.SOC_OVERSHOOT, value)

    @property
    def forecast_error_sigma(self) -> float:
        return self.get(self.FORECAST_ERROR_SIGMA)

    @forecast_error_sigma.setter
    def forecast_error_sigma(self, value: float) -> None:
        self.set(self.FORECAST_ERROR_SIGMA, value)

    @property
    def forecast_error_mu(self) -> float:
        return self.get(self.FORECAST_ERROR_MU)

    @forecast_error_mu.setter
    def forecast_error_mu(self, value: float) -> None:
        self.set(self.FORECAST_ERROR_MU, value)



    @property
    def id(self) -> str:
        return 'EMS'

    @classmethod
    def sum_parallel(cls, system_states: []):
        raise Exception('sum_parallel is not implemented for EnergyManagementState')

    @classmethod
    def sum_serial(cls, states: []):
        raise Exception('sum_serial is not implemented for EnergyManagementState')
