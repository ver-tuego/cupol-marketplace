document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('subscribeForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвращаем стандартное поведение отправки формы

        // Получаем значение email из поля ввода
        var email = document.getElementById('emailInput').value;

        // Создаем объект FormData и добавляем в него значение email
        var formData = new FormData();
        formData.append('email', email);

        // Отправляем данные на сервер с помощью AJAX
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/subscribe', true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                // Выводим сообщение об успешной подписке
                alert('Вы успешно подписались!');
            } else if (xhr.readyState === 4 && xhr.status !== 200) {
                // Выводим сообщение об ошибке при подписке
                alert('Произошла ошибка при подписке. Пожалуйста, попробуйте снова.');
            }
        };
        xhr.send(formData); // Отправляем FormData на сервер
    });
});