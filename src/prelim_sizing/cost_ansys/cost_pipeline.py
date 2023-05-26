import src.prelim_sizing.complexity.field as cx
import src.prelim_sizing.complexity.ci_database as db
import src.prelim_sizing.cost_ansys.launch_cost as launch
import src.prelim_sizing.cost_ansys.production_cost as prod
import src.prelim_sizing.cost_ansys.ait_cost as ait

class CostPipeline:

    def __init__(self, sysmass, nsat):
        self.devcost = 0
        self.prodcost = 0
        self.launchcost = 0
        self.aitcost = 0
        self.sysmass = sysmass
        self.sats = nsat
        self.subsystems = 7
        # self.distributions = [0.16,0.12,0.10,0.20,0.12,0.11,0.17]
        self.sbspmass = [0.34, 0.11, 0.3, 0.04, 0.04, 0.1, 0.07]
        self.sbsppower = [0.02, 0.25, 0.28, 0.15, 0.09, 0.16, 0.05]
        self.field = cx.Field(3, -1, 8, 0.3)
        self.ci_database = db.CiDatabase(self.field)
        self.launcher = launch.Launcher(10000000, 100000)
        self.production = prod.Production(self.sats, self.sysmass)
        self.AIT = ait.Ait(self.subsystems, self.sats, self.sysmass)

    def getdevcost(self):
        missionci = 0
        for i in range(len(self.sbspmass)):
            # devP = (self.sbsp[i] - self.distributions[i]) / self.distributions[i]
            # devM = (self.sbsp[i] - self.distributions[i]) / self.distributions[i]
            devP = (self.sbsppower[i] - self.ci_database.distributions[i][4]) / self.ci_database.distributions[i][5]
            devM = (self.sbspmass[i] - self.ci_database.distributions[i][1]) / self.ci_database.distributions[i][2]
            # print(devP, devM)
            missionci = missionci + self.field.getci(devP, devM) * self.ci_database.distributions[i][3]
            # missionci = missionci + self.field.getci(devP, devM) * self.distributions[i]

        slope, intercept, rvalue = self.ci_database.getlinearregressor()
        print(missionci, 'r-value:', rvalue)
        self.devcost = slope * missionci + intercept

    def getprodcost(self):
        self.prodcost = self.production.getcost(self.sysmass, self.sats)

    def getlaunchcost(self):
        self.launchcost = self.launcher.getcost(self.sysmass)

    def getaitcost(self):
        self.aitcost = self.AIT.getcost()

    def populatecost(self):
        self.getdevcost()
        self.getprodcost()
        self.getlaunchcost()
        self.getaitcost()

    def gettotalcost(self):
        cost = self.devcost + self.prodcost + self.launchcost + self.aitcost

        return cost