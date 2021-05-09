import pytest
from restate import Machine, State


def test_state_change():
    s1 = State(name='locked')
    s2 = State(name='unlocked')
    turnstile = Machine('locked', states=[s1, s2])
    turnstile.add_transition(name='lock', start='unlocked', target='locked')
    turnstile.add_transition(name='unlock', start='locked', target='unlocked')

    assert(turnstile.state == 'locked')
    turnstile.unlock()
    assert(turnstile.state == 'unlocked')
    turnstile.lock()
    assert(turnstile.state == 'locked')
