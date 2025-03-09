import uuid
from datetime import datetime


def generate_unique_id():
    """
    Generates a unique ID using UUID and current timestamp.

    Returns:
        str: A unique ID string.
    """
    unique_id = uuid.uuid4()
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    combined_id = f"{unique_id}-{current_time}"
    return combined_id
