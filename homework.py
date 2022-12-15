class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message_parameters: list = [self.training_type, self.duration,
                                    self.distance, self.speed, self.calories]
        message: str = ('Тип тренировки: {0}; Длительность: {1:.3f} ч.; '
                        'Дистанция: {2:.3f} км; Ср. скорость: {3:.3f} км/ч; '
                        'Потрачено ккал: {4:.3f}.'.format(*message_parameters))
        return message


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    CM_IN_M: int = 100
    MIN_IN_H: int = 60
    KMH_IN_MSEC: float = 0.278

    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                            * self.get_mean_speed()
                            + self.CALORIES_MEAN_SPEED_SHIFT)
                           * self.weight
                           / self.M_IN_KM
                           * (self.duration * self.MIN_IN_H))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height / self.CM_IN_M

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


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

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
        workout = training_types[workout_type](*data)
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
        if training is None:
            print(f'Переданы неверные данные: тип тренировки {workout_type}')
        else:
            main(training)
