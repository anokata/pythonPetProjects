import pytest
import sys, os
sys.path.append('.')
import quest
import actions

def test_tire():
    p = quest.make_actor()
    s = p.arms.stamina
    actions.tire(p.arms, 3)
    assert p.arms.stamina == s - 3
