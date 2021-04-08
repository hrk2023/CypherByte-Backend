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
                return jsonify({"status" : 200, "message" : "data insertion successful"})
            return jsonify({"status" : 404, "message" : "data insertion failed"})

        return '<h1>WORKING</h1>'

    
    @cypherbyte.route("/add/bulk",methods=["POST","GET"])
    def add_bulk_playlist():
        if request.method == 'POST':
            bulk_data = request.json["bulk_data"]
            collection = request.json["collection"]
            for data in bulk_data:
                playlist_data = {
                    "topic" : data["topic"],
                    "original_src" : data["original_src"],
                    "description" : data["description"],
                    "docs" : data["docs"],
                    "videos" : data["videos"],
                    "datetime" : datetime.datetime.now(),
                    "tags" : data["tags"],
                    "unique_id" : str(uuid.uuid4()),
                    "poster_path" : data["poster_path"]
                }
                response = daos.post_new_topic(playlist_data,collection)
                if response:
                    continue
                else:
                    return jsonify({"status" : 404, "message" : "data insertion failed for {}".format(data["topic"])})
            return jsonify({"status" : 200, "message" : "data insertion successful"})
        return '<h1>WORKING</h1>'

    #GET ALL DATA OF A SECTION
    @cypherbyte.route('/search/all/<section>',methods=['GET'])
    def get_by_section(section):
        response = daos.get_by_col(section)
        if response:
            return jsonify({"status" : 200, "result" : response})
        return jsonify({"status" : 404, "message" : "data not found"})

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
        
    #ADD NEW VIDEO TO A TOPIC
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

    #ADD NEW DOC TO A TOPIC
    @cypherbyte.route('/add/doc',methods = ["GET","POST"])
    def add_doc():
        if request.method == "POST":
            topic = request.json["topic"]
            doc_name = request.json["doc_name"]
            doc_link = request.json["doc_link"]

            insert_doc = {
                "doc_name" : doc_name,
                "doc_link" : doc_link,
            }

            response = daos.post_new_doc(insert_doc,topic)

            if response:
                return jsonify({"status": 200, "message" : "doc added successfully"})
            return jsonify({"status" : 404, "message" : "doc failed to add"})
        return '<h1>Working</h1>'

    #ADD NEW ORIGINAL_SRC TO A TOPIC
    @cypherbyte.route('/add/ori',methods = ["GET","POST"])
    def add_ori():
        if request.method == "POST":
            topic = request.json["topic"]
            author = request.json["author"]
            channel = request.json["channel"]

            insert_os = {
                "author" : author,
                "channel" : channel,
            }

            response = daos.post_new_orginal_src(insert_os,topic)

            if response:
                return jsonify({"status": 200, "message" : "original src added successfully"})
            return jsonify({"status" : 404, "message" : "original src failed to add"})
        return '<h1>Working</h1>'
    
    @cypherbyte.route('/delete/<topic>', methods=["DELETE"])
    @cypherbyte.route('/delete', methods=['DELETE'])
    def delete_topic(topic = None):
        if topic is not None and request.method == 'DELETE':
            response = daos.delete_topic(topic)
            if response:
                return jsonify({"status": 200, "message" : "topic deleted successfully"})
            return jsonify({"status" : 404, "message" : "topic failed to delete"})
        else:
            topic = request.json["topic"]
            response = daos.delete_topic(topic)
            if response:
                return jsonify({"status": 200, "message" : "topic deleted successfully"})
            return jsonify({"status" : 404, "message" : "topic failed to delete"})
            
    
    return cypherbyte