class Formatter():

    def PlaylistFormatter(datas):
        output = []
        for data in datas:
            playlist_data = {
                "topic" : data["topic"],
                "original_src" : data["original_src"],
                "description" : data["description"],
                "docs" : data["docs"],
                "videos" : data["videos"],
                "datetime" : data["datetime"],
                "tags" : data["tags"],
                "unique_id" : data["unique_id"],
                "poster_path": data["poster_path"]
            }
            output.append(playlist_data)
        return output

            