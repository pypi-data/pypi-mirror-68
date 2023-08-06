import time
from typing import List, Dict
from gp_framework.population_manager import PopulationManager, LifecycleReport
from gp_framework.fitness_calculator import NumberGeneratorPhenotypeConverter, NumberGenerator, StringPhenotypeConverter


class EvolutionaryOptimizer:
    def __init__(self, managers: List[PopulationManager]):
        self._managers = managers

    @staticmethod
    def _run_lifecycles(manager: PopulationManager, max_iterations: int = -1) -> List[LifecycleReport]:
        print("Began {} at {}.".format(manager.name, _time()))

        i = 0
        reports = []
        # todo decide how to implement metadata, maybe have a list inside LifecycleReport
        while i < max_iterations and (len(reports) == 0 or reports[len(reports) - 1].max_fitness != 1.0):
            reports.append(manager.lifecycle())
            i += 1

        print("Finished {} ({} iterations) at {}.".format(manager.name, i, _time()))
        if reports[-1].solution is not None:
            converter = StringPhenotypeConverter(len(reports[-1].solution))
            print("Solution:", converter.convert(reports[-1].solution))
        print()

        return reports

    def run_many_lifecycles(self, max_iterations) -> Dict[str, List[LifecycleReport]]:
        manager_name_to_reports = {}
        for manager in self._managers:
            manager_name_to_reports[manager.name] = EvolutionaryOptimizer._run_lifecycles(manager, max_iterations)

        return manager_name_to_reports


def _time() -> str:
    return time.asctime(time.localtime(time.time()))
