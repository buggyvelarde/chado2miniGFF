class Feature(object):
    def __init__(self, uniquename, feature_id):
        self.uniquename = uniquename
        self.feature_id = feature_id

class SubjectRelationship(object):
    def __init__(self, subject_id, object_id, object_uniquename, type):
        self.subject_id = subject_id
        self.object_id = object_id
        self.type = type
        self.object_uniquename = object_uniquename

class ObjectRelationship(object):
    def __init__(self, object_id, subject_id, subject_uniquename, type):
        self.object_id = object_id
        self.subject_id = subject_id
        self.type = type
        self.subject_uniquename = subject_uniquename