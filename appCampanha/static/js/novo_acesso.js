
    function mostrarSenhaSingUp1() {
        var inputPass = document.getElementById('password1');
        var btnShowPass = document.getElementById('olho-senha');

        if (inputPass.type === 'password') {
            inputPass.setAttribute('type', 'text');
            btnShowPass.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            inputPass.setAttribute('type', 'password');
            btnShowPass.classList.replace('fa-eye-slash', 'fa-eye');
        }
    }

    function mostrarSenhaSingUp2() {
        var inputPass = document.getElementById('password2');
        var btnShowPass = document.getElementById('olho-senha2');

        if (inputPass.type === 'password') {
            inputPass.setAttribute('type', 'text');
            btnShowPass.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            inputPass.setAttribute('type', 'password');
            btnShowPass.classList.replace('fa-eye-slash', 'fa-eye');
        }
    }

document.addEventListener('DOMContentLoaded', function () {
    const funcaoSelect = document.getElementById('funcao');
    const atuacoesContainer = document.getElementById('atuacoes-container');  // O container que contém a label e as checkboxes

    // Função para exibir ou esconder o campo "Atuações" e limpar seleções
    function toggleAtuacoes() {
        if (funcaoSelect.value === 'Solucionador') {
            atuacoesContainer.style.display = 'block';  // Exibe o campo "Atuações" (inclui a label e as checkboxes)
        } else {
            atuacoesContainer.style.display = 'none';  // Esconde o campo "Atuações" (inclui a label e as checkboxes)
            // Desmarca todas as checkboxes quando não for "Solucionador"
            const checkboxes = atuacoesContainer.querySelectorAll('input[type="checkbox"]');
            checkboxes.forEach(checkbox => checkbox.checked = false);
        }
    }

    // Chama a função quando o valor da função mudar
    funcaoSelect.addEventListener('change', toggleAtuacoes);

    // Chama a função ao carregar a página para verificar a seleção inicial
    toggleAtuacoes();
});