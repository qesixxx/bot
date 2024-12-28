# base_for_expiry.py
from datetime import datetime

class Equipment:
    def __init__(self, name, position, expiration_date, passport_link):
        self.name = name
        self.position = position
        self.expiration_date = expiration_date
        self.passport_link = passport_link

    def __str__(self):
        return (f"{self.name} (до: {self.expiration_date.strftime('%d.%m.%Y')}), "
                f"{self.position}, {self.passport_link}")

    def is_expired(self):
        return self.expiration_date < datetime.now()

    def is_expiring_soon(self):
        return (self.expiration_date - datetime.now()).days < 30 and not self.is_expired()


equipment_database = [
    Equipment(
        "Пресс гидравлический",
        "Склад 1, ряд 3",
        datetime(2025, 12, 31),
        "http://example.com/passport1"
    ),
    Equipment(
        "Токарный станок",
        "Цех 2, ряд 5",
        datetime(2023, 10, 15),
        "http://example.com/passport2"
    ),
    Equipment(
        "Фрезерный станок",
        "Цех 1, ряд 2",
        datetime(2024, 12, 31),
        "http://example.com/passport3"
    ),
    Equipment(
        "Сварочный аппарат",
        "Склад 2, ряд 1",
        datetime(2023, 10, 20),
        "http://example.com/passport4"
    )
]