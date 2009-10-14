from gff_organism import gffForOrganism

from business import GFFQueries
from util import getArg, dolog
from init import host, database, user, password

def getOrganisms(gffQueries, savePath, organisms = None):
    
    if organisms == None:
        organisms = gffQueries.getAllOrganisms()
    
    for organism in organisms:
        dolog("Exporting for " + organism)
        gffForOrganism(gffQueries, organism, savePath)
    

if __name__ == "__main__":
    
    savePath = getArg("savePath")
    if savePath == None or len(savePath) == 0:
        raise Exception("Please supply a savePath using the -savePath argument")
    
    organisms = getArg("organisms", True)
    
    gffQueries = GFFQueries(host, database, user, password)
    getOrganisms(gffQueries, savePath, organisms)
    
    