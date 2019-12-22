from __future__ import annotations
from abc import ABC, abstractmethod


class ErrorData(Exception):
    pass


class ListException(Exception):
    pass


class Context():

    def __init__(self):
        self.throw = FirstThrow()
        self.total_result = 0

    def count_result(self, game_result):
        try:
            self.counting(game_result=game_result)
            return self.total_result
        except ListException:
            print("Неверное количество фреймов, должно быть 10")
        except ValueError:
            print("Неверный тип данных, должны быть только числа от 1 до 9, X и символы / и -")
        except TypeError:
            print("Неверные данные, после / и - должны быть цифры")

    def counting(self, game_result):
        if len(game_result) < 10 or len(game_result) > 20:
            raise ListException
        self.total_count = 0
        for letter in game_result:
            self.aim_throw = self.throw.process(symbol=letter)
            if self.aim_throw == 20:
                self.total_count += 2
            else:
                self.total_count += 1
                self.moving()
            if self.aim_throw == 15:
                self.total_result -= self.previous_throw
            self.total_result += self.aim_throw
            self.previous_throw = self.aim_throw
        if self.total_count != 20:
            raise ListException

    def moving(self):
        if isinstance(self.throw, FirstThrow):
            self.throw = SecondThrow()
        else:
            frame = [self.previous_throw, self.aim_throw]
            if 15 not in frame and self.previous_throw + self.aim_throw >= 10:
                raise ListException
            self.throw = FirstThrow()


class Throw(ABC):

    def process(self, symbol):
        try:
            if symbol == 'X':
                return self._strike()
            elif symbol == '-':
                return 0
            elif symbol == '/':
                return self._spare()
            elif not int(symbol):
                raise ValueError("Неверный тип данных, должны быть только числа от 1 до 9, X и символы / и -")
            else:
                return int(symbol)
        except:
            raise

    @abstractmethod
    def _strike(self):
        pass

    @abstractmethod
    def _spare(self):
        pass


class FirstThrow(Throw):

    def _strike(self):
        return 20

    def _spare(self):
        raise TypeError("Неверные данные, должно быть число или -")


class SecondThrow(Throw):

    def _strike(self):
        raise TypeError("Неверные данные, должно быть число, / или -")

    def _spare(self):
        return 15


class Bowling():

    def __init__(self, game_result):
        self.game_result = game_result

    def get_score(self):
        result = Context()
        total_result = result.count_result(game_result=self.game_result)
        return total_result


