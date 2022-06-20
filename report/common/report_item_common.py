from abc import ABC, abstractmethod


class ReportItemCommon(ABC):
    @abstractmethod
    def generate_latex(self, remote=False) -> str:
        # commmon for all items
        raise NotImplementedError
