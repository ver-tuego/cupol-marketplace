var currentUrl = window.location.href;
var pathParts = currentUrl.split('/');
var product_id = pathParts[pathParts.length - 1];
console.log('Product ID:', product_id)

document.getElementById('addButton').addEventListener('click', function() {
    fetch('/basket_add', {
        method: 'POST',
        body: JSON.stringify({ product: product_id }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success == "1") {
            showToast('Успех', 'Товар добавлен в корзину');
        } else if (data.success == "0") {
            showToast('Ошибка', 'Вы не покупатель');
        } else if (data.success == "2") {
            showToast('Ошибка', 'Товара нет в наличии')
        } else if (data.success == "3") {
            showToast('Ошибка', 'В корзине максимальное количество товара')
        } else {
            showToast('Ошибка', 'Произошла неизвестная ошибка')
        }
    })
    .catch(error => {
        showToast('Ошибка', 'Произошла неизвестная ошибка');
    });
});

function showToast(title, message) {
    const toastElement = document.getElementById('dynamicToast');
    document.getElementById('toastTitle').textContent = title;
    document.getElementById('toastBody').textContent = message;
    $(toastElement).toast({ delay: 1000 });
    $(toastElement).toast('show');
}

document.querySelectorAll('.toast .close').forEach(button => {
    button.addEventListener('click', function() {
        const toastElement = this.closest('.toast');
        toastElement.classList.remove('show');
    });
});