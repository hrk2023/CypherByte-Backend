# database access object
from flask import jsonify
from NetflixForCoder.routes.dataArranger import Formatter
class Datadaos:
    def __init__(self,cluster):
        self.cluster = cluster

    def check_topic(topic,col=None):
        cluster = self.cluster.db
        if(col is not None):
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
                return True
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
        cluster = self.cluster.db
        col = cluster[col]
        # col = check_topic(topic,col)
        # if col:
        #     return col.update_one({"topic" : topic},{"$set" : data})
        # else:
        return col.insert_one(data)
            
    def post_new_video(self,data,topic):
        col = check_topic(topic)
        if col:
            return col.update_one({"topic" : topic},{"$set" : {"videos" : data}})
        else: 
            return False
                
   