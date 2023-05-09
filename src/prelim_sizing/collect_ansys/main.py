import collect_methods as cm


def main():
    return None


if __name__ == "__main__":

    azur_quad_junct = cm.PhotoCell(0.32, 3.018e-3, 1.780e-3, 1)
    print(azur_quad_junct)

    azur_trip_junct = cm.PhotoCell(0.30, 2.651e-3, 2.350e-3, 1)
    print(azur_trip_junct)

    cesi_trip_junct = cm.PhotoCell(0.295, 2.650e-3, 2.349e-3, 1)     # guessed mass value
    print(cesi_trip_junct)

    main()
