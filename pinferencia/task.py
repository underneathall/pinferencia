"""All the supported task type"""

# General Task
RAW_REQUEST = "raw_request"
IMAGE_TO_TEXT = "image_to_text"
IMAGE_TO_IMAGE = "image_to_image"
TEXT_TO_TEXT = "text_to_text"
TEXT_TO_IMAGE = "text_to_image"

# Specific Task
TRANSLATION = "translation"
IMAGE_CLASSIFICATION = "image_classification"
IMAGE_STYLE_TRANSFER = "image_style_transfer"
CAMERA_IMAGE_TO_IMAGE = "camera_image_to_image"
CAMERA_IMAGE_TO_TEXT = "camera_image_to_text"

BUILT_IN_TASKS = (
    RAW_REQUEST,
    TRANSLATION,
    IMAGE_CLASSIFICATION,
    IMAGE_STYLE_TRANSFER,
    CAMERA_IMAGE_TO_IMAGE,
    CAMERA_IMAGE_TO_TEXT,
    IMAGE_TO_TEXT,
    IMAGE_TO_IMAGE,
    TEXT_TO_TEXT,
    TEXT_TO_IMAGE,
)
