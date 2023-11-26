function validateForm() {
    let v = document.forms["Form"]["Mensaje"].value;
    let x = document.forms["Form"]["Nombre"].value;
    let y = document.forms["Form"]["Email"].value;
    let z = document.forms["Form"]["Telefono"].value; 
    if (x=="") {
      alert("La columna Nombre se encuentra vacia");
      return false;
    }
    if (y=="") {
        alert("La columna Mail se encuentra vacia");
        return false;
      }
    if (z=="") {
        alert("La columna Telefono se encuentra vacia");
        return false;
      }  
    if (v=="") {
        alert("La columna Mensaje se encuentra vacia");
        return false;
      }    
  }