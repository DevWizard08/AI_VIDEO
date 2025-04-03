import cloudinary.uploader

def upload_to_cloudinary(file_path, folder="uploads"):
    """ Cloudinary pe file upload kare aur URL return kare """
    try:
        response = cloudinary.uploader.upload(file_path, resource_type="auto", folder=folder)
        return response.get("secure_url")  
    except Exception as e:
        return str(e)
