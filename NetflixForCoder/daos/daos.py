# database access object
from flask import jsonify

class Datadaos():
    def __init__(self,cluster):
        self.cluster = cluster

    def get_by_topic(self, topic):
        collection = ["DS","ALGO","Misc","Productivity"]
        cursors = self.cluster.db.collection.find_one({"topic" : topic})

        
            
                
   