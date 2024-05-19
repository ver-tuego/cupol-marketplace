function checkFiles(input) {
    if (input.files.length > 4) {
        alert("Максимальное количество файлов для загрузки - 4");
        input.value = '';
    }
}