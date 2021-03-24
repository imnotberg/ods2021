from sportsreference.nfl.roster import Roster, Player

qbs = []
roster = Roster('CHI',slim=True)
x = Player('TrubMi00')
print(['qb'.lower() in x._position if x._position is not None])
