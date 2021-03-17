from flask import Flask,jsonify,Blueprint,request
from NetflixForCoder.daos.daos import Datadaos
import uuid
import datetime

def create_blueprint(cluster):
    cypherbyte = Blueprint("cypherbyte",__name__,url_prefix = "/cypherbyte")
    daos = Datadaos(cluster)


    # ADD NEW TOPIC TO A COLLECTION
    @cypherbyte.route("/add",methods=['POST','GET'])      
    def add_playlist():
        if request.method == "POST":
            topic = request.json["topic"]
            original_src = request.json["original_src"]
            description = request.json["description"]
            docs = request.json["docs"]
            videos = request.json["videos"]
            tags = request.json["tags"]
            collection = request.json["collection"]

            insert_obj = {
                "unique_id" : str(uuid.uuid4()),
                "topic" : topic,
                "original_src" : original_src,
                "description" : description,
                "docs" : docs,
                "videos" : videos,
                "tags" : tags,
                "datetime" : datetime.datetime.now()
            }

            response = daos.post_new_topic(insert_obj,collection)
            if response:
                return jsonify({"status" : 200, "message" : "data insertion successfull"})
            return jsonify({"status" : 404, "message" : "data insertion failed"})

        return '<h1>WORKING</h1>'
    #GET DATA ON THE BASIS OF TOPIC
    @cypherbyte.route('/search/topic/<topic>',methods=['GET'])
    def get_by_topic(topic):
        response = daos.get_by_topic(topic)
        if response:
            return jsonify({"status" : 200, "result" : response})
        return jsonify({"status" : 404, "message" : "data not found"})
    

    #GET DATA ON THE BASIS OF TAGNAME
    @cypherbyte.route('/search/tag/<tag>',methods=['GET'])
    def get_by_tagname(tag):
        response = daos.get_by_tagname(tag)
        if response:
            return jsonify({"status" : 200, "result" : response})
        return jsonify({"status" : 404, "message" : "data not found"})
        

    @cypherbyte.route('/add/video',methods = ["GET","POST"])
    def add_video():
            if request.method == "POST":
                topic = request.json["topic"]
                video_title = request.json["video_title"]
                video_link = request.json["video_link"]
                author = request.json["author"]

                insert_vid = {
                    "video_title" : video_title,
                    "video_link" : video_link,
                    "author" : author
                }

                response = daos.post_new_video(insert_vid,topic)

                if response:
                    return jsonify({"status": 200, "message" : "video added successfully"})
                return jsonify({"status" : 404, "message" : "video failed to add"})
            return '<h1>Working</h1>'
    
    
    return cypherbyte