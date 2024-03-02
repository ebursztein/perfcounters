from .format import format_counters
from typing import List, Union, Dict
AnyNum = Union[int, float]

class ValueCounter():
    "Single value counter"

    def __init__(self, name: str, value: AnyNum = 0, prefix: str = ""):
        self.name = name
        self.prefix = prefix
        self.value: AnyNum = value
        self.laps: List[AnyNum] = []

    def lap(self) -> None:
        "record intermediate value"
        self.laps.append(self.value)

    def inc(self, value: AnyNum = 1) -> AnyNum:
        "increment counter by X"
        self.value += value
        return self.value


    def dec(self, value: AnyNum = 1) -> AnyNum:
        "Decrement counter by X"
        self.value -= value
        return self.value

    def set(self, value: AnyNum = 1) -> AnyNum:
        "Set counter to X"
        self.value = value
        return self.value


    def reset(self, value: int = 0) -> None:
        "reset counter."
        self.value = 0

    def get(self, rounding: int = 2) -> AnyNum:
        """get counter value.

        Args:
            rounding: Value rounding. Defaults to 2.

        Returns:
            Counter value.

        """
        if isinstance(self.value, float):
            return round(self.value, rounding)
        return self.value


    def get_laps(self, rounding: int) -> List[AnyNum]:
        """Report laps values as a timeserie

        Args:
            rounding: Time rounding. Defaults to 2.

        Returns:
            laps timeserie.

        """

        serie: List[AnyNum] = []

        for val in self.laps:
            # round if need be
            val = round(val, rounding) if isinstance(val, float) else val
            serie.append(val)

        # final val
        # compute current elapsed if stop not available
        val = self.value
        val = round(val, rounding) if isinstance(val, float) else val
        serie.append(val)

        return serie

    def __str__(self) -> str:
        if self.prefix:
            return f"{self.prefix}{self.name}"
        else:
            return self.name

    def __repr__(self) -> str:
        if self.prefix:
            return f"{self.prefix}{self.name}"
        else:
            return self.name

class ValueCounters():
    def __init__(self, prefix: str = "") -> None:
        self.prefix = prefix
        self.counters: Dict[str, ValueCounter] = {}

    def _init_counter(self, name: str, value: AnyNum = 0) -> None:
        "init a counter"
        if name in self.counters:
            raise ValueError(f"Counter {name} already exist")
        self.counters[name] = ValueCounter(name=name, value=value,
                                           prefix=self.prefix)

    def inc(self, name: str, value=1) -> AnyNum:
        "Imcrement a counter"
        if name not in self.counters:
            self._init_counter(name=name, value=0)
        return self.counters[name].inc(value=value)

    def dec(self, name: str, value=1) -> AnyNum:
        "decrement a counter"
        if name not in self.counters:
            self._init_counter(name=name, value=0)
        return self.counters[name].dec(value=value)

    def set(self, name: str, value=1) -> AnyNum:
        "decrement a counter"
        if name not in self.counters:
            self._init_counter(name=name, value=0)
        return self.counters[name].set(value=value)


    def lap(self, name: str):
        "record intermediate value"
        if name not in self.counters:
            self._init_counter(name=name)
        return self.counters[name].lap()


    def reset(self, name) -> None:
        "reset a given counter"
        if name not in self.counters:
            raise ValueError(f"Unknown counter {name}")
        self.counters[name].reset()


    def reset_all(self) -> None:
        "reset all counters"
        for cnt in self.counters.values():
            cnt.reset()


    def get(self, name: str, rounding : int = 2) -> AnyNum:
        """Return a counter value

        Args:
            name: name of the counter.

            rounding: Float rounding. Defaults to 2.

        Returns:
            counter value

        """
        if name not in self.counters:
            raise ValueError(f"Unknown counter {name}")
        return self.counters[name].get(rounding=rounding)

    def get_laps(self, name: str, rounding : int = 2) -> List[AnyNum]:
        """Return a counter laps timeserie.

        Args:
            name: name of the counter.

            format: time reporting format. m for minute, s for second,
            ms for millisecond. Defaults to second (s).

            rounding: Time rounding. Defaults to 2.

        Returns:
            laps timeserie in the request format.

        """
        if name not in self.counters:
            raise ValueError(f"Unknown counter {name}")
        return self.counters[name].get_laps(rounding=rounding)

    def get_all(self, rounding : int = 2) -> Dict[str, AnyNum]:
        """Return all counters values as a dictionary

        Args:

            rounding: Time rounding. Defaults to 2.

        Returns:
            Dictionary of counters

        """
        cnts = {}
        for name, cnt in self.counters.items():
            cnts[f"{self.prefix}{name}"] = cnt.get(rounding=rounding)
        return cnts

    def report(self, rounding : int = 2) -> None:
        "pretty print counters "
        print(self._format(output_type='rounded_outline',
                           rounding=rounding))

    def to_json(self, rounding : int = 2) -> str:
        """Return counters a json string

        Args:

            format: time reporting format. m for minute, s for second,
            ms for millisecond. Defaults to second (s).

            rounding: Time rounding. Defaults to 2.

        Returns:
            json string

        """
        return self._format(output_type='json', rounding=rounding)

    def to_html(self, format: str = "s",
                rounding : int = 2) -> str:
        """Return counters as html

        Args:

            format: time reporting format. m for minute, s for second,
            ms for millisecond. Defaults to second (s).

            rounding: Time rounding. Defaults to 2.

        Returns:
            counters as a html table

        """
        return self._format(output_type='html', rounding=rounding)


    def to_md(self, rounding : int = 2) -> str:
        """Return counters as markdown format

        Args:

            format: time reporting format. m for minute, s for second,
            ms for millisecond. Defaults to second (s).

            rounding: Time rounding. Defaults to 2.

        Returns:
            json string

        """
        return self._format(output_type='github', rounding=rounding)


    def to_latex(self, rounding : int = 2) -> str:
        """Return counters as latex format

        Args:
            rounding: Time rounding. Defaults to 2.

        Returns:
            counters in a latex table

        """
        return self._format(output_type='latex', rounding=rounding)


    def _format(self, output_type: str, rounding: int) -> str:
        cnts = self.get_all(rounding=rounding)
        return format_counters(cnts, headers=['Name', "Value"],
                               format=output_type)


    def __len__(self):
        return len(self.counters)
