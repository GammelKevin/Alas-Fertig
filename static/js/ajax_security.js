// AJAX-Sicherheitshelfer für API-Schlüssel-Authentifizierung
document.addEventListener('DOMContentLoaded', function() {
    // Die API-Schlüssel-Funktion abrufen
    fetch('/get_api_key_token')
        .then(response => response.json())
        .then(data => {
            // API-Schlüssel-Token für spätere Verwendung speichern
            window.apiKeyToken = data.token;
            
            // Alle AJAX-Anfragen abfangen und den API-Schlüssel hinzufügen
            const originalFetch = window.fetch;
            window.fetch = function(url, options) {
                options = options || {};
                options.headers = options.headers || {};
                
                // API-Schlüssel zu Anfragen hinzufügen
                if (window.apiKeyToken) {
                    options.headers['X-API-Key'] = window.apiKeyToken;
                }
                
                return originalFetch(url, options);
            };
            
            // Auch für jQuery AJAX-Anfragen (falls verwendet)
            if (window.jQuery) {
                $(document).ajaxSend(function(event, jqxhr, settings) {
                    jqxhr.setRequestHeader('X-API-Key', window.apiKeyToken);
                });
            }
        })
        .catch(error => console.error('Fehler beim Abrufen des API-Schlüssels:', error));
});
