// Получение product_id из текущего URL-адреса
var product_id = window.location.pathname.split('/').pop();

// Заполнение скрытого поля формы с product_id
document.getElementById('product_id').value = product_id;