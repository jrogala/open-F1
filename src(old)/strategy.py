from typing import overload
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from tyre import Tyre


@dataclass
class PitStop():
    new_tyre: Tyre
    lap: int
    pit_rolling: float = field(default=17)
    pit_time: float = field(default=2.5)
