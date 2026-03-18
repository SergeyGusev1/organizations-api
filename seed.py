"""
Populate the database with test data.

Usage:
    python seed.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.models.building import Building
from app.models.activity import Activity
from app.models.organization import Organization, Phone


def seed() -> None:
    db = SessionLocal()
    try:
        # ------------------------------------------------------------------
        # Buildings
        # ------------------------------------------------------------------
        buildings = [
            Building(address="г. Москва, ул. Ленина 1, офис 3", latitude=55.7558, longitude=37.6173),
            Building(address="г. Москва, пр. Блюхера 32/1", latitude=55.7700, longitude=37.6500),
            Building(address="г. Санкт-Петербург, Невский пр. 10", latitude=59.9343, longitude=30.3351),
        ]
        db.add_all(buildings)
        db.flush()

        # ------------------------------------------------------------------
        # Activity tree (max 3 levels)
        #
        # Еда (1)
        #   Мясная продукция (2)
        #   Молочная продукция (2)
        # Автомобили (1)
        #   Грузовые (2)
        #   Легковые (2)
        #     Запчасти (3)
        #     Аксессуары (3)
        # ------------------------------------------------------------------
        eda = Activity(name="Еда", level=1)
        avto = Activity(name="Автомобили", level=1)
        db.add_all([eda, avto])
        db.flush()

        myaso = Activity(name="Мясная продукция", level=2, parent_id=eda.id)
        moloko = Activity(name="Молочная продукция", level=2, parent_id=eda.id)
        gruz = Activity(name="Грузовые", level=2, parent_id=avto.id)
        legk = Activity(name="Легковые", level=2, parent_id=avto.id)
        db.add_all([myaso, moloko, gruz, legk])
        db.flush()

        zapch = Activity(name="Запчасти", level=3, parent_id=legk.id)
        akses = Activity(name="Аксессуары", level=3, parent_id=legk.id)
        db.add_all([zapch, akses])
        db.flush()

        # ------------------------------------------------------------------
        # Organizations
        # ------------------------------------------------------------------
        org1 = Organization(name='ООО "Рога и Копыта"', building_id=buildings[0].id)
        org2 = Organization(name='ЗАО "Молочный рай"', building_id=buildings[0].id)
        org3 = Organization(name='ИП Иванов — Автозапчасти', building_id=buildings[1].id)
        org4 = Organization(name='АвтоГрупп', building_id=buildings[1].id)
        org5 = Organization(name='Северная Молочня', building_id=buildings[2].id)

        db.add_all([org1, org2, org3, org4, org5])
        db.flush()

        # Phones
        db.add_all([
            Phone(number="2-222-222", organization_id=org1.id),
            Phone(number="3-333-333", organization_id=org1.id),
            Phone(number="8-923-666-13-13", organization_id=org1.id),
            Phone(number="8-800-555-35-35", organization_id=org2.id),
            Phone(number="8-495-123-45-67", organization_id=org3.id),
            Phone(number="8-495-765-43-21", organization_id=org4.id),
            Phone(number="8-812-999-00-11", organization_id=org5.id),
        ])

        # Activities
        org1.activities = [myaso, eda]
        org2.activities = [moloko]
        org3.activities = [zapch, akses]
        org4.activities = [gruz, legk]
        org5.activities = [moloko, eda]

        db.commit()
        print("✓ Seed data inserted successfully.")
    except Exception as exc:
        db.rollback()
        print(f"✗ Seed failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
