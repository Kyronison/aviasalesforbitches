document.addEventListener("DOMContentLoaded", () => {
    const passwordInput = document.getElementById("password");
    const submitButton = document.getElementById("submitButton");

    // Изначально кнопка отключена
    submitButton.disabled = true;

    // Проверяем длину пароля
    passwordInput.addEventListener("input", () => {
        if (passwordInput.value.length >= 8) {
            submitButton.disabled = false;
        } else {
            submitButton.disabled = true;
        }
    });
});