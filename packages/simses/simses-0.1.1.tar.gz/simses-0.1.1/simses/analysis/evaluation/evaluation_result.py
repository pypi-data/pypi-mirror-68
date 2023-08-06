import numpy as np

from simses.commons.utils.utils import format_float


class Description:

    class Technical:
        EFFICIENCY: str = 'Efficiency'
        MEAN_SOC: str = 'Mean soc'
        NUMBER_CHANGES_SIGNS: str = 'Number of changes of signs per day'
        RESTING_TIME_AVG: str = 'Avg. length of resting times'
        ENERGY_CHANGES_SIGN: str = 'Pos. energy between changes of sign'
        FULFILLMENT_AVG: str = 'Avg. Fulfillment Factor'
        EQUIVALENT_FULL_CYCLES: str = 'Equivalent full cycles'
        DEPTH_OF_DISCHARGE: str = 'Depth of discharges'
        REMAINING_CAPACITY: str = 'Remaining capacity'
        ENERGY_THROUGHPUT: str = 'Energy throughput'
        COULOMB_EFFICIENCY: str = 'Coulomb efficiency'
        POWER_ABOVE_PEAK_MAX: str = 'Max. grid power above peak'
        POWER_ABOVE_PEAK_AVG: str = 'Average power above peak'
        ENERGY_ABOVE_PEAK_MAX: str = 'Max. energy event above peak'
        ENERGY_ABOVE_PEAK_AVG: str = 'Average energy event above peak'
        NUMBER_ENERGY_EVENTS: str = 'Number of energy events above peak'
        PE_EFFICIENCY_DISCHARGE_MEAN: str = 'Mean power electronics efficiency discharge'
        PE_EFFICIENCY_CHARGE_MEAN: str = 'Mean power electronics efficiency charge'
        H2_PRODUCTION_EFFICIENCY_LHV: str = 'hydrogen production efficiency relative to LHV'

    class Economical:
        CASHFLOW: str = 'Cashflow each year'
        NET_PRESENT_VALUE: str = 'NPV'
        INTERNAL_RATE_OF_RETURN: str = 'IRR'
        PROFITABILITY_INDEX: str = 'Profitability Index'
        RETURN_ON_INVEST: str = 'ROI'
        LEVELIZED_COST_OF_STORAGE: str = 'Levelized Cost of Storage'
        INVESTMENT_COSTS: str = 'Investment Costs'
        DISCOUNT_RATE: str = 'Discount Rate'

        class FCR:
            PRICE_AVERAGE: str = 'Average FCR Price Each Year'
            REVENUE_YEARLY: str = 'FCR Revenue Each Year'
            POWER_BID_AVERAGE: str = 'Average FCR Power Bid Each Year'

        class Intraday:
            PRICE_AVERAGE: str = 'Average Intraday Revenue Price Each Year'
            REVENUE_YEARLY: str = 'Intraday Revenue Each Year'
            POWER_AVERAGE: str = 'Average Intraday Revenue Power Each Year'

        class SCI:
            COST_WITHOUT_STORAGE: str = 'Electricity cost each year without storage system'
            COST_WITH_STORAGE: str = 'Electricity cost each year with storage system'
            COST_ELECTRICITY: str = 'Electricity Costs'
            PV_FEED_IN_TARIFF: str = 'PV Feed In Tariff'

        class DemandCharges:
            COST_WITHOUT_STORAGE: str = 'Demand charges each year without storage system'
            COST_WITH_STORAGE: str = 'Demand charges each year with storage system'
            CYCLE: str = 'Demand Charge Billing Cycle'
            PRICE: str = 'Demand Charge Price'
            INTERVAL: str = 'Demand Charge Average Interval'


class Unit:
    NONE: str = '-'
    PERCENTAGE: str = '%'
    MINUTES: str = 'min'
    EURO: str = 'EUR'
    WATT: str = 'W'
    KILOWATT: str = 'kW'
    KWH: str = 'kWh'
    EURO_PER_KW: str = 'EUR / kW'
    EURO_PER_MWH: str = 'EUR / MWh'
    EURO_PER_KWH: str = 'EUR / kWh'
    EURO_PER_KWH_DAY: str = 'EUR / kWh / d'


class EvaluationResult:
    """Provides a structure for evaluation results in order to organize data management for printing to
    the console, exporting to csv files, etc.."""

    def __init__(self, description: str, unit: str, value):
        self.__description: str = description
        self.__unit: str = unit
        self.__value = value

    @property
    def description(self) -> str:
        """Description of the result"""
        return self.__description

    @property
    def unit(self) -> str:
        """Unit of the result"""
        return self.__unit

    @property
    def value(self) -> str:
        """Value of the result"""
        if isinstance(self.__value, (int, float, complex)) and not np.isnan(self.__value):
            return format_float(self.__value, decimals=2)
        elif isinstance(self.__value, (list, np.ndarray)):
            return str([round(value, 2) for value in self.__value])
        else:
            return str(self.__value)

    def to_csv(self) -> [str]:
        """Returns EvaluationResult as a list of strings."""
        res = list()
        res.append(self.description)
        res.append(self.value)
        res.append(self.unit)
        return res

    def to_console(self) -> str:
        """Returns EvaluationResult as a string in a format that is suitable for printing to the console."""
        res = ''
        res += '{:<50}'.format(self.description)
        res += self.value + ' '
        res += self.unit
        return res

    def __str__(self):
        return self.to_csv()

    def __repr__(self):
        return self.to_csv()
