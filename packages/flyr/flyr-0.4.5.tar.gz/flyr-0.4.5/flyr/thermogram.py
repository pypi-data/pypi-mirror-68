from math import sqrt, exp, fsum

import numpy as np
from nptyping import Array


class FlyrThermogram:
    optical = None  # Optional[Array[int, ..., ..., 3]]
    raw_data = None  # Optional[Array[int, ..., ..., ...]]
    camera_info = None  # Optional[Dict[str, Any]]

    _kelvin = None  # Optional[Array[float, ..., ...]]
    _celsius = None  # Optional[Array[float, ..., ...]]

    @property
    def kelvin(self):
        if self._kelvin is None:
            self._kelvin = self.raw_to_kelvin(**self.camera_info)
        return self._kelvin

    @property
    def celsius(self):
        if self._celsius is None:
            self._celsius = self.kelvin - 273.15
        return self._celsius

    def raw_to_kelvin(
        self,
        emissivity: float = 1.0,
        object_distance: float = 1.0,
        atmospheric_temperature: float = 293.15,
        ir_window_temperature: float = 293.15,
        ir_window_transmission: float = 1.0,
        reflected_apparent_temperature: float = 293.15,
        relative_humidity: float = 0.5,
        planck_r1: float = 21106.77,
        planck_r2: float = 0.012545258,
        planck_b: float = 1501.0,
        planck_f: int = 1,
        planck_o: int = -7340,
    ) -> Array[float, ..., ...]:
        """ Use the details camera info metadata to translate the raw
            temperatures to °Kelvin.

            The method is expected to be called with the `camera_info` object
            variable as its key words arguments, e.g.
            `raw_to_kelvin(**self.camera_info)`. Missing values are filled with
            the parameters' default values.

            Parameters
            ----------
            emissivity : float
            object_distance : float
                Unit is meters
            atmospheric_temperature : float
                Unit is Kelvin
            ir_window_temperature : float
                Unit is Kelvin
            ir_window_transmission : float
                Unit is Kelvin
            reflected_apparent_temperature : float
                Unit is Kelvin
            relative_humidity : float
                Value in 0 and 1
            planck_r1 : float
            planck_r2 : float
            planck_b : float
            planck_f : float
            planck_o : int

            Returns
            -------
            Array[float, ..., ...]
                An array of float values with the °C unit
        """
        # Constants
        # TODO? Verify these values are constants. They are different in the
        # file flir_e53_1.jpg for example.
        ATA1 = 0.006569   # atmospheric transmission alpha 1
        ATA2 = 0.01262    # atmospheric transmission alpha 2
        ATB1 = -0.002276  # atmospheric transmission beta 1
        ATB2 = -0.00667   # atmospheric transmission beta 2
        ATX = 1.9         # atmospheric transmission x

        # Transmission through window (calibrated)
        emiss_wind = 1 - ir_window_transmission
        refl_wind = 0

        # Transmission through the air
        h2o = relative_humidity * exp(
            1.5587
            + 0.06939 * (atmospheric_temperature - 273.15)
            - 0.00027816 * (atmospheric_temperature - 273.17) ** 2
            + 0.00000068455 * (atmospheric_temperature - 273.15) ** 3
        )

        term1 = exp(-sqrt(object_distance / 2) * (ATA1 + ATB1 * sqrt(h2o)))
        term2 = exp(-sqrt(object_distance / 2) * (ATA2 + ATB2 * sqrt(h2o)))
        tau1 = ATX * term1 + (1 - ATX) * term2
        tau2 = ATX * term1 + (1 - ATX) * term2

        # Radiance from the environment
        def plancked(t):
            planck_tmp = planck_r2 * (exp(planck_b / t) - planck_f)
            return planck_r1 / planck_tmp - planck_o

        raw_refl1 = plancked(reflected_apparent_temperature)
        raw_refl1_attn = (1 - emissivity) / emissivity * raw_refl1

        raw_atm1 = plancked(atmospheric_temperature)
        raw_atm1_attn = (1 - tau1) / emissivity / tau1 * raw_atm1

        term3 = emissivity * tau1 * ir_window_transmission
        raw_wind = plancked(ir_window_temperature)
        raw_wind_attn = emiss_wind / term3 * raw_wind

        raw_refl2 = plancked(reflected_apparent_temperature)
        raw_refl2_attn = refl_wind / term3 * raw_refl2

        raw_atm2 = plancked(atmospheric_temperature)
        raw_atm2_attn = (1 - tau2) / term3 / tau2 * raw_atm2

        subtraction = fsum(
            [
                raw_atm1_attn,
                raw_atm2_attn,
                raw_wind_attn,
                raw_refl1_attn,
                raw_refl2_attn,
            ]
        )

        raw_obj = self.raw_data.astype(float)
        raw_obj /= emissivity * tau1 * ir_window_transmission * tau2
        raw_obj -= subtraction

        # Temperature from radiance
        raw_obj += planck_o
        raw_obj *= planck_r2
        planck_term = planck_r1 / raw_obj + planck_f
        return planck_b / np.log(planck_term)
