function downloadContent() {
    const url = document.getElementById('urlInput').value;
    if (isValidInstagramURL(url)) {
        fetch(`/download?url=${encodeURIComponent(url)}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('downloadLink').style.display = 'block';
                    document.getElementById('downloadButton').href = data.download_url;
                } else {
                    showErrorMessage(data.message);
                }
            })
            .catch(() => {
                showErrorMessage('An error occurred while processing the request.');
            });
    } else {
        showErrorMessage('Invalid Instagram URL');
    }
}

function isValidInstagramURL(url) {
    const regex = /^(https?:\/\/)?(www\.)?instagram\.com\/(?:p|tv|reel)\/([A-Za-z0-9-_]+)/;
    return regex.test(url);
}

function showErrorMessage(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorMessage').style.display = 'block';
    document.getElementById('downloadLink').style.display = 'none';
}
