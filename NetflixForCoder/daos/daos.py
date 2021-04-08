# database access object
from flask import jsonify
from NetflixForCoder.routes.dataArranger import Formatter
class Datadaos:
    def __init__(self,cluster):
        self.cluster = cluster

    def check_topic(self,topic,col=None):
        cluster = self.cluster.db
        if col is None:
            collections = cluster.collection_names()
            for i in collections:
                collection = cluster[i]
                response = collection.find_one({"topic": 
                {'$regex' : '^{}'.format(topic),'$options' : 'i'}
                })
                if response:
                    return collection
            return False
        else:
            collection = cluster[col]
            response = collection.find_one({"topic": 
                {'$regex' : '^{}'.format(topic),'$options' : 'i'}
                })
            if response:
                return collection
            return False

    def get_by_col(self, col):
        cluster = self.cluster.db
        collections = cluster.collection_names()
        if col in collections:
            collection = cluster[col]
            response = collection.find()
            if response:
                result = Formatter.PlaylistFormatter(response)
                return result
        return False

    def get_by_topic(self, topic):
        cluster = self.cluster.db
        collections = cluster.collection_names()
        for i in collections:
            collection = cluster[i]
            response = collection.find({"topic": 
            {'$regex' : '^{}'.format(topic),'$options' : 'i'}
            })
            if response:
                result = Formatter.PlaylistFormatter(response)
                return result
        return False

    def get_by_tagname(self, tagname):
        cluster = self.cluster.db
        collections = cluster.collection_names()
        for i in collections:
            collection = cluster[i]
            response = collection.find({"tags": 
            {'$regex' : '^{}'.format(tagname),'$options' : 'i'}
            })
            if response:
                result = Formatter.PlaylistFormatter(response)
                return result
        return False

    def post_new_topic(self,data,col):
        topic = data["topic"]
        collection = self.check_topic(topic,col)
        if collection:
            return collection.update_one({"topic" : topic},{"$set" : data})
        else:
            cluster = self.cluster.db
            col = cluster[col]
            return col.insert_one(data)


    def post_new_video(self,data,topic):
        col = self.check_topic(topic)
        if col:
            return col.update_one({"topic" : topic},{"$push" : {"videos" : data}})
        else: 
            return False
    
    def post_new_doc(self,data,topic):
        col = self.check_topic(topic)
        if col:
            return col.update_one({"topic" : topic},{"$push" : {"docs" : data}})
        else: 
            return False

    def post_new_original_src(self,data,topic):
        col = self.check_topic(topic)
        if col:
            return col.update_one({"topic" : topic},{"$push" : {"original_src" : data}})
        else: 
            return False
                
    def delete_topic(self,topic):
        col = self.check_topic(topic)
        if col:
           return col.delete_one({"topic" : topic})
        else:
            return False
    
