// Функция для загрузки новых карточек товаров с сервера
function loadMoreCards(start, limit) {
// Получаем путь страницы
var path = window.location.pathname;

// Разбиваем путь на части по символу "/"
var pathParts = path.split('/');

// Получаем последний элемент массива, который и будет вашим <query>
var query = pathParts[pathParts.length - 1];
fetch(`/load-more-search?start=${start}&limit=${limit}&query=${query}`)
  .then(response => response.json())
  .then(data => {
    // Добавляем новые карточки товаров на страницу
    data.forEach(product => {
      const cardDiv = document.createElement('div');
      cardDiv.classList.add('col-md-3'); // Используем класс сетки Bootstrap для ограничения ширины карточки и количества карточек в линии
      cardDiv.innerHTML = `
        <div class="card">
          <img src="/${product.image}" class="card-img-top" alt="${product.name}">
          <div class="card-body">
            <h5 class="card-title">${product.name}</h5>
            <p class="card-price">Цена: ${product.price}₽</p>
            <p class="card-rating">★${product.rating}</p>
            <a href="/product/${product.id}" class="btn btn-dark btn-primary btn-animated">Подробнее</a> <!-- Кнопка "Подробнее" -->
          </div>
        </div>
      `;
      document.getElementById('product-container').appendChild(cardDiv);
    });
  })
  .catch(error => console.error('Ошибка загрузки карточек товаров:', error));
}

// Обработчик события прокрутки страницы
window.addEventListener('scroll', function() {
if (isBottomReached()) {
  loadMoreCards(document.querySelectorAll('.card').length, 4); // Загружаем по 4 новых карточки при достижении конца страницы
}
});

// Функция, которая проверяет, достиг ли пользователь конца страницы
function isBottomReached() {
return window.innerHeight + window.scrollY >= document.body.offsetHeight;
}

// Начинаем загрузку карточек товаров при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
loadMoreCards(0, 16); // Загружаем первые 16 карточек товаров
});