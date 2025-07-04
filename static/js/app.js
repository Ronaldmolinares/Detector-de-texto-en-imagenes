document.addEventListener('DOMContentLoaded', function() {
    // Elementos DOM
    const uploadSection = document.getElementById('uploadSection');
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const progressContainer = document.getElementById('progressContainer');
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    const resultsSection = document.getElementById('resultsSection');
    const imageResults = document.getElementById('imageResults');
    const processNewBtn = document.getElementById('processNewBtn');
    const downloadAllBtn = document.getElementById('downloadAllBtn');
    const copyAllBtn = document.getElementById('copyAllBtn');
    const messageContainer = document.getElementById('messageContainer');

    // Almacenamiento de resultados
    let allResults = [];

    // Ocultar inicialmente
    progressContainer.style.display = 'none';
    resultsSection.style.display = 'none';

    // Configurar eventos para drag & drop
    uploadSection.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadSection.classList.add('drag-over');
    });

    uploadSection.addEventListener('dragleave', function() {
        uploadSection.classList.remove('drag-over');
    });

    uploadSection.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadSection.classList.remove('drag-over');
        
        if (e.dataTransfer.files.length > 0) {
            handleFiles(e.dataTransfer.files);
        }
    });

    // Configurar eventos para selección de archivos
    uploadBtn.addEventListener('click', function() {
        fileInput.click();
    });

    fileInput.addEventListener('change', function() {
        if (fileInput.files.length > 0) {
            handleFiles(fileInput.files);
        }
    });

    // Procesar nuevas imágenes
    processNewBtn.addEventListener('click', function() {
        uploadSection.style.display = 'flex';
        resultsSection.style.display = 'none';
        allResults = [];
        imageResults.innerHTML = '';
    });

    // Descargar todos los resultados
    downloadAllBtn.addEventListener('click', function() {
        if (allResults.length === 0) return;
        
        let text = '';
        allResults.forEach(result => {
            text += `${result.filename}:\n${result.coordinates}\n${'-'.repeat(60)}\n`;
        });
        
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'coordenadas_formateadas.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showMessage('Texto descargado correctamente', 'success');
    });

    // Copiar todos los resultados
    copyAllBtn.addEventListener('click', function() {
        if (allResults.length === 0) return;
        
        let text = '';
        allResults.forEach(result => {
            text += `${result.filename}:\n${result.coordinates}\n${'-'.repeat(60)}\n`;
        });
        
        navigator.clipboard.writeText(text)
            .then(() => showMessage('Texto copiado al portapapeles', 'success'))
            .catch(() => showMessage('Error al copiar texto', 'error'));
    });

    // Función para procesar archivos
    function handleFiles(files) {
        // Mostrar progreso
        uploadSection.style.display = 'none';
        progressContainer.style.display = 'block';
        progressFill.style.width = '0%';
        progressText.textContent = 'Procesando (0/' + files.length + ')';
        
        let processed = 0;
        allResults = [];

        // Procesar cada archivo
        Array.from(files).forEach(file => {
            const formData = new FormData();
            formData.append('image', file);
            
            fetch('/api/extract', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la respuesta del servidor');
                }
                return response.json();
            })
            .then(data => {
                processed++;
                updateProgress(processed, files.length);
                
                // Guardar resultado
                allResults.push({
                    filename: file.name,
                    coordinates: data.coordinates,
                    text: data.text
                });
                
                // Mostrar resultado
                displayResult(file, data.text, data.coordinates);
                
                // Comprobar si se han procesado todos los archivos
                if (processed === files.length) {
                    showResults();
                }
            })
            .catch(error => {
                processed++;
                updateProgress(processed, files.length);
                console.error('Error:', error);
                
                // Mostrar error
                displayError(file.name, error);
                
                // Comprobar si se han procesado todos los archivos
                if (processed === files.length) {
                    showResults();
                }
            });
        });
    }

    // Actualizar barra de progreso
    function updateProgress(current, total) {
        const percent = Math.round((current / total) * 100);
        progressFill.style.width = percent + '%';
        progressText.textContent = `Procesando (${current}/${total})`;
    }

    // Mostrar resultados
    function showResults() {
        progressContainer.style.display = 'none';
        resultsSection.style.display = 'block';
        showMessage(`Procesadas ${allResults.length} imágenes correctamente`, 'success');
    }

    // Mostrar un resultado individual
    function displayResult(file, text, coordinates) {
        const resultDiv = document.createElement('div');
        resultDiv.className = 'result-item';
        
        // Crear miniatura de la imagen
        const img = document.createElement('img');
        const reader = new FileReader();
        reader.onload = function(e) {
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
        
        // Crear contenido del resultado
        resultDiv.innerHTML = `
            <div class="result-image">
                <img src="" alt="${file.name}">
            </div>
            <div class="result-content">
                <h3>${file.name}</h3>
                <div class="result-coordinates">
                    <strong>Coordenadas:</strong>
                    <pre>${coordinates}</pre>
                </div>
                <div class="result-text">
                    <details>
                        <summary>Texto extraído</summary>
                        <pre>${text}</pre>
                    </details>
                </div>
                <div class="result-actions">
                    <button class="btn btn-sm btn-secondary copy-btn" data-text="${coordinates}">
                        📋 Copiar coordenadas
                    </button>
                </div>
            </div>
        `;
        
        // Reemplazar la imagen cuando se cargue
        reader.onload = function(e) {
            const imgElement = resultDiv.querySelector('img');
            imgElement.src = e.target.result;
        };
        
        // Agregar evento para copiar coordenadas
        resultDiv.querySelector('.copy-btn').addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-text');
            navigator.clipboard.writeText(textToCopy)
                .then(() => showMessage('Coordenadas copiadas', 'success'))
                .catch(() => showMessage('Error al copiar texto', 'error'));
        });
        
        // Agregar a la lista de resultados
        imageResults.appendChild(resultDiv);
    }

    // Mostrar error
    function displayError(filename, error) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'result-item error';
        errorDiv.innerHTML = `
            <div class="result-content">
                <h3>${filename}</h3>
                <div class="error-message">
                    <strong>Error:</strong> ${error.message || 'Error al procesar la imagen'}
                </div>
            </div>
        `;
        imageResults.appendChild(errorDiv);
    }

    // Mostrar mensajes
    function showMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;
        
        messageContainer.appendChild(messageDiv);
        
        // Eliminar mensaje después de 3 segundos
        setTimeout(() => {
            messageDiv.classList.add('fade-out');
            setTimeout(() => {
                messageContainer.removeChild(messageDiv);
            }, 500);
        }, 3000);
    }
});