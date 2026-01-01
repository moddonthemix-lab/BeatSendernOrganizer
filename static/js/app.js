// Global state
let config = null;

// Initialize app on page load
document.addEventListener('DOMContentLoaded', function() {
    checkHealth();
    loadConfig();
    loadBeats();
    setupFileInput();
    setupUploadForm();
});

// Tab Management
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName + 'Tab').classList.add('active');

    // Add active to clicked button
    event.target.classList.add('active');

    // Load data for specific tabs
    if (tabName === 'library') {
        loadBeats();
    } else if (tabName === 'artists') {
        loadConfig();
    }
}

// Health Check
async function checkHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();

        const statusDiv = document.getElementById('emailStatus');

        if (data.email_configured) {
            statusDiv.textContent = '✓ Email configured';
            statusDiv.className = 'status-indicator healthy';
        } else {
            statusDiv.textContent = '⚠ Email not configured - configure .env to send emails';
            statusDiv.className = 'status-indicator warning';
        }
    } catch (error) {
        const statusDiv = document.getElementById('emailStatus');
        statusDiv.textContent = '✗ Connection error';
        statusDiv.className = 'status-indicator error';
    }
}

// Load Configuration
async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        config = await response.json();

        // Populate genre selects
        populateGenreSelects();

        // Display artists management
        displayGenresManagement();

    } catch (error) {
        console.error('Error loading config:', error);
        showMessage('Error loading configuration', 'error');
    }
}

// Populate genre dropdowns
function populateGenreSelects() {
    const genreSelect = document.getElementById('genre');
    const sendGenreSelect = document.getElementById('sendGenre');

    // Clear existing options (except first)
    genreSelect.innerHTML = '<option value="">Choose a genre...</option>';
    sendGenreSelect.innerHTML = '<option value="">Choose a genre...</option>';

    if (config && config.genres) {
        config.genres.forEach(genre => {
            const option1 = document.createElement('option');
            option1.value = genre.name;
            option1.textContent = genre.name.toUpperCase();
            genreSelect.appendChild(option1);

            const option2 = document.createElement('option');
            option2.value = genre.name;
            option2.textContent = genre.name.toUpperCase();
            sendGenreSelect.appendChild(option2);
        });
    }
}

// Load artists for selected genre (upload form)
function loadGenreArtists() {
    const genreSelect = document.getElementById('genre');
    const genre = genreSelect.value;

    if (!genre) {
        document.getElementById('artistsGroup').style.display = 'none';
        return;
    }

    const genreData = config.genres.find(g => g.name === genre);

    if (genreData && genreData.artists.length > 0) {
        const artistsList = document.getElementById('artistsList');
        artistsList.innerHTML = '';

        genreData.artists.forEach((artist, index) => {
            const checkbox = document.createElement('label');
            checkbox.className = 'artist-checkbox';
            checkbox.innerHTML = `
                <input type="checkbox" name="artist" value="${index + 1}">
                <span>${artist.name} (${artist.email})</span>
            `;
            artistsList.appendChild(checkbox);
        });

        document.getElementById('artistsGroup').style.display = 'block';
    } else {
        document.getElementById('artistsGroup').style.display = 'none';
    }
}

// Load artists for send form
function loadSendArtists() {
    const genreSelect = document.getElementById('sendGenre');
    const genre = genreSelect.value;

    if (!genre) {
        document.getElementById('sendArtistsGroup').style.display = 'none';
        return;
    }

    const genreData = config.genres.find(g => g.name === genre);

    if (genreData && genreData.artists.length > 0) {
        const artistsList = document.getElementById('sendArtistsList');
        artistsList.innerHTML = '';

        genreData.artists.forEach((artist, index) => {
            const checkbox = document.createElement('label');
            checkbox.className = 'artist-checkbox';
            checkbox.innerHTML = `
                <input type="checkbox" name="sendArtist" value="${index + 1}">
                <span>${artist.name} (${artist.email})</span>
            `;
            artistsList.appendChild(checkbox);
        });

        document.getElementById('sendArtistsGroup').style.display = 'block';
    } else {
        document.getElementById('sendArtistsGroup').style.display = 'none';
    }
}

// File Input Setup
function setupFileInput() {
    const fileInput = document.getElementById('beatFile');
    const fileName = document.getElementById('fileName');

    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            fileName.textContent = e.target.files[0].name;
            fileName.classList.add('has-file');
        } else {
            fileName.textContent = 'No file chosen';
            fileName.classList.remove('has-file');
        }
    });

    // Make the label clickable
    fileName.addEventListener('click', function() {
        fileInput.click();
    });
}

// Setup Upload Form
function setupUploadForm() {
    const form = document.getElementById('uploadForm');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = new FormData();
        const fileInput = document.getElementById('beatFile');
        const genre = document.getElementById('genre').value;
        const sendEmail = document.getElementById('sendEmail').checked;

        // Add file
        if (fileInput.files.length === 0) {
            showUploadMessage('Please select a file', 'error');
            return;
        }

        formData.append('file', fileInput.files[0]);
        formData.append('genre', genre);
        formData.append('sendEmail', sendEmail);

        // Get selected artists
        const selectedArtists = [];
        document.querySelectorAll('input[name="artist"]:checked').forEach(cb => {
            selectedArtists.push(cb.value);
        });

        if (selectedArtists.length > 0) {
            formData.append('artists', selectedArtists.join(','));
        }

        // Show progress
        document.getElementById('uploadProgress').style.display = 'block';
        document.getElementById('uploadResult').style.display = 'none';
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span>⏳ Uploading...</span>';

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok && result.success) {
                let message = `✓ ${result.message}`;
                if (result.sent !== undefined) {
                    message += `\n📧 Emails sent: ${result.sent}`;
                    if (result.failed > 0) {
                        message += ` | Failed: ${result.failed}`;
                    }
                }
                showUploadMessage(message, 'success');

                // Reset form
                form.reset();
                document.getElementById('fileName').textContent = 'No file chosen';
                document.getElementById('fileName').classList.remove('has-file');
                document.getElementById('artistsGroup').style.display = 'none';

                // Reload beats library
                loadBeats();
            } else {
                showUploadMessage('✗ ' + (result.error || 'Upload failed'), 'error');
            }
        } catch (error) {
            showUploadMessage('✗ Error: ' + error.message, 'error');
        } finally {
            document.getElementById('uploadProgress').style.display = 'none';
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<span id="uploadBtnText">📤 Upload & Organize</span>';
        }
    });
}

// Show upload message
function showUploadMessage(message, type) {
    const resultDiv = document.getElementById('uploadResult');
    resultDiv.textContent = message;
    resultDiv.className = `result-message ${type}`;
    resultDiv.style.display = 'block';
}

// Load Beats Library
async function loadBeats() {
    const libraryDiv = document.getElementById('beatsLibrary');
    libraryDiv.innerHTML = '<p class="loading">Loading beats...</p>';

    try {
        const response = await fetch('/api/beats');
        const data = await response.json();

        if (data.beats && data.beats.length > 0) {
            // Group by genre
            const groupedBeats = {};
            data.beats.forEach(beat => {
                if (!groupedBeats[beat.genre]) {
                    groupedBeats[beat.genre] = [];
                }
                groupedBeats[beat.genre].push(beat);
            });

            // Display
            let html = '';
            for (const [genre, beats] of Object.entries(groupedBeats)) {
                html += `
                    <div class="genre-section">
                        <h3>${genre.toUpperCase()} (${beats.length} beat${beats.length !== 1 ? 's' : ''})</h3>
                        ${beats.map(beat => `
                            <div class="beat-item">
                                <span class="beat-name">🎵 ${beat.filename}</span>
                            </div>
                        `).join('')}
                    </div>
                `;
            }

            libraryDiv.innerHTML = html;
        } else {
            libraryDiv.innerHTML = '<div class="empty-state"><p>No beats organized yet. Upload your first beat!</p></div>';
        }
    } catch (error) {
        libraryDiv.innerHTML = '<div class="error">Error loading beats: ' + error.message + '</div>';
    }
}

// Display Genres Management
function displayGenresManagement() {
    const genresListDiv = document.getElementById('genresList');

    if (!config || !config.genres) {
        genresListDiv.innerHTML = '<p class="loading">Loading...</p>';
        return;
    }

    let html = '';

    config.genres.forEach((genre, genreIndex) => {
        html += `
            <div class="genre-card">
                <h3>${genre.name}</h3>
                <div id="artists-${genreIndex}">
                    ${genre.artists.map((artist, artistIndex) => `
                        <div class="artist-item">
                            <input type="text"
                                   placeholder="Artist Name"
                                   value="${artist.name}"
                                   onchange="updateArtist(${genreIndex}, ${artistIndex}, 'name', this.value)">
                            <input type="email"
                                   placeholder="Email"
                                   value="${artist.email}"
                                   onchange="updateArtist(${genreIndex}, ${artistIndex}, 'email', this.value)">
                            <button class="remove-artist-btn" onclick="removeArtist(${genreIndex}, ${artistIndex})">✕</button>
                        </div>
                    `).join('')}
                </div>
                <button class="add-artist-btn" onclick="addArtist(${genreIndex})">+ Add Artist</button>
            </div>
        `;
    });

    genresListDiv.innerHTML = html;
}

// Update artist
function updateArtist(genreIndex, artistIndex, field, value) {
    config.genres[genreIndex].artists[artistIndex][field] = value;
}

// Add artist
function addArtist(genreIndex) {
    config.genres[genreIndex].artists.push({
        name: '',
        email: ''
    });
    displayGenresManagement();
}

// Remove artist
function removeArtist(genreIndex, artistIndex) {
    if (confirm('Remove this artist?')) {
        config.genres[genreIndex].artists.splice(artistIndex, 1);
        displayGenresManagement();
    }
}

// Save Configuration
async function saveConfig() {
    try {
        const response = await fetch('/api/config/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            alert('✓ Configuration saved successfully!');
            loadConfig();
        } else {
            alert('✗ Error saving configuration: ' + (result.error || 'Unknown error'));
        }
    } catch (error) {
        alert('✗ Error: ' + error.message);
    }
}

// Send Beats
async function sendBeats() {
    const genre = document.getElementById('sendGenre').value;

    if (!genre) {
        showSendMessage('Please select a genre', 'error');
        return;
    }

    // Get selected artists
    const selectedArtists = [];
    document.querySelectorAll('input[name="sendArtist"]:checked').forEach(cb => {
        selectedArtists.push(parseInt(cb.value));
    });

    showSendMessage('📧 Sending beats...', 'info');

    try {
        const response = await fetch('/api/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                genre: genre,
                artists: selectedArtists.length > 0 ? selectedArtists : null
            })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showSendMessage(`✓ ${result.message}\n📧 Sent: ${result.sent} | Failed: ${result.failed}`, 'success');
        } else {
            showSendMessage('✗ ' + (result.error || 'Send failed'), 'error');
        }
    } catch (error) {
        showSendMessage('✗ Error: ' + error.message, 'error');
    }
}

// Send All Beats
async function sendAllBeats() {
    if (!confirm('Send ALL beats from ALL genres? This will send all organized beats to their respective artists.')) {
        return;
    }

    showSendMessage('📧 Sending all beats...', 'info');

    try {
        const response = await fetch('/api/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sendAll: true
            })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showSendMessage(
                `✓ ${result.message}\n` +
                `📁 Genres: ${result.genres_processed}\n` +
                `📧 Sent: ${result.total_sent} | Failed: ${result.total_failed}`,
                'success'
            );
        } else {
            showSendMessage('✗ ' + (result.error || 'Send failed'), 'error');
        }
    } catch (error) {
        showSendMessage('✗ Error: ' + error.message, 'error');
    }
}

// Show send message
function showSendMessage(message, type) {
    const resultDiv = document.getElementById('sendResult');
    resultDiv.innerHTML = message.replace(/\n/g, '<br>');
    resultDiv.className = `result-message ${type}`;
    resultDiv.style.display = 'block';
}

// Helper function for general messages
function showMessage(message, type) {
    alert(message);
}
