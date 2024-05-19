function search(event) {
    event.preventDefault();
    // Получаем значение из строки ввода
    var query = document.getElementById('searchQuery').value;
    // Формируем URL с параметром запроса
    var url = "/search/" + encodeURIComponent(query);
    // Перенаправляем пользователя на эту страницу
    if (query != "") {
        window.location.href = url;
    }
}