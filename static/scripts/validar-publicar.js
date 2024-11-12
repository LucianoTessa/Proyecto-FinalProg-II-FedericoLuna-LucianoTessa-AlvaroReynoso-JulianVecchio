document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('formulario-publicar');

  form.addEventListener('submit', (e) => {
    e.preventDefault(); // Evitar el envío inicial
    let isValid = true;

    // Función para mostrar mensajes de error
    const showError = (elementId, message) => {
      document.getElementById(elementId).innerText = message;
    };

    // Función para limpiar mensajes de error
    const clearError = (elementId) => {
      document.getElementById(elementId).innerText = '';
    };

    // Validación del título
    const titulo = document.getElementById('titulo').value.trim();
    if (titulo === '') {
      showError('error-titulo', 'Por favor, ingrese un título para la propiedad.');
      isValid = false;
    } else {
      clearError('error-titulo');
    }

    // Validación del precio
    const precio = document.getElementById('precio').value.trim();
    if (precio === '' || isNaN(precio) || Number(precio) <= 0) {
      showError('error-precio', 'Por favor, ingrese un precio válido.');
      isValid = false;
    } else {
      clearError('error-precio');
    }

    // Validación del tipo de propiedad
    const tipo = document.getElementById('tipo').value;
    if (tipo === 'otros') {
      showError('error-tipo', 'Por favor, seleccione el tipo de propiedad.');
      isValid = false;
    } else {
      clearError('error-tipo');
    }

    // Validación de modalidad (venta/alquiler)
    const modalidad = document.getElementById('venta').value;
    if (modalidad === 'otros') {
      showError('error-venta', 'Por favor, seleccione la modalidad.');
      isValid = false;
    } else {
      clearError('error-venta');
    }

    // Validación de baños
    const banios = document.getElementById('banios').value.trim();
    if (banios === '' || isNaN(banios) || Number(banios) <= 0) {
      showError('error-banios', 'Ingrese un número válido de baños.');
      isValid = false;
    } else {
      clearError('error-banios');
    }

    // Validación de habitaciones
    const habitaciones = document.getElementById('habitaciones').value.trim();
    if (habitaciones === '' || isNaN(habitaciones) || Number(habitaciones) <= 0) {
      showError('error-habitaciones', 'Ingrese un número válido de habitaciones.');
      isValid = false;
    } else {
      clearError('error-habitaciones');
    }

    // Validación de metros cuadrados
    const metros = document.getElementById('metros').value.trim();
    if (metros === '' || isNaN(metros) || Number(metros) <= 0) {
      showError('error-metros', 'Ingrese los metros cuadrados válidos.');
      isValid = false;
    } else {
      clearError('error-metros');
    }

    // Validación de ciudad
    const ciudad = document.getElementById('ciudad').value.trim();
    if (ciudad === '') {
      showError('error-ciudad', 'Por favor, ingrese la ciudad.');
      isValid = false;
    } else {
      clearError('error-ciudad');
    }

    // Validación de dirección
    const direccion = document.getElementById('direccion').value.trim();
    if (direccion === '') {
      showError('error-direccion', 'Por favor, ingrese la dirección.');
      isValid = false;
    } else {
      clearError('error-direccion');
    }

    // Validación de descripción
    const descripcion = document.getElementById('descripcion').value.trim();
    if (descripcion === '') {
      showError('error-descripcion', 'Por favor, ingrese una descripción.');
      isValid = false;
    } else {
      clearError('error-descripcion');
    }

    // Enviar el formulario solo si todos los campos son válidos
    if (isValid) {
      form.submit();
    }
  });
});
