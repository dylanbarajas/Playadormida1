function comprobarClave() {

    var p1 = document.getElementById("password1").value;
    var p2 = document.getElementById("password2").value;

    var espacios = false;
    var cont = 0;

    while (!espacios && (cont < p1.length)) {
        if (p1.charAt(cont) == " ")
            espacios = true;
        cont++;
    }

    if (espacios) {
        alert("La password no puede contener espacios en blanco");
        return false;
    }

    if (p1 != p2) {
        alert("Las passwords deben de coincidir");
        return false;
      } else {
        alert("Procesando registro...");
        document.getElementById('registropropietarios').submit()
        return true; 
      }
    
    
}

