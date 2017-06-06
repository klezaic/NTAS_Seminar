class MoviesData:

    def __init__ (self, ID, shortName, longName):
        self.ID = ID
        self.shortName = shortName
        self.longName = longName

    def __lt__(self, other):
        return self.shortName < other.shortName

    def __le__(self, other):
        return self.shortName <= other.shortName

    def __gt__(self, other):
        return self.shortName > other.shortName

    def __ge__(self, other):
        return self.shortName >= other.shortName

    def __getitem__(self,index):
        return self.shortName

    def __str__(self):
        return "ID: " + str(self.ID) + "\tshortName: " + self.shortName + "\tlongName: " + self.longName
