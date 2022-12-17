from dataclasses import dataclass, field


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE_TEXT: str = field(init=False, default=(
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    ))

    def get_message(self) -> str:
        message: str = self.MESSAGE_TEXT.format(
            training_type=self.training_type,
            duration=self.duration,
            distance=self.distance,
            speed=self.speed,
            calories=self.calories
        )
        return message


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    M_IN_KM: int = field(init=False, default=1000)
    MIN_IN_H: int = field(init=False, default=60)

    LEN_STEP: float = field(init=False, default=0.65)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message: InfoMessage = InfoMessage(self.__class__.__name__,
                                           self.duration,
                                           self.get_distance(),
                                           self.get_mean_speed(),
                                           self.get_spent_calories()
                                           )
        return message


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = field(init=False, default=18)
    CALORIES_MEAN_SPEED_SHIFT: float = field(init=False, default=1.79)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                            * self.get_mean_speed()
                            + self.CALORIES_MEAN_SPEED_SHIFT)
                           * self.weight
                           / self.M_IN_KM
                           * (self.duration * self.MIN_IN_H))
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    CM_IN_M: int = field(init=False, default=100)
    KMH_IN_MSEC: float = field(init=False, default=0.278)

    CALORIES_WEIGHT_MULTIPLIER: float = field(init=False, default=0.035)
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = field(init=False, default=0.029)

    def __post_init__(self):
        self.height = self.height / self.CM_IN_M

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе."""
        calories: float = ((self.CALORIES_WEIGHT_MULTIPLIER
                            * self.weight
                            + ((self.get_mean_speed() * self.KMH_IN_MSEC)**2
                               / self.height)
                            * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                            * self.weight)
                           * (self.duration * self.MIN_IN_H))
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int

    LEN_STEP: float = field(init=False, default=1.38)

    CALORIES_MEAN_SPEED_SHIFT: float = field(init=False, default=1.1)
    CALORIES_MEAN_SPEED_MULTIPLIER: int = field(init=False, default=2)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        speed: float = (self.length_pool
                        * self.count_pool
                        / self.M_IN_KM
                        / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        calories: float = ((self.get_mean_speed()
                            + self.CALORIES_MEAN_SPEED_SHIFT)
                           * self.CALORIES_MEAN_SPEED_MULTIPLIER
                           * self.weight
                           * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout: Training = None
    training_types: dict = {'SWM': Swimming,
                            'RUN': Running,
                            'WLK': SportsWalking}
    if workout_type in training_types:
        try:
            workout = training_types[workout_type](*data)
        except TypeError:
            print(f'Переданы неверные параметры для тренировки {workout_type}')
    else:
        print(f'Тип тренировки: {workout_type} не предусмотрен программой.')
    return workout


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[str, list] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        try:
            main(training)
        except AttributeError:
            pass
        except ZeroDivisionError:
            print(f'Для тренировки {training.__class__.__name__} '
                  f'переданы некорректные параметры: длительность или рост '
                  f'(для типа плавание).')
