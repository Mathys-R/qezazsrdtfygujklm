def test_intentionally_failing_math():
    """Ce test est fait pour échouer : 1 + 1 != 3"""
    assert 1 + 1 == 3

def test_intentionally_failing_logic():
    """Ce test est fait pour échouer : True is not False"""
    assert True is False
