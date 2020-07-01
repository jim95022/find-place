def detect_landmarks(path):
    """Detects landmarks in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations

    for landmark in landmarks:
        desc = landmark.description
        for location in landmark.locations:
            lat_lng = location.lat_lng
            lat = lat_lng.latitude
            lng = lat_lng.longitude

            return lat, lng, desc
            