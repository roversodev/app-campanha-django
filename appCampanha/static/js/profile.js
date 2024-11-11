// JavaScript para exibir o preview da imagem após o upload
const profileImageInput = document.getElementById('profile_image');
const profileImagePreview = document.getElementById('profileImagePreview');
const removeProfileImageIcon = document.getElementById('removeProfileImage');
const removeProfileImageHidden = document.getElementById('remove_profile_image_hidden');

profileImageInput.addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            profileImagePreview.src = e.target.result; // Atualiza a imagem com o preview
            removeProfileImageHidden.value = "false"; // Redefine a remoção da imagem
        }
        reader.readAsDataURL(file); // Lê o arquivo de imagem como URL
    }
});

// Remove a imagem e substitui pelo placeholder ao clicar no ícone "X"
removeProfileImageIcon.addEventListener('click', function () {
    const placeholder = profileImagePreview.getAttribute('data-placeholder'); // Obtém o caminho da imagem do atributo
    profileImagePreview.src = placeholder; // Substitui a imagem pelo placeholder
    removeProfileImageHidden.value = "true"; // Define que a imagem foi removida
    profileImageInput.value = ''; // Limpa o input de arquivo
});
