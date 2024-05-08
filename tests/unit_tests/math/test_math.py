import pytest


class TestMath:
    async def test_one_plus_ose(self):
        assert 1+1 == 2

    def test_divide_by_zero(self):
        def divide_by_zero():
            return 9 / 0

        # Если функция divide_by_zero вызывает исключение ZeroDivisionError, тест будет пройден успешно
        with pytest.raises(ZeroDivisionError):
            divide_by_zero()

    def test_multiply_5_by_10(self):
        assert 5*10 == 50
