// Abre o modal quando o botão é clicado
document.getElementById("openModal").onclick = function() {
    console.log('Abrindo modal');
    document.getElementById("sendNotificationModal").style.display = "flex";
}

// Fecha o modal quando o botão de fechar é clicado
document.querySelector(".close").onclick = function() {
    document.getElementById("sendNotificationModal").style.display = "none";
}

// Fecha o modal quando o usuário clica fora do modal
window.onclick = function(event) {
    const modal = document.getElementById("sendNotificationModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
}

    // Função para filtrar notificações
    function filterNotifications(type) {
        const items = document.querySelectorAll('.notification-item');
        items.forEach(item => {
            const isUnread = item.classList.contains('unread');
            if (type === 'all') {
                item.style.display = 'flex';
            } else if (type === 'unread' && !isUnread) {
                item.style.display = 'none';
            } else if (type === 'read' && isUnread) {
                item.style.display = 'none';
            }
        });
    }

    // Função para marcar todas as notificações como lidas
    function markAllAsRead() {
        // Faz uma chamada AJAX para marcar todas as notificações como lidas
        fetch('/notifications/mark_all_as_read/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),  // Adicione o token CSRF se necessário
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Atualiza a interface do usuário
                filterNotifications('all'); // Atualiza a lista para mostrar notificações lidas
                alert('Todas as notificações foram marcadas como lidas.');
            }
        })
        .catch(error => console.error('Erro ao marcar todas como lidas:', error));
    }

    // Função para pegar o token CSRF, caso esteja usando formulários protegidos
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

    // A função para abrir o modal já está sendo tratada pelo Bootstrap
    // O botão com data-toggle="modal" e data-target="#sendNotificationModal" cuida disso
    $(document).ready(function() {
        $('#sendNotificationModal').on('show.bs.modal', function (event) {
            // Limpa os campos do formulário ao abrir o modal
            $('#recipients').val([]);
            $('#message').val('');
        });
    });

    // Função para enviar notificação
    function sendNotification() {
        const recipients = Array.from(document.getElementById('recipients').selectedOptions).map(option => option.value);
        const message = document.getElementById('message').value;

        if (recipients.length === 0 || message === '') {
            alert('Por favor, selecione pelo menos um destinatário e escreva uma mensagem.');
            return;
        }

        fetch('/send-notification/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                recipients: recipients,
                message: message
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Notificação enviada com sucesso!');
                $('#sendNotificationModal').modal('hide');  // Fechar o modal
            } else {
                alert('Erro ao enviar notificação.');
            }
        })
        .catch(error => console.error('Erro:', error));
    }