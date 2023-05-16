import orbit_ansys as oa


def main():
    ...


if __name__ == "__main__":
    FLLO = oa.OrbitFromPeri(110000, 0.09547, 84.8, "Frozen low lunar orbit")
    FELO = oa.OrbitFromPeri(750000, 0.5, 48.46, "Frozen elliptical lunar orbit")

    print(FLLO)
    print(FELO)
