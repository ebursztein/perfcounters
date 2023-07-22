import json
from tabulate import tabulate
from typing import List, Dict, Union

AnyNum = Union[int, float]
CNTS = Dict[str, AnyNum]

def format_counters(cnts: CNTS, headers: List[str],
                    format: str = 'rounded_outline') -> str:

    if format == "json":
        return json.dumps(cnts)
    else:
        rows = [[k, v] for k, v in cnts.items()]
        return tabulate(rows, headers=headers, tablefmt=format)

