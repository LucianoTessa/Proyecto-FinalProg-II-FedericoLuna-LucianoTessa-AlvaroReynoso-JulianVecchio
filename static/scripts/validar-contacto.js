const form = document.querySelector("#formulario-contacto");

function validarEmail(event) {
  event.preventDefault();

  const nombre = document.querySelector("#nombre");
  const email = document.querySelector("#email");
  const mensaje = document.querySelector("#mensaje");

  const nombreError = document.querySelector("#nombre-error");
  const emailError = document.querySelector("#email-error");
  const mensajeError = document.querySelector("#mensaje-error");

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  let emailValidado = emailRegex.test(email.value);

  // Limpiar errores
  nombreError.textContent = "";
  nombre.style.border = "1px solid rgb(223, 223, 223)";
  mensajeError.textContent = "";
  mensaje.style.border = "1px solid rgb(223, 223, 223)";
  emailError.textContent = "";
  email.style.border = "1px solid rgb(223, 223, 223)";

  // Validar campos
  if (nombre.value.length < 3) {
    nombreError.textContent = "El nombre debe tener al menos 3 caracteres";
    nombre.style.border = "2px solid red";
  }

  if (mensaje.value.length === 0) {
    mensajeError.textContent = "El mensaje es obligatorio";
    mensaje.style.border = "2px solid red";
  }

  if (!emailValidado) {
    emailError.textContent = "El email es invalido";
    email.style.border = "2px solid red";
  }

  // Enviar formulario
  if (nombre.value.length >= 3 && mensaje.value.length > 0 && emailValidado) {
    const botonForm = document.querySelector("#boton-form");
    botonForm.style.background = "#4BB543";
    botonForm.textContent = "Enviado";
  }
}

form.addEventListener("submit", validarEmail);
