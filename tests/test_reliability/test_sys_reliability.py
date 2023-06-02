import src.Reliability.sys_reliability as rel


class TestSysReliaibility:
    spacesys = rel.SystemReliability(80,0.95,0.95)
    print('Buffer spacecraft necessary to achieve system level reliability:',spacesys.getBuffer())
    print('Spacecraft reliability per year:',spacesys.getReqSatRel())
    spacesys.costinfo(1098000000, 13700000)
