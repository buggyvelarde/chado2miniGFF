import psycopg2
import sys

from model import Feature, ObjectRelationship, SubjectRelationship
from util import dolog


class GFFQueries(object):
    
    def __init__(self, host, database, user, password):
        
        self.conn = psycopg2.connect("dbname='" + database + "' user='" + user + "' host='" + host + "' password='" + password + "'");
        self.cur = self.conn.cursor()
        
        self.queries = {}
        self.queries['gff3view'] = self.getQueryFromFile("gff3view.sql")
        self.queries["subjects"] = self.getQueryFromFile("getSubjectRelations.sql") 
        self.queries["objects"] = self.getQueryFromFile("getObjectRelations.sql") 
        self.queries["residues"] = self.getQueryFromFile("residues.sql") 
    
    def getQueryFromFile(self, fileName):
        filePath = self.sqlFilePath()
        return "\n".join (open(filePath + fileName, 'r').readlines())
    
    def sqlFilePath(self):
        return sys.path[0] + "/sql/" 
    
    def getQuery(self, queryName):
        return self.queries.get(queryName)
    
    def getTopLevelFeatures(self, organism):
    	dolog("getting top level features for " + str(organism))
        query  = "select f.uniquename,f.feature_id from feature f "
        query += "join cvterm on f.type_id = cvterm.cvterm_id "
        query += "join featureprop using (feature_id) "
        query += "where f.organism_id= "

        query += str(organism)

        query += " and featureprop.type_id in "
        query += "  (select cvterm_id from cvterm join cv using (cv_id) where cv.name = 'genedb_misc' and cvterm.name = 'top_level_seq') "

        # query += " and f.type_id not in ('432', '1087') "

        query += "order by uniquename ";
        
        self.cur.execute(query)
        rows = self.cur.fetchall()
        
        features = []
        for row in rows:
            # print row
            feature = Feature(row[0], row[1])
            features.append(feature)
        return features
        
        
    def getAllOrganisms(self):
        query = " select common_name from organism ";
        self.cur.execute(query)
        rows = self.cur.fetchall()
        common_names = []
        for row in rows:
            value = row[0]
            if value == "dummy":
                continue
            common_names.append(value)
        return common_names
    
    def getOrganismIDFromCommonName(self, commonName):
        # print commonName
        query  = " select organism_id from organism where common_name = '" + commonName + "'"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        for row in rows:
            # print row[0]
            return int(row[0])
    
    def getFeatureIDFromUniqueName(self, uniquename):
        query = " select feature_id from feature where uniquename = '" + uniquename + "' "
        self.cur.execute(query, (uniquename, ))
        rows = self.cur.fetchall()
        for row in rows:
            return row[0]
        
    def getResidues(self, feature_id):
        query = self.getQuery("residues")
        self.cur.execute(query, (feature_id, ))
        rows = self.cur.fetchall()
        for row in rows:
            return row[0]

    
    def getGFF3View(self, sourceFeatureId):
        query = self.getQuery("gff3view")
        self.cur.execute(query, (sourceFeatureId, ))
        rows = self.cur.fetchall()
        return rows
    
    def getRelations(self, relationType, feature_ids):
        results = {}
        
        if relationType != "subjects" and relationType != "objects":
            raise "Invalid relation " + relationType
        
        for feature_id in feature_ids:
            
            query = self.getQuery(relationType)
            
            self.cur.execute(query, (feature_id, ))
            rows = self.cur.fetchall()
            
            rels = []
            
            for r in rows:
                # print r
                
                if relationType == "subjects":
                    rel = SubjectRelationship(r[0], r[1], r[2], r[3])
                else:
                    rel = ObjectRelationship(r[0], r[1], r[2], r[3])
                
                rels.append(rel)
                
            results[feature_id] = rels
        
        return results
