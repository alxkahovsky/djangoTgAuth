document.addEventListener('DOMContentLoaded', function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
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
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
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
            window.open(`https://t.me/yakovlev_auth_bot?start=${token}`, '_blank');
                   async function checkAuthStatus() {
            let result = false;
            const interval = 2000; // Интервал в миллисекундах (2 секунды)

            while (result === false) {
                try {
                    const response = await fetch('/api/users/telegram/auth/status?session_token='+token, {
                        method: 'GET',
                    });

                    if (response.status === 200) {
                        result = true;
                        window.location.reload();
                    } else {
                        await new Promise(resolve => setTimeout(resolve, interval));
                    }
                } catch (error) {
                    console.error('Ошибка:', error);
                    await new Promise(resolve => setTimeout(resolve, interval));
                }
            }
        }
        checkAuthStatus();
        });
    });
});