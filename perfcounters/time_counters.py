from time import time
from typing import List, Dict, Union

from .format import format_counters
AnyNum = Union[int, float]


class TimeCounter():
    "Single time counter"

    def __init__(self, name: str, prefix: str = ""):
        self.prefix = prefix
        self.name = name
        self.start_ts: float = time()
        self.laps: List[float] = []
        self.stop_ts: float = 0

    def lap(self) -> None:
        "record lap time"
        self.laps.append(time())

    def stop(self) -> None:
        "stop time counter"
        self.stop_ts = time()

    def reset(self):
        "Reset counter"
        self.start_ts = time()
        self.stop_ts = 0

    def get(self, format: str ='s', rounding: int = 2) -> float:
        """Report total elapsed time

        Args:
            format: reporting format. m for minute, s for second,
            ms for millisecond. Defaults to second (s).

            rounding: Time rounding. Defaults to 2.

        Returns:
            Report total elapsed time.

        """

        # compute current elapsed if stop not available
        stop_ts = self.stop_ts if self.stop_ts else time()


        ts = stop_ts - self.start_ts
        return self._convert_time(ts, format=format, rounding=rounding)

    def get_laps(self, format: str, rounding: int) -> List[float]:
        """Report laps time as a timeserie

        Args:
            format: reporting format. m for minute, s for second,
            ms for millisecond. Defaults to second (s).

            rounding: Time rounding. Defaults to 2.

        Returns:
            laps timeserie.

        """

        serie: List[float] = []

        # go through the laps
        prev_ts = self.start_ts
        for lap in self.laps:
            ts = lap - prev_ts
            ts = self._convert_time(ts, format=format, rounding=rounding)
            serie.append(ts)
            prev_ts = lap


        # final lap
        # compute current elapsed if stop not available
        stop_ts = self.stop_ts if self.stop_ts else time()
        ts = stop_ts - prev_ts
        ts = self._convert_time(ts, format=format, rounding=rounding)
        serie.append(prev_ts - self.stop_ts)

        return serie


    def _convert_time(self, ts: float, format: str, rounding: int) -> AnyNum:
        "convert time to requested format"
        if format not in ['m', 's', 'ms']:
            raise ValueError("Unsupported format. Valid: m , s and ms")

        if format == 'm':
            ts /= 60
        if format == 'ms':
            ts *= 1000

        # if rounding to 0 then we want the int
        if not rounding:
            return int(ts)
        else:
            return round(ts, rounding)

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


class TimeCounters():
    def __init__(self, prefix: str = "") -> None:
        self.prefix = prefix
        self.counters: Dict[str, TimeCounter] = {}

    def start(self, name: str) -> None:
        "start a counter"
        if name in self.counters:
            raise ValueError(f"Counter {name} already exist")
        self.counters[name] = TimeCounter(name=name, prefix=self.prefix)

    def stop(self, name: str) -> None:
        "stop a counter"
        if name not in self.counters:
            raise ValueError(f"Unknown counter {name}")
        return self.counters[name].stop()


    def stop_all(self) -> None:
        "stop all counters"
        for cnt in self.counters.values():
            cnt.stop()

    def lap(self, name: str) -> None:
        "add lap"
        if name not in self.counters:
            raise ValueError(f"Unknown counter {name}")
        return self.counters[name].lap()


    def reset(self, name: str) -> None:
        "reset a given counter"
        if name not in self.counters:
            raise ValueError(f"Unknown counter {name}")
        self.counters[name].reset()


    def reset_all(self) -> None:
        "reset all counters"
        for cnt in self.counters.values():
            cnt.reset()


    def get(self, name: str, format: str = "s", rounding : int = 2) -> float:
        """Return a counter total time

        Args:
            name: name of the counter.

            format: time reporting format. m for minute, s for second,
            ms for millisecond. Defaults to second (s).

            rounding: Time rounding. Defaults to 2.

        Returns:
            total time in requested format.

        """
        if name not in self.counters:
            raise ValueError(f"Unknown counter {name}")
        return self.counters[name].get(format=format, rounding=rounding)


    def get_laps(self, name: str, format: str = "s",
                rounding : int = 2) -> List[float]:
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
        return self.counters[name].get_laps(format=format, rounding=rounding)

    def get_all(self, format: str = "s", rounding : int = 2) -> Dict[str, float]:
        """Return all counters elapsed times as a dictionary

        Args:

            format: time reporting format. m for minute, s for second,
            ms for millisecond. Defaults to second (s).

            rounding: Time rounding. Defaults to 2.

        Returns:
            Dictionary of counters

        """
        cnts = {}
        for name, cnt in self.counters.items():
            cnts[f'{self.prefix}{name}'] = cnt.get(format=format, rounding=rounding)
        return cnts


    def report(self, format: str = "s", rounding : int = 2) -> None:
        "pretty print counters "
        print(self._format(output_type='rounded_outline', format=format,
                           rounding=rounding))


    def report_laps(self, name: str, format: str = "s",
                    rounding : int = 2) -> None:
        "pretty print a counter lap "
        print(self._format_laps(name=name,
                                output_type='rounded_outline', format=format,
                                rounding=rounding))

    def to_json(self, format: str = "s",
                rounding : int = 2) -> str:
        """Return counters a json string

        Args:

            format: time reporting format. m for minute, s for second,
            ms for millisecond. Defaults to second (s).

            rounding: Time rounding. Defaults to 2.

        Returns:
            counters serialized as json string

        """
        return self._format(output_type='json', format=format,
                            rounding=rounding)

    def laps_to_json(self, name: str, format: str = "s",
                    rounding : int = 2) -> str:
        """Return counter laps a json string

        Args:
            name: name of the counter.
            format: time reporting format. m for minute, s for second,
            ms for millisecond. Defaults to second (s).

            rounding: Time rounding. Defaults to 2.

        Returns:
            laps serialized as json string
        """

        return self._format_laps(name=name, output_type='json',
                                 format=format, rounding=rounding)


    def to_html(self, format: str = "s",
                rounding : int = 2) -> str:
        """Return counters as html table

        Args:

            format: time reporting format. m for minute, s for second,
            ms for millisecond. Defaults to second (s).

            rounding: Time rounding. Defaults to 2.

        Returns:
            counters as html table

        """
        return self._format(output_type='html', format=format,
                            rounding=rounding)

    def laps_to_html(self, name: str, format: str = "s",
                    rounding : int = 2) -> str:
        """Return counter laps a html table

        Args:
            name: name of the counter.
            format: time reporting format. m for minute, s for second,
            ms for millisecond. Defaults to second (s).

            rounding: Time rounding. Defaults to 2.

        Returns:
            laps html table
        """

        return self._format_laps(name=name, output_type='html',
                                 format=format, rounding=rounding)



    def to_md(self, format: str = "s",
                rounding : int = 2) -> str:
        """Return counters as markdown format

        Args:

            format: time reporting format. m for minute, s for second,
            ms for millisecond. Defaults to second (s).

            rounding: Time rounding. Defaults to 2.

        Returns:
            counters as markdown table

        """
        return self._format(output_type='github', format=format,
                            rounding=rounding)

    def laps_to_md(self, name: str, format: str = "s",
                    rounding : int = 2) -> str:
        """Return counter laps a Markdown table

        Args:
            name: name of the counter.
            format: time reporting format. m for minute, s for second,
            ms for millisecond. Defaults to second (s).

            rounding: Time rounding. Defaults to 2.

        Returns:
            laps markdown table
        """

        return self._format_laps(name=name, output_type='github',
                                 format=format, rounding=rounding)

    def to_latex(self, format: str = "s",
                rounding : int = 2) -> str:
        """Return counters as latex format

        Args:

            format: time reporting format. m for minute, s for second,
            ms for millisecond. Defaults to second (s).

            rounding: Time rounding. Defaults to 2.

        Returns:
           counters as latex table

        """
        return self._format(output_type='latex', format=format,
                            rounding=rounding)


    def laps_to_latex(self, name: str, format: str = "s",
                    rounding : int = 2) -> str:
        """Return counter laps a html table

        Args:
            name: name of the counter.
            format: time reporting format. m for minute, s for second,
            ms for millisecond. Defaults to second (s).

            rounding: Time rounding. Defaults to 2.

        Returns:
            laps html table
        """

        return self._format_laps(name=name, output_type='html',
                                 format=format, rounding=rounding)

    def _format(self, output_type: str, format: str, rounding: int) -> str:
        cnts = self.get_all(format=format, rounding=rounding)
        return format_counters(cnts, headers=['Name', f"Time ({format})"],
                               format=output_type)



    def _format_laps(self, name: str, output_type: str,  format: str,
                         rounding: int) -> str:
        laps = self.get_laps(name, format=format, rounding=rounding)

        # converts laps into a dict[str, int]
        rows = {}
        for i, v in enumerate(laps):
            rows[str(i)] = v

        return format_counters(rows,
                               headers=['Lap', 'Value'],
                               format=output_type)


    def __len__(self):
        return len(self.counters)

