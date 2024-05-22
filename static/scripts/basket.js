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

    function handlePayment() {
        fetch('/payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => {
            if (response.ok) {
                // Очищаем корзину после успешного платежа
                const basketContainer = document.getElementById('basketItemsContainer');
                basketContainer.innerHTML = '';
                updateTotalAmount(0);
                alert('Оплата прошла успешно');
            } else {
                console.error('Payment failed:', response.statusText);
            }
        })
        .catch(error => console.error('Error during payment:', error));
    }

    document.getElementById('checkoutButton').addEventListener('click', handlePayment);

    fetchBasketItems();
});