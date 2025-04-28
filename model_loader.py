def get_model():
    """Load the model only when explicitly called."""
    from DeepFitClassifier import DeepFitClassifier
    import os

    # Define model path
    model_path = os.path.join(
        os.path.dirname(__file__), 'deepfit_classifier_v3.tflite'
    )

    # Ensure model file exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at path: {model_path}")

    # Initialize and return the model instance
    return DeepFitClassifier(model_path)
