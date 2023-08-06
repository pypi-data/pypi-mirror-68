"""Use this script to initialise and call the auxiliary classes."""

from simses.commons.utils.max_peak_shaving_limit import MaxPeakShavingLimit

# Example:
scaling_factor = 1
path = "C:/Users/Collath/Documents/GitHub/SimSES/simses/commons/profile/technical_profile/data/CHP_Batt_analysis/SBAP_med_2_25GWh_300s.csv"
random_profile = False
limitfinder = MaxPeakShavingLimit(1370e3, 1e6, 0.9, 300, random_profile, path, scaling_factor)
limitfinder.calc_max_peak(20)