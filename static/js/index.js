    // Объект для хранения последнего выбранного значения для каждой группы радиокнопок
    const radioCheckedState = {};

    // Находим все радиокнопки на странице
    document.querySelectorAll('input[type="radio"]').forEach(radio => {
        radio.addEventListener('click', function() {
            const groupName = this.name;      // Имя группы (например, 'delivery' или 'size')
            const currentValue = this.value;  // Значение нажатой кнопки

            // Проверяем, был ли этот же элемент уже выбран последним в этой группе
            if (radioCheckedState[groupName] === currentValue) {
                // Если да — снимаем выбор и удаляем запись о последнем выборе
                this.checked = false;
                delete radioCheckedState[groupName];
            } else {
                // Если нет — запоминаем новый выбор
                radioCheckedState[groupName] = currentValue;
            }
        });
    });