var currentUrl = window.location.href;
var pathParts = currentUrl.split('/');
var product_id = pathParts[pathParts.length - 1];
console.log('Product ID:', product_id)

$(document).ready(function(){
  $('#addButton').click(function(){
    $.ajax({
      url: '/basket_add',
      type: 'POST',
      data: { product: product_id },
      success: function(response) {
        console.log('Данные успешно обновлены!');
      },
      error: function(error) {
        console.log('Произошла ошибка: ' + error);
      }
    });
  });
});