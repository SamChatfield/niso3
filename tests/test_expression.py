from expression import Expression

def test_eval_add():
    assert Expression('(add 5 4)').eval() == 9

def test_eval_pow():
    assert Expression('(pow 2 3)').eval() == 8
    assert Expression('(pow -1 0.5)').eval() == 0

def test_eval_sqrt():
    assert Expression('(sqrt -1)').eval() == 0

def test_eval_log():
    assert Expression('(log -1)').eval() == 0
