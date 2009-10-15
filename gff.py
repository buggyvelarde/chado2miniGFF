import sys

from model import Feature, ObjectRelationship
from business import GFFQueries
from format import GFFFormatter
from util import getArg, dolog
from init import host, database, user, password

def gffTopLevelFeature(gffQueries, feature):
    rows = gffQueries.getGFF3View(feature.feature_id)
    dolog(feature.uniquename)
    feature_ids = []
    for r in rows:
        feature_ids.append(r[0])

    relations = gffQueries.getRelations("objects", feature_ids)
    residues = gffQueries.getResidues(feature.feature_id)
    
    if residues == None:
    	residues = ""

    gffFormatter = GFFFormatter(feature, rows, relations, residues)
    gffFormatter.parse()
    format = gffFormatter.format()
    
    # try to stop leaks...
    gffFormatter = None
    relations = None
    residues = None
    
    return format


if __name__ == "__main__":
    
    featureUniqueName = getArg("featureUniqueName")
    if featureUniqueName == None or len(featureUniqueName) == 0:
        raise Exception("Please supply a feature uniquename using the -featureUniqueName argument")
    
    gffQueries = GFFQueries(host, database, user, password)
    
    featureID = gffQueries.getFeatureIDFromUniqueName(featureUniqueName)
    
    if featureID == None:
        raise Exception("Sorry, this uniquename has not been recognised.")
    
    feature = Feature(featureUniqueName, featureID)
    
    print gffTopLevelFeature(gffQueries, feature)
    





