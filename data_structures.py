from dataclasses import dataclass, field

@dataclass(order=True)
class PrioritizedItem:
    priority: float
    g_cost: float = field(compare=False)
    word: str = field(compare=False)