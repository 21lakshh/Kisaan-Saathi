document.addEventListener('DOMContentLoaded', function() {
    const uploadBtn = document.getElementById('upload-btn');
    const imageUpload = document.getElementById('image-upload');
    const imageContainer = document.getElementById('image-container');
    const imagePreview = document.getElementById('image-preview');
    const removeBtn = document.getElementById('remove-image');
    const languageSelect = document.getElementById('language-select');
    const submitQuery = document.getElementById('submit-query');
    const responseContainer = document.getElementById('response-container');
    const errorContainer = document.getElementById('error-container');
    const errorText = document.getElementById('error-text');
    console.log("Script loaded and event listeners attached.");


    function getFormattedDateTime() {
        let now = new Date();
    
        let year = now.getFullYear();
        let month = String(now.getMonth() + 1).padStart(2, '0');
        let day = String(now.getDate()).padStart(2, '0');
        let hours = String(now.getHours()).padStart(2, '0');
        let minutes = String(now.getMinutes()).padStart(2, '0');
        let seconds = String(now.getSeconds()).padStart(2, '0');
    
        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    }
    // Click to Upload button trigger
    let isClicking = false;

    uploadBtn.addEventListener('click', function () {
        if (isClicking) return; // Prevent multiple clicks
        isClicking = true;
    
        imageUpload.click();
    
        setTimeout(() => isClicking = false, 500); // Reset after 500ms
    });

    // Handle image selection
    imageUpload.addEventListener('change', function(event) {
        console.log("Image selected:", event.target.files[0]);
        const file = event.target.files[0];
        
        if (!file) return;
        
        if (!file.type.startsWith('image/')) {
            showError('⚠️ Please upload an image file');
            return;
        }
        
        if (file.size > 2 * 1024 * 1024) {
            showError('⚠️ File size should be less than 2MB');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imageContainer.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    });

    // Handle image removal
    removeBtn.addEventListener('click', function() {
        imagePreview.src = '';
        imageContainer.classList.add('hidden');
        imageUpload.value = ''; // Clear the file input
    });

    // Submit Selected language
    submitQuery.addEventListener('click', async (event) => {
        event.preventDefault();
        const image = imageUpload.files[0];
        const selectedLanguage = languageSelect.value;

        // Enhanced validation
        if (!image) {
            showError('⚠️ Please upload an image before submitting.');
            return;
        }
        if (!selectedLanguage) {
            showError('⚠️ Please select a language.');
            return;
        }

        // Log the selected language for debugging
        console.log('Selected language:', selectedLanguage);
        console.log('Language type:', typeof selectedLanguage);

        const formData = new FormData();
        formData.append('file', image);
        formData.append('selected_language', selectedLanguage);
        
        try {
            submitQuery.disabled = true;
            submitQuery.textContent = 'Processing... ⏳';

            console.log('Sending request with:', {
                imageName: image.name,
                imageSize: image.size,
                selectedLanguage: selectedLanguage
            });

            const response = await fetch('/disease_prediction', {
                method: 'POST',
                body: formData
            });

            console.log('Response status:', response.status);
            console.log('Response headers:', Object.fromEntries(response.headers.entries()));

            // Get the response text first
            const responseText = await response.text();
            console.log('Raw Server Response:', responseText);

            // Try to parse as JSON
            let result;
            try {
                result = JSON.parse(responseText);
                console.log('Parsed JSON Response:', result);
            } catch (e) {
                console.error('Failed to parse JSON:', e);
                console.error('Response text that failed to parse:', responseText);
                throw new Error(`Server returned invalid JSON: ${responseText.slice(0, 100)}`);
            }

            // Handle HTTP errors
            if (!response.ok) {
                console.error('Server Error Response:', result);
                const errorMessage = result.detail || result.error || `Server Error (${response.status})`;
                throw new Error(errorMessage);
            }

            // Check for error in response
            if (result.error) {
                console.error('Error in response:', result.error);
                throw new Error(result.error);
            }
            
            // Validate response structure
            if (!result.choices?.[0]?.message?.content) {
                console.error('Invalid Response Structure:', result);
                throw new Error('Invalid response structure from server. Expected choices[0].message.content');
            }
            
            // Display the response
            responseContainer.innerHTML = marked.parse(result["choices"][0]["message"]["content"]);
            responseContainer.classList.remove('hidden');
            errorContainer.classList.add('hidden');

        } catch (error) {
            console.error('Detailed Error:', error);
            console.error('Error stack:', error.stack);
            // Handle both string and object errors
            const errorMessage = error.message || (typeof error === 'object' ? JSON.stringify(error) : String(error));
            showError(errorMessage);
        } finally {
            submitQuery.disabled = false;
            submitQuery.textContent = '🚀 Submit Query';
        }
    });

    function showError(message) {
        // Ensure message is a string
        const errorMessage = typeof message === 'string' ? message : JSON.stringify(message);
        errorText.textContent = errorMessage;
        errorContainer.classList.remove('hidden');
        responseContainer.classList.add('hidden');
        imageUpload.value = ''; // Clear the file input on error
    }
});