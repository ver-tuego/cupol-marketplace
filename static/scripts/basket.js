document.addEventListener('DOMContentLoaded', function() {
    function fetchBasketItems() {
        fetch('/basket')
            .then(response => response.json())
            .then(data => {
                renderBasketItems(data.items);
                updateTotalAmount(data.total);
            })
            .catch(error => console.error('Error fetching basket items:', error));
    }

    function renderBasketItems(items) {
        const basketContainer = document.getElementById('basketItemsContainer');
        basketContainer.innerHTML = ''; // Очищаем контейнер

        items.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.classList.add('product-item', 'd-flex', 'align-items-center');
            itemElement.innerHTML = `
                <img src="${item.image}" alt="${item.name}" class="product-image mr-3">
                <div>
                    <h6>${item.name}</h6>
                    <p>Цена: ${item.price} руб.</p>
                    <p>Количество: ${item.quantity}</p>
                </div>
            `;
            basketContainer.appendChild(itemElement);
        });
    }

    function updateTotalAmount(total) {
        document.getElementById('totalAmount').textContent = total;
    }

    fetchBasketItems();

    document.getElementById('checkoutButton').addEventListener('click', function() {
    });
});