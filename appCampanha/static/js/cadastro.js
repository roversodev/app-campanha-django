$(document).ready(function(){
    $("#cpf").mask("000.000.000-00");
  });


  $("#cpf, #dataN").on('input', function() {
    if ($(this).val()) {
        $(this).addClass('input-valid').removeClass('input-invalid');
    } else {
        $(this).addClass('input-invalid').removeClass('input-valid');
    }
});

$("#btnSubmit").click(function(event) {
    event.preventDefault();

    if ($("#cpf").val() === "" || $("#dataN").val() === "") {
        alert("Preencha todos os campos!");
        return;
    }

    $(this).addClass('btn-loading');
    $("#CadastroForm").submit();
    $("#loadingPopup").fadeIn();

    setTimeout(function() {
        $("#loadingPopup").fadeOut();
        $("#btnSubmit").removeClass('btn-loading');
    }, 300000); // Reduzido o tempo de espera para um exemplo mais prático
});