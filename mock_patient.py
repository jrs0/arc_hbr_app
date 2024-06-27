from typing import Any
from faker import Faker
from dataclasses import dataclass, field
import numpy as np

@dataclass
class Random:
    seed: int
    missingness: float = 0.2
    rng: np.random.Generator = field(init=False)
    faker: Faker = field(init=False)

    def __post_init__(self):
        self.rng = np.random.default_rng(seed=self.seed)
        self.faker = Faker(seed=self.seed)
        
    def random_name(self):
        return self.faker.name()

    def random_tnumber(self):
        num = int(self.rng.uniform(0, 9999999))
        return f"T{num:>07}"
        
    def random_choice(self, choices: list[Any], p: list[float]) -> Any | None:
        other_weights = [w * (1 - self.missingness) for w in p]
        weights = [self.missingness] + other_weights

        return self.rng.choice([None] + choices, p = weights)
    
    def random_int(self, center: int, scale: int) -> int | None:
        val = max(0, int(self.rng.normal(center, scale)))
        return self.random_choice([val], p = [1.0])

    def random_float(self, center: float, scale: float, dp: int) -> float | None:
        """Random real number rounded to decimal places
        """
        val = max(0.0, round(self.rng.normal(center, scale), dp))
        return self.random_choice([val], p = [1.0])
    
    def random_patient(self) -> dict[str, str | int | float | None]:
        """Create mock patient data
        
        This simulates data that might be fetched from backend
        data sources automatically.
        """
        return {
            "name": self.random_name(),
            "age": self.random_int(70, 10),
            "oac": self.random_choice(["Yes", "No"], p = [0.05, 0.95]),
            "gender": self.random_choice(["Male", "Female"], p = [0.5, 0.5]),
            "hb": self.random_float(12, 2, 1),
            "platelets": self.random_int(150, 70),
            "egfr": self.random_int(90, 50),
            "prior_bleeding": self.random_choice([
                "< 6 months or recurrent",
                "< 12 months",
                "No bleeding"
            ], p = [0.025, 0.025, 0.95]),
            "cirrhosis_ptl_hyp": self.random_choice(["Yes", "No"], p = [0.05, 0.95]),
            "nsaid": self.random_choice(["Yes", "No"], p = [0.05, 0.95]),
            "cancer": self.random_choice(["Yes", "No"], p = [0.05, 0.95]),
            "prior_ich_stroke": self.random_choice([
                "bAVM, ICH, or moderate/severe ischaemic stroke < 6 months",
                "Any prior ischaemic stroke",
                "No ICH/ischaemic stroke"
            ], p = [0.025, 0.025, 0.95]),
            "prior_surgery_trauma": self.random_choice(["Yes", "No"], p = [0.05, 0.95]),
            "planned_surgery": self.random_choice(["Yes", "No"], p = [0.05, 0.95]),
        }


    


