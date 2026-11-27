from studytracker.core.timer_state import TimerState

def test_timer_state_are_definded():
    assert TimerState.IDLE
    assert TimerState.RUNNING
    assert TimerState.PAUSED
    assert TimerState.FINISHED


