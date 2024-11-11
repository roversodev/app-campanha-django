const sign_in_btn2 = document.querySelector("#sign-in-btn2");
const sign_up_btn2 = document.querySelector("#sign-up-btn2");
const container3 = document.querySelector(".container3");

sign_up_btn2.addEventListener("click", () => {
  container3.classList.add("sign-up-mode");
});

sign_in_btn2.addEventListener("click", () => {
  container3.classList.remove("sign-up-mode");
});


function mostrarSenha() {
    var senha = document.getElementById("password");
    var toggleText = document.getElementById("toggle-password");
    
    if (senha.type === "password") {
        senha.type = "text";
        toggleText.textContent = "Ocultar";
    } else {
        senha.type = "password";
        toggleText.textContent = "Mostrar";
    }
}

    $(document).ready(function(){
      
      $("#cpf").mask("000.000.000-00");
  
    });