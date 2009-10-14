select subject_id, object_id, object_feature.uniquename, cvterm.name 
from feature_relationship 
join cvterm on cvterm.cvterm_id = feature_relationship.type_id 
join feature object_feature on feature_relationship.object_id = object_feature.feature_id 
join feature subject_feature on feature_relationship.subject_id = subject_feature.feature_id 
where subject_id = %s