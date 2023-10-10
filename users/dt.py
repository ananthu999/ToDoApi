from datetime import datetime

def get_current_time_formatted():
    """
    Get the current time in the format "%Y-%m-%d %H:%M:%S".

    Returns:
        str: The formatted current time.
    """
    current_time = datetime.utcnow()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

# Usage example:
# formatted_current_time = get_current_time_formatted()
# print(formatted_current_time)
