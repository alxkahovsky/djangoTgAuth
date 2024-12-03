document.addEventListener('DOMContentLoaded', function() {
    function getCurrentDateTime() {
        console.log(new Date().toISOString());
        return new Date().toISOString();
    }
    function getAuthToken(callback) {
        const data = {
            created: getCurrentDateTime()
        };
        fetch('/api/users/telegram/auth/start/',{
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(data => {
                if (data.id) {
                    callback(data.id);
                } else {
                    console.error('Ошибка получения токена');
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
    }
    // Обработчик события нажатия на кнопку
    document.getElementById('telegram-auth-button').addEventListener('click', function() {
        getAuthToken(function(token) {
            // Открываем новую вкладку с токеном в URL
            window.open(`https://t.me/yakovlev_auth_bot?start=${token}`, '_blank');
        });
    });
});