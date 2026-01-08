import time
from huey.contrib.djhuey import task, signal
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.files.storage import default_storage

@task(retries=3, retry_delay=60)
def generate_large_file() -> str:
    """ (Task queue) Generate a large file and return the file path """

    # Simulate a long running task
    time.sleep(5)

    # Generate a large file
    file_path = f'large_file_{timezone.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt' # Starting from the media root
    with default_storage.open(file_path, 'w') as file:
        file.write('This is a generated large file. We slowed it down to simulate a long running task, but in reality, this could be a large file that takes a while to generate.')

    return file_path