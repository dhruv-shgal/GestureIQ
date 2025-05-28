console.log("JS loaded");

document.addEventListener('DOMContentLoaded', function() {
    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const statusDiv = document.getElementById('status');
    const uploadForm = document.getElementById('uploadForm');

    // Handle file selection via button
    uploadBtn.addEventListener('click', () => {
        fileInput.click();
    });

    // Handle file selection
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            handleFileUpload(fileInput.files[0]);
        }
    });

    // Handle drag and drop
    dropArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropArea.style.background = 'rgba(108, 99, 255, 0.2)';
    });

    dropArea.addEventListener('dragleave', () => {
        dropArea.style.background = 'rgba(108, 99, 255, 0.05)';
    });

    dropArea.addEventListener('drop', (e) => {
        e.preventDefault();
        dropArea.style.background = 'rgba(108, 99, 255, 0.05)';
        
        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    function handleFileUpload(file) {
        console.log('File selected:', file.name);
        
        // Validate file type
        if (!file.name.match(/\.(ppt|pptx)$/i)) {
            showStatus('Please upload a PowerPoint file (.ppt or .pptx)', 'error');
            return;
        }

        // Update form data
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;

        // Show loading status
        showStatus('Uploading presentation...', 'loading');

        // Submit the form
        const formData = new FormData(uploadForm);
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Server response:', data);
            if (data.status === 'success') {
                showStatus('Presentation started successfully! Connect your camera to begin gesture control.', 'success');
                startStatusCheck();
            } else {
                showStatus(data.message || 'Error uploading file', 'error');
            }
        })
        .catch(error => {
            console.error('Upload error:', error);
            showStatus('Error uploading file: ' + error.message, 'error');
        });
    }

    function showStatus(message, type) {
        console.log('Status update:', type, message);
        statusDiv.textContent = message;
        statusDiv.className = `status-message status-${type}`;
        statusDiv.classList.remove('hidden');
    }

    function startStatusCheck() {
        const checkInterval = setInterval(() => {
            fetch('/status')
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Status check:', data);
                    if (!data.is_running) {
                        clearInterval(checkInterval);
                        showStatus('Presentation ended. You can upload a new presentation.', 'success');
                    }
                })
                .catch(error => {
                    console.error('Status check error:', error);
                    clearInterval(checkInterval);
                    showStatus('Error checking presentation status', 'error');
                });
        }, 2000);
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
});
  