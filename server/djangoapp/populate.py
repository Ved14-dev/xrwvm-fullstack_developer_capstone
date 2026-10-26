from .models import CarMake, CarModel


def initiate():
    if CarMake.objects.exists():
        return

    makes = [
        ("Audi", "German luxury vehicles"),
        ("BMW", "Performance-focused German vehicles"),
        ("Ford", "American cars, trucks, and SUVs"),
        ("Honda", "Reliable cars and utility vehicles"),
        ("Toyota", "Efficient and dependable vehicles"),
    ]
    models = [
        ("Audi", 1, "A4", "Sedan", 2021),
        ("Audi", 2, "Q5", "SUV", 2022),
        ("Audi", 3, "A6", "Sedan", 2023),
        ("BMW", 4, "3 Series", "Sedan", 2021),
        ("BMW", 5, "X3", "SUV", 2022),
        ("BMW", 6, "5 Series", "Sedan", 2023),
        ("Ford", 7, "Escape", "SUV", 2021),
        ("Ford", 8, "Explorer", "SUV", 2022),
        ("Ford", 9, "Taurus", "Sedan", 2023),
        ("Honda", 10, "Civic", "Sedan", 2021),
        ("Honda", 11, "CR-V", "SUV", 2022),
        ("Honda", 12, "Accord", "Sedan", 2023),
        ("Toyota", 13, "Camry", "Sedan", 2021),
        ("Toyota", 14, "RAV4", "SUV", 2022),
        ("Toyota", 15, "Venza", "Wagon", 2023),
    ]
    make_objects = {
        name: CarMake.objects.create(name=name, description=description)
        for name, description in makes
    }
    CarModel.objects.bulk_create(
        [
            CarModel(
                car_make=make_objects[make],
                dealer_id=dealer_id,
                name=name,
                type=car_type,
                year=year,
            )
            for make, dealer_id, name, car_type, year in models
        ]
    )
