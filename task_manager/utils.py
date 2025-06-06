import json
import os
from django.test import modify_settings, override_settings


test_english = override_settings(
    LANGUAGE_CODE="en-US",
    LANGUAGES=(("en", "English"),),
)

remove_rollbar = modify_settings(
    MIDDLEWARE={
        "remove": [
            "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
        ]
    }
)


def load_data(path):
    """
    Load JSON data from a fixture file located in the 'task_manager/fixtures'
        directory.

    Args:
        path (str): Relative path to the fixture file (e.g., 'users.json').

    Returns:
        dict or list: Parsed JSON content from the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file content is not valid JSON.
    """
    with open(os.path.abspath(f"task_manager/fixtures/{path}")) as file:
        return json.loads(file.read())
