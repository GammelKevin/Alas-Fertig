document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM ist geladen, initialisiere Event-Listener...');
    
    // Hinzufügen-Formular Event-Listener
    const addForm = document.getElementById('addForm');
    if (addForm) {
        console.log('Hinzufügen-Formular gefunden, füge Event-Listener hinzu');
        
        addForm.addEventListener('submit', function(event) {
            event.preventDefault();
            console.log('Hinzufügen-Formular abgeschickt!');
            
            // Grundlegende Formularvalidierung
            const day = this.querySelector('[name="day"]').value;
            if (!day) {
                showToast('error', 'Bitte wählen Sie einen Tag aus.');
                return;
            }
            
            // Checkbox-Status überprüfen
            const vacationCheckbox = document.getElementById('addVacation');
            const closedCheckbox = document.getElementById('addClosed');
            
            const isVacation = vacationCheckbox.checked;
            const isClosed = closedCheckbox.checked;
            
            console.log('Formular-Status:', { day, isVacation, isClosed });
            
            // Spezifische Validierung basierend auf ausgewähltem Modus
            if (isVacation) {
                const startDate = document.getElementById('addVacationStart').value;
                const endDate = document.getElementById('addVacationEnd').value;
                
                if (!startDate || !endDate) {
                    showToast('error', 'Für Urlaubstage müssen Start- und Enddatum angegeben werden.');
                    return;
                }
            } else if (!isClosed) {
                const openTime1 = document.getElementById('addOpenTime1').value;
                const closeTime1 = document.getElementById('addCloseTime1').value;
                
                if (!openTime1 || !closeTime1) {
                    showToast('error', 'Bitte geben Sie die erste Öffnungszeit an.');
                    return;
                }
            }
            
            // FormData erstellen
            const formData = new FormData();
            
            // Grunddaten hinzufügen
            formData.append('day', day);
            formData.append('vacation_active', isVacation ? 'true' : 'false');
            formData.append('closed', isClosed ? 'true' : 'false');
            
            // CSRF-Token hinzufügen
            const csrfToken = document.querySelector('input[name="csrf_token"]').value;
            formData.append('csrf_token', csrfToken);
            
            // Spezifische Felder basierend auf dem Modus hinzufügen
            if (isVacation) {
                formData.append('vacation_start', document.getElementById('addVacationStart').value);
                formData.append('vacation_end', document.getElementById('addVacationEnd').value);
            } else if (!isClosed) {
                formData.append('open_time_1', document.getElementById('addOpenTime1').value);
                formData.append('close_time_1', document.getElementById('addCloseTime1').value);
                
                const openTime2 = document.getElementById('addOpenTime2').value;
                const closeTime2 = document.getElementById('addCloseTime2').value;
                
                if (openTime2 && closeTime2) {
                    formData.append('open_time_2', openTime2);
                    formData.append('close_time_2', closeTime2);
                }
            }
            
            // Debugging: Formular-Daten anzeigen
            console.log('Formular-Daten:');
            for (let [key, value] of formData.entries()) {
                console.log(`${key}: ${value}`);
            }
            
            // Anfrage an den Server senden
            fetch('/admin/oeffnungszeiten/hinzufuegen', {
                method: 'POST',
                body: formData,
                credentials: 'same-origin'
            })
            .then(response => {
                console.log('Server-Antwort Status:', response.status);
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.message || 'Netzwerkantwort war nicht ok');
                    }).catch(() => {
                        throw new Error('Netzwerkantwort war nicht ok und konnte nicht als JSON verarbeitet werden');
                    });
                }
                
                // Versuche, die Antwort als JSON zu parsen
                return response.text().then(text => {
                    console.log('Server Response Text:', text);
                    if (!text) {
                        throw new Error('Leere Antwort vom Server erhalten');
                    }
                    
                    try {
                        return JSON.parse(text);
                    } catch (e) {
                        console.error('Fehler beim Parsen der JSON-Antwort:', e);
                        throw new Error('Die Serverantwort konnte nicht als JSON verarbeitet werden');
                    }
                });
            })
            .then(data => {
                console.log('Server-Antwort Daten:', data);
                
                if (data.success) {
                    // Erfolgsmeldung anzeigen
                    showToast('success', data.message || 'Öffnungszeit erfolgreich hinzugefügt');
                    
                    // Formular zurücksetzen
                    addForm.reset();
                    document.getElementById('addVacationDates').style.display = 'none';
                    document.getElementById('addTimeFields').style.display = 'block';
                    
                    // Seite neu laden
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                } else {
                    // Fehlermeldung anzeigen
                    showToast('error', data.message || 'Fehler beim Hinzufügen der Öffnungszeit');
                }
            })
            .catch(error => {
                console.error('Fehler bei der Anfrage:', error);
                showToast('error', 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.');
            });
        });
    } else {
        console.warn('Hinzufügen-Formular nicht gefunden!');
    }
    
    // Event-Listener für Checkboxen im Hinzufügen-Formular
    const addVacationCheckbox = document.getElementById('addVacation');
    const addClosedCheckbox = document.getElementById('addClosed');
    
    if (addVacationCheckbox) {
        addVacationCheckbox.addEventListener('change', function() {
            console.log('Urlaubs-Checkbox geändert:', this.checked);
            const vacationDates = document.getElementById('addVacationDates');
            const timeFields = document.getElementById('addTimeFields');
            
            if (vacationDates && timeFields) {
                vacationDates.style.display = this.checked ? 'block' : 'none';
                
                if (this.checked) {
                    timeFields.style.display = 'none';
                    if (addClosedCheckbox) addClosedCheckbox.checked = false;
                } else if (!addClosedCheckbox || !addClosedCheckbox.checked) {
                    timeFields.style.display = 'block';
                }
            }
        });
    }
    
    if (addClosedCheckbox) {
        addClosedCheckbox.addEventListener('change', function() {
            console.log('Ruhetag-Checkbox geändert:', this.checked);
            const vacationDates = document.getElementById('addVacationDates');
            const timeFields = document.getElementById('addTimeFields');
            
            if (timeFields) {
                timeFields.style.display = this.checked ? 'none' : (addVacationCheckbox && addVacationCheckbox.checked ? 'none' : 'block');
                
                if (this.checked && addVacationCheckbox) {
                    addVacationCheckbox.checked = false;
                    if (vacationDates) vacationDates.style.display = 'none';
                }
            }
        });
    }
    
    // Event Listener für Urlaub und Ruhetag Checkboxen im Edit-Formular
    const editVacationCheckbox = document.getElementById('editVacation');
    const editClosedCheckbox = document.getElementById('editClosed');
    
    if (editVacationCheckbox) {
        editVacationCheckbox.addEventListener('change', function() {
            const vacationDates = document.getElementById('editVacationDates');
            const timeFields = document.getElementById('editTimeFields');
            
            if (vacationDates && timeFields) {
                vacationDates.style.display = this.checked ? 'block' : 'none';
                timeFields.style.display = this.checked || (editClosedCheckbox && editClosedCheckbox.checked) ? 'none' : 'block';
                
                if (this.checked && editClosedCheckbox) {
                    editClosedCheckbox.checked = false;
                }
            }
        });
    }

    if (editClosedCheckbox) {
        editClosedCheckbox.addEventListener('change', function() {
            const timeFields = document.getElementById('editTimeFields');
            const vacationDates = document.getElementById('editVacationDates');
            
            if (timeFields) {
                timeFields.style.display = this.checked ? 'none' : 'block';
                
                if (this.checked && editVacationCheckbox) {
                    editVacationCheckbox.checked = false;
                    if (vacationDates) vacationDates.style.display = 'none';
                }
            }
        });
    }

    // Event Listener für das Edit-Formular
    const editForm = document.getElementById('editForm');
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const id = document.getElementById('editId').value;
            if (!id) {
                showToast('error', 'Keine ID für die Bearbeitung gefunden');
                return;
            }
            
            handleSubmit(this, `/admin/oeffnungszeiten/bearbeiten/${id}`, 'edit');
        });
    }
});

function setupCheckboxListeners(prefix) {
    console.log('Setup Checkbox Listeners für Prefix:', prefix);
    
    // ACHTUNG: Diese Funktion wird in der aktuellen Version nicht verwendet
    // Die Event-Listener werden direkt im DOMContentLoaded Event hinzugefügt
    
    const vacationCheckbox = document.getElementById(`${prefix}Vacation`);
    const vacationDates = document.getElementById(`${prefix}VacationDates`);
    const timeFields = document.getElementById(`${prefix}TimeFields`);
    const closedCheckbox = document.getElementById(`${prefix}Closed`);

    console.log('Gefundene Elemente:', {
        vacationCheckbox: vacationCheckbox !== null,
        vacationDates: vacationDates !== null,
        timeFields: timeFields !== null,
        closedCheckbox: closedCheckbox !== null
    });

    if (vacationCheckbox && vacationDates && timeFields && closedCheckbox) {
        // Urlaub Checkbox
        vacationCheckbox.addEventListener('change', function() {
            console.log(`${prefix} Vacation Checkbox Change:`, this.checked);
            vacationDates.style.display = this.checked ? 'block' : 'none';
            timeFields.style.display = this.checked ? 'none' : (closedCheckbox.checked ? 'none' : 'block');
            if (this.checked) {
                closedCheckbox.checked = false;
            }
        });

        // Geschlossen Checkbox
        closedCheckbox.addEventListener('change', function() {
            console.log(`${prefix} Closed Checkbox Change:`, this.checked);
            timeFields.style.display = this.checked ? 'none' : (vacationCheckbox.checked ? 'none' : 'block');
            if (this.checked) {
                vacationCheckbox.checked = false;
                vacationDates.style.display = 'none';
            }
        });
    }
}

function handleSubmit(form, url, action) {
    console.log('Handle Submit:', { url, action });
    
    if (!validateForm(form)) {
        console.log('Formularvalidierung fehlgeschlagen');
        return;
    }

    const formData = new FormData(form);
    
    // Checkbox-Werte korrekt verarbeiten
    const vacationActive = form.querySelector('[name="vacation_active"]');
    const closed = form.querySelector('[name="closed"]');
    
    // Entferne alte Checkbox-Werte aus dem FormData
    if (formData.has('vacation_active')) {
        formData.delete('vacation_active');
    }
    if (formData.has('closed')) {
        formData.delete('closed');
    }
    
    // Füge die korrekten Werte hinzu (true/false als Strings)
    formData.append('vacation_active', vacationActive && vacationActive.checked ? 'true' : 'false');
    formData.append('closed', closed && closed.checked ? 'true' : 'false');

    // Stelle sicher, dass CSRF-Token eingebunden ist
    const csrfTokenInput = document.querySelector('input[name="csrf_token"]');
    if (csrfTokenInput && !formData.has('csrf_token')) {
        formData.append('csrf_token', csrfTokenInput.value);
    }
    
    console.log('Form Data für Submit:', {
        day: formData.get('day'),
        vacation_active: formData.get('vacation_active'),
        closed: formData.get('closed'),
        vacation_start: formData.get('vacation_start'),
        vacation_end: formData.get('vacation_end'),
        open_time_1: formData.get('open_time_1'),
        close_time_1: formData.get('close_time_1'),
        csrf_token: formData.get('csrf_token')
    });
    
    fetch(url, {
        method: 'POST',
        body: formData,
        credentials: 'same-origin'
    })
    .then(response => {
        console.log('Server Response Status:', response.status);
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.message || 'Netzwerkantwort war nicht ok');
            }).catch(() => {
                throw new Error('Netzwerkantwort war nicht ok und konnte nicht als JSON verarbeitet werden');
            });
        }
        
        // Versuche, die Antwort als JSON zu parsen
        return response.text().then(text => {
            console.log('Server Response Text:', text);
            if (!text) {
                throw new Error('Leere Antwort vom Server erhalten');
            }
            
            try {
                return JSON.parse(text);
            } catch (e) {
                console.error('Fehler beim Parsen der JSON-Antwort:', e);
                throw new Error('Die Serverantwort konnte nicht als JSON verarbeitet werden');
            }
        });
    })
    .then(data => {
        console.log('Server Response Data:', data);
        if (!data) {
            throw new Error('Leere Daten vom Server erhalten');
        }
        
        if (data.success) {
            showToast('success', data.message);
            
            if (action === 'add') {
                form.reset();
                if (document.getElementById('addVacationDates')) {
                    document.getElementById('addVacationDates').style.display = 'none';
                }
                if (document.getElementById('addTimeFields')) {
                    document.getElementById('addTimeFields').style.display = 'block';
                }
            } else if (action === 'edit') {
                const editModal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
                if (editModal) {
                    editModal.hide();
                }
            }
            
            // Seite nach erfolgreicher Aktion neu laden
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            showToast('error', data.message || 'Ein Fehler ist aufgetreten.');
        }
    })
    .catch(error => {
        console.error('Fetch Error:', error);
        showToast('error', error.message || 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.');
    });
}

function validateForm(form) {
    console.log('Validiere Formular');
    
    // Prüfe, welche Checkboxen aktiviert sind
    const vacationCheckbox = form.querySelector('[name="vacation_active"]');
    const closedCheckbox = form.querySelector('[name="closed"]');
    
    const vacationActive = vacationCheckbox ? vacationCheckbox.checked : false;
    const closed = closedCheckbox ? closedCheckbox.checked : false;
    
    console.log('Formular-Status:', { 
        vacationActive, 
        closed,
        'vacation_active input type': vacationCheckbox ? vacationCheckbox.type : 'not found',
        'closed input type': closedCheckbox ? closedCheckbox.type : 'not found'
    });
    
    // Konvertiere Checkbox-Werte zu hidden-Feldern für korrekte Übertragung
    let hiddenVacationActive = form.querySelector('input[type="hidden"][name="vacation_active"]');
    if (!hiddenVacationActive) {
        hiddenVacationActive = document.createElement('input');
        hiddenVacationActive.type = 'hidden';
        hiddenVacationActive.name = 'vacation_active';
        form.appendChild(hiddenVacationActive);
    }
    hiddenVacationActive.value = vacationActive ? 'true' : 'false';
    
    let hiddenClosed = form.querySelector('input[type="hidden"][name="closed"]');
    if (!hiddenClosed) {
        hiddenClosed = document.createElement('input');
        hiddenClosed.type = 'hidden';
        hiddenClosed.name = 'closed';
        form.appendChild(hiddenClosed);
    }
    hiddenClosed.value = closed ? 'true' : 'false';
    
    const day = form.querySelector('[name="day"]').value;
    if (!day) {
        showToast('error', 'Bitte wählen Sie einen Tag aus.');
        return false;
    }

    if (vacationActive) {
        const startDate = form.querySelector('[name="vacation_start"]').value;
        const endDate = form.querySelector('[name="vacation_end"]').value;
        
        if (!startDate || !endDate) {
            showToast('error', 'Bitte geben Sie Start- und Enddatum für den Urlaub an.');
            return false;
        }
        
        const start = new Date(startDate);
        const end = new Date(endDate);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (start > end) {
            showToast('error', 'Das Enddatum muss nach dem Startdatum liegen.');
            return false;
        }
        
        if (start < today) {
            showToast('error', 'Das Startdatum darf nicht in der Vergangenheit liegen.');
            return false;
        }
        
        if ((end - start) / (1000 * 60 * 60 * 24) > 365) {
            showToast('error', 'Der Urlaubszeitraum darf nicht länger als ein Jahr sein.');
            return false;
        }
    }

    if (!vacationActive && !closed) {
        const openTime1 = form.querySelector('[name="open_time_1"]').value;
        const closeTime1 = form.querySelector('[name="close_time_1"]').value;
        const openTime2 = form.querySelector('[name="open_time_2"]').value;
        const closeTime2 = form.querySelector('[name="close_time_2"]').value;
        
        if (!openTime1 || !closeTime1) {
            showToast('error', 'Bitte geben Sie mindestens die erste Öffnungszeit an.');
            return false;
        }
        
        // Überprüfe, ob die Zeiten im korrekten Format sind
        const timeRegex = /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/;
        if (!timeRegex.test(openTime1) || !timeRegex.test(closeTime1)) {
            showToast('error', 'Bitte geben Sie gültige Uhrzeiten im Format HH:MM ein.');
            return false;
        }
        
        // Überprüfe die zweite Öffnungszeit, falls angegeben
        if ((openTime2 && !closeTime2) || (!openTime2 && closeTime2)) {
            showToast('error', 'Bitte geben Sie beide Zeiten für die zweite Öffnungszeit an oder lassen Sie beide leer.');
            return false;
        }
        
        if (openTime2 && closeTime2) {
            if (!timeRegex.test(openTime2) || !timeRegex.test(closeTime2)) {
                showToast('error', 'Bitte geben Sie gültige Uhrzeiten im Format HH:MM ein.');
                return false;
            }
        }
        
        // Überprüfe, ob die Schließzeit nach der Öffnungszeit liegt
        const [openHour1, openMin1] = openTime1.split(':').map(Number);
        const [closeHour1, closeMin1] = closeTime1.split(':').map(Number);
        if (openHour1 > closeHour1 || (openHour1 === closeHour1 && openMin1 >= closeMin1)) {
            showToast('error', 'Die Schließzeit muss nach der Öffnungszeit liegen.');
            return false;
        }
        
        if (openTime2 && closeTime2) {
            const [openHour2, openMin2] = openTime2.split(':').map(Number);
            const [closeHour2, closeMin2] = closeTime2.split(':').map(Number);
            
            // Konvertiere Zeiten in Minuten seit Mitternacht
            const closeTime1InMinutes = closeHour1 * 60 + closeMin1;
            let openTime2InMinutes = openHour2 * 60 + openMin2;
            let closeTime2InMinutes = closeHour2 * 60 + closeMin2;
            
            // Wenn die zweite Öffnungszeit vor der ersten Schließzeit liegt,
            // nehmen wir an, dass sie am nächsten Tag ist
            if (openTime2InMinutes <= closeTime1InMinutes) {
                openTime2InMinutes += 1440; // Füge 24 Stunden hinzu
                closeTime2InMinutes += 1440; // Die zweite Schließzeit muss auch am nächsten Tag sein
            }
            
            // Wenn die zweite Schließzeit vor der zweiten Öffnungszeit liegt,
            // fügen wir weitere 24 Stunden hinzu
            if (closeTime2InMinutes <= openTime2InMinutes) {
                closeTime2InMinutes += 1440;
            }
            
            if (closeTime2InMinutes <= openTime2InMinutes) {
                showToast('error', 'Die zweite Schließzeit muss nach der zweiten Öffnungszeit liegen.');
                return false;
            }
        }
    }

    return true;
}

async function editOpeningHours(id) {
    try {
        console.log('Bearbeite Öffnungszeit mit ID:', id);
        const response = await fetch(`/admin/oeffnungszeiten/${id}`);
        const data = await response.json();
        
        if (data.success) {
            console.log('Daten geladen:', data);
            // Hidden Input für die ID setzen
            const editIdInput = document.getElementById('editId');
            editIdInput.value = id;
            console.log('ID gesetzt auf:', editIdInput.value);
            
            const daySelect = document.getElementById('editDay');
            daySelect.value = data.hours.day;
            daySelect.setAttribute('readonly', true); // Statt disabled verwenden wir readonly
            
            document.getElementById('editVacation').checked = data.hours.vacation_active;
            document.getElementById('editClosed').checked = data.hours.closed;
            
            if (data.hours.vacation_active) {
                document.getElementById('editVacationDates').style.display = 'block';
                document.getElementById('editVacationStart').value = data.hours.vacation_start;
                document.getElementById('editVacationEnd').value = data.hours.vacation_end;
                document.getElementById('editTimeFields').style.display = 'none';
            } else if (data.hours.closed) {
                document.getElementById('editVacationDates').style.display = 'none';
                document.getElementById('editTimeFields').style.display = 'none';
            } else {
                document.getElementById('editVacationDates').style.display = 'none';
                document.getElementById('editTimeFields').style.display = 'block';
                document.getElementById('editOpenTime1').value = data.hours.open_time_1 || '';
                document.getElementById('editCloseTime1').value = data.hours.close_time_1 || '';
                document.getElementById('editOpenTime2').value = data.hours.open_time_2 || '';
                document.getElementById('editCloseTime2').value = data.hours.close_time_2 || '';
            }
            
            const modal = new bootstrap.Modal(document.getElementById('editModal'));
            modal.show();
        } else {
            showToast('error', data.message || 'Fehler beim Laden der Daten');
        }
    } catch (error) {
        console.error('Fehler beim Laden der Öffnungszeiten:', error);
        showToast('error', 'Fehler beim Laden der Öffnungszeiten');
    }
}

async function deleteOpeningHours(id) {
    console.log('deleteOpeningHours aufgerufen mit ID:', id);
    
    if (!confirm('Möchten Sie diesen Eintrag wirklich löschen?')) {
        console.log('Löschen wurde abgebrochen');
        return;
    }

    try {
        console.log('Sende DELETE-Request...');
        // CSRF-Token sammeln
        const csrfToken = document.querySelector('input[name="csrf_token"]').value;
        
        // FormData erstellen und CSRF-Token hinzufügen
        const formData = new FormData();
        formData.append('csrf_token', csrfToken);
        
        const response = await fetch(`/admin/oeffnungszeiten/loeschen/${id}`, {
            method: 'POST',
            body: formData,
            credentials: 'same-origin'
        });

        console.log('Response erhalten:', response.status);
        const data = await response.json();
        console.log('Response-Daten:', data);

        if (data.success) {
            console.log('Löschen erfolgreich');
            showToast('success', 'Öffnungszeiten erfolgreich gelöscht');
            // Seite neu laden um die Tabelle zu aktualisieren
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            console.log('Löschen fehlgeschlagen:', data.message);
            showToast('error', data.message || 'Fehler beim Löschen der Öffnungszeiten');
        }
    } catch (error) {
        console.error('Fehler beim Löschen:', error);
        showToast('error', 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.');
    }
}

function addTableRow(data) {
    console.log('Füge neue Tabellenzeile hinzu:', data);
    
    const tbody = document.querySelector('table tbody');
    const row = document.createElement('tr');
    row.setAttribute('data-id', data.id);
    
    row.innerHTML = createRowHtml(data);
    tbody.appendChild(row);
}

function updateTableRow(data) {
    console.log('Aktualisiere Tabellenzeile:', data);
    
    const row = document.querySelector(`tr[data-id="${data.id}"]`);
    if (row) {
        row.innerHTML = createRowHtml(data);
    }
}

function createRowHtml(data) {
    let statusHtml = '';
    if (data.vacation_active) {
        statusHtml = `<span class="badge bg-warning">Urlaub</span><br>
                     ${data.vacation_start} bis ${data.vacation_end}`;
    } else if (data.closed) {
        statusHtml = '<span class="badge bg-danger">Geschlossen</span>';
    } else {
        statusHtml = `${data.open_time_1} - ${data.close_time_1}`;
        if (data.open_time_2 && data.close_time_2) {
            statusHtml += `<br>${data.open_time_2} - ${data.close_time_2}`;
        }
    }
    
    return `
        <td>${data.day}</td>
        <td>${statusHtml}</td>
        <td>
            <button type="button" class="btn btn-primary btn-sm" onclick="editOpeningHours(${data.id})">
                <i class="fas fa-edit"></i>
            </button>
            <button type="button" class="btn btn-danger btn-sm" onclick="deleteOpeningHours(${data.id})">
                <i class="fas fa-trash"></i>
            </button>
        </td>
    `;
}

function showToast(type, message) {
    // Zuerst alle existierenden Toasts entfernen
    const existingToasts = document.querySelectorAll('.toast');
    existingToasts.forEach(toast => toast.remove());
    
    // Neuen Toast erstellen
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    // Schließen-Button hinzufügen
    const closeButton = document.createElement('button');
    closeButton.className = 'close-button';
    closeButton.innerHTML = '×';
    closeButton.onclick = () => toast.remove();
    toast.appendChild(closeButton);
    
    // Toast zur Seite hinzufügen
    document.body.appendChild(toast);
    
    // Toast nach 5 Sekunden automatisch entfernen
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, 5000);
}

function loadOpeningHours() {
    console.log('Lade Öffnungszeiten');
    
    fetch('/admin/oeffnungszeiten')
        .then(response => response.json())
        .then(data => {
            console.log('Öffnungszeiten:', data);
            if (data.success) {
                const tbody = document.querySelector('table tbody');
                tbody.innerHTML = '';
                
                data.hours.forEach(hour => {
                    const row = document.createElement('tr');
                    row.setAttribute('data-id', hour.id);
                    
                    row.innerHTML = createRowHtml(hour);
                    tbody.appendChild(row);
                });
            } else {
                showToast('error', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('error', 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.');
        });
}
