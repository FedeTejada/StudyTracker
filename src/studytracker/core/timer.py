
import math
import time
from collections.abc import Callable

from studytracker.core.timer_state import TimerState


class Timer:
    def __init__(
        self,
        duration: int | float,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if isinstance(duration, bool) or not isinstance(duration, (int, float)):
            raise TypeError("Duration must be a number")

        if not math.isfinite(duration) or duration <= 0:
            raise ValueError("Duration must be a positive finite number")

        self.duration = float(duration)
        self.state = TimerState.IDLE

        self._remaining = self.duration
        self._deadline: float | None = None
        self._clock = clock

    @property
    def remaining(self) -> float:
        if self.state == TimerState.RUNNING:
            if self._deadline is None:
                raise RuntimeError("Running timer must have a deadline")

            return max(0.0, self._deadline - self._clock())

        return self._remaining

    def start(self) -> None:
        if self.state != TimerState.IDLE:
            raise RuntimeError("Timer can only be started from IDLE state")

        self._deadline = self._clock() + self._remaining
        self.state = TimerState.RUNNING

    def tick(self) -> None:
        if self.state != TimerState.RUNNING:
            return

        self._remaining = self.remaining

        if self._remaining == 0:
            self._deadline = None
            self.state = TimerState.FINISHED

    def pause(self) -> None:
        if self.state != TimerState.RUNNING:
            raise RuntimeError("Timer can only be paused from RUNNING state")

        if self.remaining <= 0:
            self.tick()
            return

        self._remaining = self.remaining
        self._deadline = None
        self.state = TimerState.PAUSED

    def resume(self) -> None:
        if self.state != TimerState.PAUSED:
            raise RuntimeError("Timer can only be resumed from PAUSED state")

        self._deadline = self._clock() + self._remaining
        self.state = TimerState.RUNNING

    def reset(self) -> None:
        self._remaining = self.duration
        self._deadline = None
        self.state = TimerState.IDLE
