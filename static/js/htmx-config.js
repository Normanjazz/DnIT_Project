// Настройка HTMX
document.body.addEventListener('htmx:configRequest', (event) => {
    // Добавляем CSRF токен ко всем запросам
    event.detail.headers['X-CSRFToken'] = getCookie('csrftoken');
});

// Функция для получения CSRF токена
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