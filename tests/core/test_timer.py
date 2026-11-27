import pytest
from studytracker.core.timer import Timer
from studytracker.core.timer_state import TimerState


def test_timer_initialization():
    timer = Timer(duration=1500)

    assert timer.duration == 1500
    assert timer.state == TimerState.IDLE
    assert timer._remaining == 1500
    assert timer._deadline is None


@pytest.mark.parametrize("duration", [0, -10, float("inf"), float("nan")])
def test_timer_rejects_invalid_duration(duration):
    with pytest.raises(ValueError):
        Timer(duration=duration)


@pytest.mark.parametrize("duration", ["1500", None, True])
def test_timer_rejects_non_numeric_duration(duration):
    with pytest.raises(TypeError):
        Timer(duration=duration)

def test_timer_start():
    timer = Timer(duration=1500, clock=lambda: 1000.0)

    timer.start()

    assert timer.state == TimerState.RUNNING
    assert timer._deadline == 2500.0


def test_timer_cannot_start_twice():
    timer = Timer(duration=1500, clock=lambda: 1000.0)

    timer.start()

    with pytest.raises(RuntimeError):
        timer.start()


def test_timer_cannot_start_from_finished():
    timer = Timer(duration=1500, clock=lambda: 1000.0)
    timer.state = TimerState.FINISHED

    with pytest.raises(RuntimeError):
        timer.start()

class FakeClock:
    def __init__(self, initial_time=1000.0):
        self.current_time = initial_time

    def advance(self, seconds):
        self.current_time += seconds

    def __call__(self):
        return self.current_time


def test_timer_remaining():
    clock = FakeClock()
    timer = Timer(duration=1500, clock=clock)

    timer.start()
    clock.advance(300)

    assert timer.remaining == 1200


def test_timer_tick_updates_remaining():
    clock = FakeClock()
    timer = Timer(duration=1500, clock=clock)

    timer.start()
    clock.advance(300)
    timer.tick()

    assert timer.remaining == 1200
    assert timer.state == TimerState.RUNNING


def test_timer_finishes_when_time_expires():
    clock = FakeClock()
    timer = Timer(duration=10, clock=clock)

    timer.start()
    clock.advance(10)
    timer.tick()

    assert timer.remaining == 0
    assert timer.state == TimerState.FINISHED
    assert timer._deadline is None


def test_timer_does_not_go_below_zero():
    clock = FakeClock()
    timer = Timer(duration=10, clock=clock)

    timer.start()
    clock.advance(15)
    timer.tick()

    assert timer.remaining == 0
    assert timer.state == TimerState.FINISHED


def test_tick_does_nothing_when_timer_is_not_running():
    clock = FakeClock()
    timer = Timer(duration=1500, clock=clock)

    timer.tick()

    assert timer.state == TimerState.IDLE
    assert timer.remaining == 1500

def test_timer_pause():
    clock = FakeClock()
    timer = Timer(duration=1500, clock=clock)

    timer.start()
    clock.advance(300)
    timer.pause()

    assert timer.state == TimerState.PAUSED
    assert timer.remaining == 1200
    assert timer._deadline is None


def test_timer_resume():
    clock = FakeClock()
    timer = Timer(duration=1500, clock=clock)

    timer.start()
    clock.advance(300)
    timer.pause()

    clock.advance(600)
    timer.resume()

    assert timer.state == TimerState.RUNNING
    assert timer.remaining == 1200
    assert timer._deadline == clock() + 1200


def test_timer_cannot_pause_when_not_running():
    timer = Timer(duration=1500)

    with pytest.raises(RuntimeError):
        timer.pause()


def test_timer_cannot_resume_when_not_paused():
    timer = Timer(duration=1500)

    with pytest.raises(RuntimeError):
        timer.resume()


def test_timer_remaining_does_not_change_while_paused():
    clock = FakeClock()
    timer = Timer(duration=1500, clock=clock)

    timer.start()
    clock.advance(300)
    timer.pause()

    clock.advance(500)

    assert timer.remaining == 1200

def test_timer_finishes_instead_of_pausing_when_deadline_expires():
    clock = FakeClock()
    timer = Timer(duration=10, clock=clock)

    timer.start()
    clock.advance(10)

    timer.pause()

    assert timer.state == TimerState.FINISHED
    assert timer.remaining == 0
    assert timer._deadline is None

def test_timer_finishes_when_pause_is_called_after_deadline():
    clock = FakeClock()
    timer = Timer(duration=10, clock=clock)

    timer.start()
    clock.advance(15)

    timer.pause()

    assert timer.state == TimerState.FINISHED
    assert timer.remaining == 0

def test_timer_reset_from_running():
    clock = FakeClock()
    timer = Timer(duration=1500, clock=clock)

    timer.start()
    clock.advance(300)
    timer.reset()

    assert timer.state == TimerState.IDLE
    assert timer.remaining == 1500
    assert timer._deadline is None


def test_timer_reset_from_paused():
    clock = FakeClock()
    timer = Timer(duration=1500, clock=clock)

    timer.start()
    clock.advance(300)
    timer.pause()
    timer.reset()

    assert timer.state == TimerState.IDLE
    assert timer.remaining == 1500
    assert timer._deadline is None


def test_timer_reset_from_finished():
    clock = FakeClock()
    timer = Timer(duration=10, clock=clock)

    timer.start()
    clock.advance(10)
    timer.tick()
    timer.reset()

    assert timer.state == TimerState.IDLE
    assert timer.remaining == 10
    assert timer._deadline is None


def test_timer_reset_multiple_times():
    timer = Timer(duration=1500)

    timer.reset()
    timer.reset()

    assert timer.state == TimerState.IDLE
    assert timer.remaining == 1500
    assert timer._deadline is None

def test_tick_does_nothing_when_timer_is_paused():
    clock = FakeClock()
    timer = Timer(duration=1500, clock=clock)

    timer.start()
    clock.advance(300)
    timer.pause()

    clock.advance(500)
    timer.tick()

    assert timer.state == TimerState.PAUSED
    assert timer.remaining == 1200