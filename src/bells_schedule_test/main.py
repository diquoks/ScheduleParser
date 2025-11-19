import models, data


def main():
    _data = data.DataProvider()

    weekdays_max_len = max([len(str(weekday)) for weekday in models.Weekdays])

    for weekday in models.Weekdays:
        print(f"{str(weekday).ljust(weekdays_max_len)} {_data.bells.get_variant_by_weekday(weekday).bells}")


if __name__ == "__main__":
    main()
