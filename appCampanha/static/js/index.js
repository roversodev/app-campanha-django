// Função para fazer a requisição via AJAX e atualizar o span de notificações
function updateNotificationCount() {
    fetch(unreadNotificationsCountUrl)  // Use a variável que contém a URL gerada pelo Django
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const notificationCountSpan = document.querySelector('.notification-count');
            
            if (data.unread_count > 0) {
                // Se houver notificações não lidas, exibir o número
                if (!notificationCountSpan) {
                    // Se o span não existir, criar um
                    const newSpan = document.createElement('span');
                    newSpan.classList.add('notification-count');
                    newSpan.textContent = data.unread_count;
                    document.querySelector('.notification-bell').appendChild(newSpan);
                } else {
                    // Atualizar o número no span existente
                    notificationCountSpan.textContent = data.unread_count;
                }
            } else {
                // Se não houver notificações não lidas, remover o span
                if (notificationCountSpan) {
                    notificationCountSpan.remove();
                }
            }
        })
        .catch(error => console.error('Erro ao buscar contagem de notificações:', error));
}

// Função para mostrar/esconder o popup com animação
function toggleNotificationPopup() {
    const popup = document.getElementById('notification-popup');
    
    if (popup.classList.contains('visible3')) {
        popup.classList.remove('visible3');
        popup.classList.add('hidden3');
        setTimeout(() => popup.style.visibility = 'hidden3', 300); // Aguarda a animação para esconder
    } else {
        popup.style.visibility = 'visible3'; // Exibe o popup antes da animação
        popup.classList.remove('hidden3');
        popup.classList.add('visible3');
        updateNotifications(); // Atualiza as notificações quando o popup é aberto
    }
}

// Função para fechar o popup quando clicar fora dele
function closePopupOnClickOutside(event) {
    const popup = document.getElementById('notification-popup');
    if (popup.classList.contains('visible3') && !popup.contains(event.target) && !event.target.closest('.notification-bell')) {
        popup.classList.remove('visible3');
        popup.classList.add('hidden3');
        setTimeout(() => popup.style.visibility = 'hidden3', 300); // Aguarda a animação para esconder
    }
}

// Função para fechar o popup ao pressionar Esc
function closePopupOnEsc(event) {
    if (event.key === 'Escape') {
        const popup = document.getElementById('notification-popup');
        if (popup.classList.contains('visible3')) {
            popup.classList.remove('visible3');
            popup.classList.add('hidden3');
            setTimeout(() => popup.style.visibility = 'hidden3', 300); // Aguarda a animação para esconder
        }
    }
}

// Atualiza as notificações no popup
function updateNotifications() {
    fetch(notificationsUrl)  // Use a variável que contém a URL gerada pelo Django
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const popup = document.getElementById('notification-popup');
            const list = popup.querySelector('ul');
            list.innerHTML = '';

            if (data.notifications.length === 0) {
                list.innerHTML = '<li>Não há novas notificações para você!</li>';
            } else {
                data.notifications.forEach(notification => {
                    const li = document.createElement('li');

                    // Adiciona a classe 'unread' se a notificação não foi lida
                    if (notification.unread) {
                        li.classList.add('unread');
                    }

                    li.onclick = () => markAsRead(notification.id);
                    li.innerHTML = `
                        ${notification.unread ? '<span class="notification-dot"></span>' : ''}
                        <strong>${notification.sender}</strong>: ${notification.verb}
                        <span class="notification-time">${notification.timestamp_timesince} atrás</span>
                    `;
                    list.appendChild(li);
                });
            }
        })
        .catch(error => console.error('Erro ao buscar notificações:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function markAsRead(notificationId) {
    fetch(`/mark-notification-as-read/${notificationId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
    .then(response => {
        if (response.ok) {
            updateNotifications(); // Atualiza as notificações após marcar como lidas
            updateNotificationCount();
        }
    })
    .catch(error => console.error('Erro ao marcar notificação como lida:', error));
}

// Atualiza a cada 30 segundos
setInterval(updateNotificationCount, 30000);
updateNotificationCount();

// Adiciona o listener para fechar o popup ao clicar fora dele
document.addEventListener('click', closePopupOnClickOutside);

// Adiciona o listener para fechar o popup ao pressionar Esc
document.addEventListener('keydown', closePopupOnEsc);
