function fillSlots(data) {
    for (let key in data) {
        let value = data[key];
        $(key).html(value);
    }
}