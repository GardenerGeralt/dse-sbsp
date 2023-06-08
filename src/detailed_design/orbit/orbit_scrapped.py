# Old sats in view
'''
        if self.index.size > 0:
            l1 = cos(RAAN) * cos(AOP) - sin(RAAN) * sin(AOP) * cos(INC)
            l2 = -cos(RAAN) * sin(AOP) - sin(RAAN) * cos(AOP) * cos(INC)
            m1 = sin(RAAN) * cos(AOP) + cos(RAAN) * sin(AOP) * cos(INC)
            m2 = -sin(RAAN) * sin(AOP) + cos(RAAN) * cos(AOP) * cos(INC)
            n1 = sin(AOP) * sin(INC)
            n2 = cos(AOP) * sin(INC)

            # Find normal vector
            plane_2D = [[0, 1], [1, 0]]
            plane_3D = []
            transform = np.array([[l1, l2], [m1, m2], [n1, n2]])
            for i in range(2):
                plane_3D.append(np.matmul(transform, plane_2D[i]))
            normal_vec = np.cross(plane_3D[0], plane_3D[1])

            ref = position3D(SMA, ECC, INC, RAAN, AOP, TA=deg2rad(0))
            self.angles = []
            for i in range(0, -2, -1):
                point = np.array(
                    [
                        self.orbit[0][self.trans_idx[i]],
                        self.orbit[1][self.trans_idx[i]],
                        self.orbit[2][self.trans_idx[i]],
                    ]
                )

                # Find angle
                dot = np.dot(ref, point)
                det = (
                    ref[0] * point[1] * normal_vec[2]
                    + point[0] * normal_vec[1] * ref[2]
                    + normal_vec[0] * ref[1] * point[2]
                    - ref[2] * point[1] * normal_vec[0]
                    - point[2] * normal_vec[1] * ref[0]
                    - normal_vec[2] * ref[1] * point[0]
                )
                TA_point = -1 * np.arctan2(det, dot)
                if TA_point < 0:
                    TA_point = 2 * np.pi + TA_point
                self.angles.append(TA_point)

            # Integrate ellipse equation
            b = np.sqrt(SMA**2 * (1 - ECC**2))
            m = ECC**2
            perim = 4 * SMA * ellipe(m)
            spacing = perim / n_sat

            T0, T1 = self.angles[0], self.angles[1]
            t0 = ellipeinc(T0 - 0.5 * np.pi, m)
            t1 = ellipeinc(T1 - 0.5 * np.pi, m)
            arclength = SMA * (t1 - t0)
        if self.trans_idx.size == 0:
            arclength = float("NaN")
            spacing = float("NaN")
        sat_in_view = arclength / spacing
        '''