from abc import ABC, abstractmethod


class ReportItemCommon(ABC):
    @abstractmethod
    def generate_latex(self, output_path: str = None, remote: bool = False) -> str:
        # commmon for all items
        raise NotImplementedError
