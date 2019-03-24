from expression import Expression

def test_eval_add():
    assert Expression('(add 5 4)').eval() == 9

def test_eval_sub():
    assert Expression('(sub 5 4)').eval() == 1

def test_eval_div():
    assert Expression('(div 4 2)').eval() == 2
    assert Expression('(div 8 5)').eval() == 1.6
    assert Expression('(div 1 0)').eval() == 0

def test_eval_pow():
    assert Expression('(pow 2 3)').eval() == 8
    assert Expression('(pow -1 0.5)').eval() == 0

def test_eval_sqrt():
    assert Expression('(sqrt -1)').eval() == 0

def test_eval_log():
    assert Expression('(log -1)').eval() == 0

def test_eval_data():
    assert Expression('(data 1)').eval((1.23, 4.56, 7.89)) == 4.56

def test_eval():
    assert Expression('(add (mul 2 3) (log 4))').eval() == 8

def test_replace_subtree():
    expr = Expression('(add 2 3)')
    expr2 = Expression('(sub 5 4)')
    repl_expr = expr.replace_subtree(1, expr2)
    assert repl_expr == Expression('(add (sub 5 4) 3)')

    expr = Expression('(add (sub 3 2) (mul 4 (sqrt 16)))')
    expr2 = Expression('1')
    repl_expr = expr.replace_subtree(3, expr2)
    assert repl_expr == Expression('(add (sub 3 1) (mul 4 (sqrt 16)))')
