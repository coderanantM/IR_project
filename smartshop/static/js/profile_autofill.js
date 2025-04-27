document.addEventListener('DOMContentLoaded', () => {
    const preferenceInput = document.getElementById('preference-input');
    const processTextBtn = document.getElementById('process-text-btn');
    const voiceInputBtn = document.getElementById('voice-input-btn');
    const voiceStatus = document.getElementById('voice-status');

    const processApiUrl = '/users/api/process-preferences/';

    // Helper function to get CSRF token from cookies
    function getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return null;
    } // Ensure this matches your Django URL configuration

    // --- Helper Function to Update Form ---
    function updateFormFields(data) {
        console.log("Updating form with data:", data);
        let updatedFields = 0;

        const fieldMap = {
            'preferred_department': 'id_preferred_department',
            'height_cm': 'id_height_cm',
            'weight_kg': 'id_weight_kg',
            'age_group': 'id_age_group',
            'preferred_fit': 'id_preferred_fit',
            'budget_min': 'id_budget_min',
            'budget_max': 'id_budget_max'
        };

        for (const key in data) {
            if (data.hasOwnProperty(key) && fieldMap.hasOwnProperty(key)) {
                const fieldId = fieldMap[key];
                const fieldElement = document.getElementById(fieldId);
                if (fieldElement && data[key] !== null && data[key] !== undefined) {
                    fieldElement.value = data[key];
                    updatedFields++;
                    fieldElement.classList.add('is-valid');
                    setTimeout(() => fieldElement.classList.remove('is-valid'), 3000);
                }
            }
        }
        if (updatedFields > 0) {
            alert(`${updatedFields} profile field(s) updated based on your input. Please review and save.`);
        } else {
            alert("Could not automatically update fields based on your input. Please fill them manually.");
        }
    }

    // --- API Call Function ---
    async function sendDataToApi(text) {
        try {
            const response = await fetch(processApiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || `HTTP error! Status: ${response.status}`);
            }

            const result = await response.json();

            if (result.status === 'success') {
                updateFormFields(result.data);
            } else {
                console.error("API Error:", result.message);
                alert(`Error processing input: ${result.message}`);
            }
        } catch (error) {
            console.error('Fetch Error:', error);
            alert(`An error occurred: ${error.message}`);
        } finally {
            voiceStatus.textContent = '';
        }
    }

    // --- Event Listener for Text Button ---
    processTextBtn.addEventListener('click', () => {
        const text = preferenceInput.value.trim();
        if (text) {
            voiceStatus.textContent = 'Processing text...';
            sendDataToApi(text);
        } else {
            alert('Please enter your preferences in the text box.');
        }
    });

    // --- Event Listener and Logic for Voice Button ---
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';
        recognition.interimResults = false;

        voiceInputBtn.addEventListener('click', () => {
            voiceStatus.textContent = 'Listening...';
            voiceInputBtn.disabled = true;
            recognition.start();
        });

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            preferenceInput.value = transcript;
            voiceStatus.textContent = 'Processing voice input...';
            sendDataToApi(transcript);
        };

        recognition.onspeechend = () => {
            recognition.stop();
            voiceStatus.textContent = 'Finished listening.';
            voiceInputBtn.disabled = false;
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            voiceStatus.textContent = `Error: ${event.error}`;
            voiceInputBtn.disabled = false;
        };

        recognition.onnomatch = () => {
            voiceStatus.textContent = "Didn't recognize that. Please try again.";
            voiceInputBtn.disabled = false;
        };
    } else {
        voiceInputBtn.disabled = true;
        voiceStatus.textContent = 'Voice recognition not supported by your browser.';
    }
});

async function sendDataToApi(text) {
    try {
        const csrfToken = getCSRFToken();
        if (!csrfToken) {
            throw new Error('CSRF token not found. Ensure you are logged in and CSRF cookies are set.');
        }

        const response = await fetch(processApiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken, // Include CSRF token in the headers
            },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        if (result.status === 'success') {
            updateFormFields(result.data);
        } else {
            alert(`Error processing input: ${result.message}`);
        }
    } catch (error) {
        console.error('Fetch Error:', error);
        alert(`An error occurred: ${error.message}`);
    } finally {
        voiceStatus.textContent = '';
    }
}

processTextBtn.addEventListener('click', () => {
    const text = preferenceInput.value.trim();
    if (text) {
        voiceStatus.textContent = 'Processing text...';
        sendDataToApi(text);
    } else {
        alert('Please enter your preferences in the text box.');
    }
});
