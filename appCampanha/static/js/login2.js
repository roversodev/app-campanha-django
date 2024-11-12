const inputs = document.querySelectorAll(".input-field");
const toggle_btn = document.querySelectorAll(".toggle");
const main = document.querySelector("main");
const bullets = document.querySelectorAll(".bullets span");
const images = document.querySelectorAll(".image");

let currentSlide = 1;
const slideIntervalTime = 5000;

// Adicionar evento de foco e blur aos inputs
inputs.forEach((inp) => {
  inp.addEventListener("focus", () => {
    inp.classList.add("active");
  });
  inp.addEventListener("blur", () => {
    if (inp.value != "") return;
    inp.classList.remove("active");
  });
});

// Alternar entre modos de sign-in e sign-up
toggle_btn.forEach((btn) => {
  btn.addEventListener("click", () => {
    main.classList.toggle("sign-up-mode");
  });
});

// Função para mover o slider
function moveSlider(index = null) {
  // Se não for passado um índice, usamos o valor de currentSlide
  if (index === null) index = currentSlide;

  let currentImage = document.querySelector(`.img-${index}`);
  
  // Remove a classe show de todas as imagens e oculta
  images.forEach((img) => img.classList.remove("show"));
  currentImage.classList.add("show");

  // Mover o texto correspondente
  const textSlider = document.querySelector(".text-group");
  textSlider.style.transform = `translateY(${-(index - 1) * 2.2}rem)`;

  // Atualizar o estado dos bullets
  bullets.forEach((bull) => bull.classList.remove("active"));
  bullets[index - 1].classList.add("active");

  // Atualizar o índice do slide atual
  currentSlide = index;
}

// Função para passar automaticamente para o próximo slide
function autoSlide() {
  currentSlide++;
  if (currentSlide > images.length) {
    currentSlide = 1; // Volta para a primeira imagem se passar do número de imagens
  }
  moveSlider(currentSlide);
}

// Definir a troca automática de slides a cada X segundos
let slideInterval = setInterval(autoSlide, slideIntervalTime);

// Permitir que o usuário troque os slides manualmente ao clicar nos bullets
bullets.forEach((bullet) => {
  bullet.addEventListener("click", function() {
    // Pausar o slide automático ao clicar
    clearInterval(slideInterval);

    // Mover para o slide correspondente ao bullet clicado
    moveSlider(parseInt(this.dataset.value));

    // Reiniciar o slide automático após a troca manual
    slideInterval = setInterval(autoSlide, slideIntervalTime);
  });
});

