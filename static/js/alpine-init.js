// Инициализация Alpine.js
document.addEventListener('alpine:init', () => {
    // Глобальные данные Alpine
    Alpine.data('global', () => ({
        showToast(message, type = 'success') {
            // Логика показа уведомлений
            console.log(type, message);
        }
    }));
});