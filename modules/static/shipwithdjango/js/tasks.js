/**
 * This file contains functions for handling tasks.
 */

/**
 * Check the status of a task that generates a file for download.
 * If the task has been completed, the file will be downloaded. Otherwise it will check again in 2 seconds.
 * @param {string} taskId - The id of the task.
 * @param {function} successCallback - The function that will be called when the task is completed.
 * @returns {void}
 * @example
 * checkFileTaskStatus('d8f7b5c9-4e0c-4d1e-8e6b-4c7f5a2b3a6e');
 */
function checkFileTaskStatus(taskId, successCallback = undefined) {

    var processing = true;

    fetch(`/swd/utils/check-file-task-status/${taskId}/`)
        .then(response => {
            // When the task is still being processed, it will return a 202 status code.
            // When the task is completed, it will return a 200 status code.

            if (response.status === 200) {
                processing = false;

                // Retrieve the filename from the Content-Disposition header
                const contentDisposition = response.headers.get('Content-Disposition');
                let filename = 'downloaded_file';

                if (contentDisposition) {
                    const matches = contentDisposition.match(/filename=([^;]+)/);
                    if (matches && matches[1]) {
                        filename = matches[1].trim();
                    }
                }

                return response.blob().then(blob => ({ filename, blob }));

            } else {
                return response.json();
            }
        })
        .then(data => {
            if (processing) {
                setTimeout(() => checkFileTaskStatus(taskId, successCallback), 2000);
            } else if(!processing) {
                const { filename, blob } = data;
                var url = URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                a.remove();
                URL.revokeObjectURL(url);

                if (successCallback) {
                    successCallback();
                }
            }
        })
}