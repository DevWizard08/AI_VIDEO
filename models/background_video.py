class BackgroundVideo:
    collection = None

    @staticmethod
    def save_video(video_url):
        result = BackgroundVideo.collection.insert_one({"video_url": video_url})
        return str(result.inserted_id)
