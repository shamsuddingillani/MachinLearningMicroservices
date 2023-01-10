from deepface import DeepFace


def load_model():
    model = DeepFace.build_model("Facenet")

    return model