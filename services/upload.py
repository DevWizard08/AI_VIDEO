import cloudinary.uploader
import os
import io

def upload_to_cloudinary(file_input, folder="uploads"):
    """
    Uploads a file to Cloudinary and returns the secure URL.
    Supports both file paths and in-memory files (like BytesIO).
    """
    try:
        if isinstance(file_input, (io.BytesIO, io.BufferedReader)):
            response = cloudinary.uploader.upload(
                file_input,
                resource_type="auto",
                folder=folder
            )
        elif isinstance(file_input, str) and os.path.exists(file_input):
            response = cloudinary.uploader.upload(
                file_input,
                resource_type="auto",
                folder=folder
            )
        else:
            raise ValueError("Unsupported input: must be file path or file-like object")

        return response.get("secure_url")

    except Exception as e:
        return str(e)
