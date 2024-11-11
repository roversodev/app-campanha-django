function buscaCep(){
    let cep = document.getElementById("txtCep").value;
    if (!cep == ""){
        let url = "https://brasilapi.com.br/api/cep/v1/" + cep;
        let req = new XMLHttpRequest();
        req.open("GET", url);
        req.send();
  
        req.onload = function (){
            if(req.status == 200){
                let endereco = JSON.parse(req.response);
                document.getElementById("endereço").value = endereco.street;
                document.getElementById("bairro").value = endereco.neighborhood;
                document.getElementById("estado").value = endereco.city;
                document.getElementById("municipio").value = endereco.state;
            }else if(req.status == 404){
                alert("CEP Inválido")
            }else{
                alert("Erro ao fazer a requisição")
            }
        }
    }
  }
  
  window.onload = function(){
    let cep = document.getElementById("txtCep");
    cep.addEventListener("blur", buscaCep);
  }