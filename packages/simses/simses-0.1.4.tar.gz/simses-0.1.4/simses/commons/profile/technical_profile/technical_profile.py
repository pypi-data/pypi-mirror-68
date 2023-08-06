from abc import ABC, abstractmethod


class TechnicalProfile(ABC):
    """
    Profile for additional data, e.g. frequency.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def next(self) -> float:
        """
        provides the data for a technical profile (SoC or frequency)

        Parameters
        ----------

        Returns
        -------
        float
            next data in a specific profile
        """
        pass

    @abstractmethod
    def close(self):
        """
        Closing all open resources in market profile

        Parameters
        ----------

        Returns
        -------

        """
        pass
