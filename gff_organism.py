from gff import gffTopLevelFeature

from business import GFFQueries
from util import getArg, mkDir, dolog
from init import host, database, user, password

def gffForOrganism(gffQueries, organism, savePath = None):
    
    organismID = gffQueries.getOrganismIDFromCommonName(organism)
    
    features = gffQueries.getTopLevelFeatures(organismID)
    
    if savePath != None:
        mkDir(savePath)
    
    for feature in features:
        gff = gffTopLevelFeature(gffQueries, feature)
        if savePath == None:
            dolog (gff)
        else:
            filePath = savePath + "/" + feature.uniquename + ".gff"
            dolog("saving : " + filePath)
            out = open(filePath, 'w')
            out.write(gff)
            out.close()
            
        # try to tidy up...
        gff = None


if __name__ == "__main__":

    organism = getArg("organism")
    if organism == None or len(organism) == 0:
        raise Exception("Please supply a organism using the -organism argument")
    
    
    savePath = getArg("savePath")
    if len(savePath) == 0:
        savePath = None
    
    gffQueries = GFFQueries(host, database, user, password)
    gffForOrganism(gffQueries, organism, savePath)