const form = document.getElementById("form-iniciar-sesion");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const email = document.getElementById("correo");
  const contrasenia = document.getElementById("contrasenia");

  const correoError = document.querySelector("#correo-error");
  const contraseniaError = document.querySelector("#contrasenia-error");

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  let emailValidado = emailRegex.test(email.value);

  const contraseniaRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$/;
  let contraseniaValidada = contraseniaRegex.test(contrasenia.value);

  correoError.textContent = "";
  email.style.border = "1px solid rgb(223, 223, 223)";
  contraseniaError.textContent = "";
  contrasenia.style.border = "1px solid rgb(223, 223, 223)";

  if (!emailValidado) {
    correoError.textContent = "El email es invalido";
    email.style.border = "2px solid red";
  }

  if (!contraseniaValidada) {
    contraseniaError.textContent =
      "La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un numero";
    contrasenia.style.border = "2px solid red";
  }

  if (emailValidado && contraseniaValidada) {
    window.location.href = "/index.html";
  }
});
