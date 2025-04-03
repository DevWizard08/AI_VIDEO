from bson.objectid import ObjectId

class Video:
    collection = None  
    @staticmethod
    def save_video(audio_url, video_url, text):
        video_data = {
            "text": text,
            "audio_url": audio_url,
            "video_url": video_url
        }
        result = Video.collection.insert_one(video_data)
        return str(result.inserted_id)