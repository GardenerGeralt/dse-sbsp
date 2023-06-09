import src.database.utils as sdbu

k = sdbu.read()
print(k)
Ix = k["sc MMOI roll"]
Iy = k["sc MMOI pitch"]
Iz = k["sc MMOI yaw"]


print(Ix, Iy, Iz)
