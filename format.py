class GFFFormatter(object):
    
    def __init__(self, topLevelFeature, mainColumns, relations, residues):
        self.topLevelFeature = topLevelFeature
        self.mainColumns = mainColumns
        self.relations = relations
        self.residues = residues


    def parse(self):
        self.newRows = []
        for row in self.mainColumns:
            
            newRow = []
            
            newRow.append (self.topLevelFeature.uniquename)
            newRow.append("chado")
            newRow.append(row[3])
            newRow.append(row[4])
            newRow.append(row[5])
            newRow.append(".")
            
            phase = "."
            
            if row[7] == -1:
                phase = "-"
            elif row[7] == 1:
                phase = "+"
            
            newRow.append(phase)
            newRow.append(".")
            
            newRow.append( self.getQualifiers(row[0], row[12]) )
            
            self.newRows.append(newRow)
    
    def getQualifiers(self, feature_id, uniquename):
        
        qualifiers = "ID=" + str(feature_id) + ";" + "Name=" + str(uniquename)
        
        theRelations = self.relations.get(feature_id)
        
        if theRelations != None:
            parents = []
            for rel in theRelations:
                if rel.type == "derives_from" or rel.type == "part_of":
                    parents.append(rel.subject_uniquename)
        
            if len(parents) > 0:
                qualifiers += ";Parent=" + ",".join(parents)
        
        return qualifiers
    
    def split_len(self, seq, length):
        return [seq[i:i+length] for i in range(0, len(seq), length)]
    
    
    # outputs the mini-gff
    # generates the string by building a list first
    # shown to be fastest in Python, see
    # http://www.skymind.com/~ocrow/python_string/
    def format(self):
        
        out = []
        
        out.append("##gff-version 3")
        out.append("##sequence-region " +  self.topLevelFeature.uniquename + " 1 " + str(len(self.residues) - 1))

        for row in self.newRows:
            line = ""
            t = ""
            for col in row:
                line += t + str(col)
                t = "\t"
            out.append( line )
        out.append( "##FASTA")
        out.append( ">" + self.topLevelFeature.uniquename )
        chunkedResidues = self.split_len(self.residues, 60)
        out.append("\n".join(chunkedResidues))
        
        return '\n'.join(out)

