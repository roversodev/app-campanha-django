function buscaCep() {
    let cep = document.getElementById("txtCep").value.trim();
    if (cep !== "") {
        let url = "https://viacep.com.br/ws/" + cep + "/json/";
        let req = new XMLHttpRequest();
        req.open("GET", url);
        req.send();

        req.onload = function () {
            if (req.status == 200) {
                let endereco = JSON.parse(req.response);
                if (endereco.erro) {
                    alert("CEP não encontrado!");
                } else {
                    document.getElementById("endereço").value = endereco.logradouro || "";
                    document.getElementById("bairro").value = endereco.bairro || "";
                    document.getElementById("estado").value = endereco.uf || "";
                    document.getElementById("municipio").value = endereco.localidade || "";
                }
            } else {
                alert("Erro ao fazer a requisição");
            }
        };

        req.onerror = function () {
            alert("Erro de rede, não foi possível acessar o serviço ViaCEP.");
        };
    } else {
        alert("Por favor, insira um CEP.");
    }
}

window.onload = function () {
    let cep = document.getElementById("txtCep");
    cep.addEventListener("blur", buscaCep);
};
