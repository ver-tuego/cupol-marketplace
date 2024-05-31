function sendData(product_id) {
    var bttn = document.getElementById("submitButton");
    var url_ = '/add_product/' + product_id;
    $.ajax({
        url: url_,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 'value': $('div.active').index() }),
        success: function(response) {
            document.getElementById('output').innerHTML = response.result;
        },
        error: function(error) {
            console.log(error);
        }
    });
}