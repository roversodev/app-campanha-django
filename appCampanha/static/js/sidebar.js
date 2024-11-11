window.addEventListener('load', () => {
    document.querySelector('.loader-container').style.display = 'none';
});

window.onscroll = function () {
    const btn = document.querySelector('.back-to-top');
    if (window.scrollY > 200) {
        btn.classList.add('show');
    } else {
        btn.classList.remove('show');
    }
};

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

$(".menu > ul > li").click(function (e) {
    // remover classe ativa do que não estiver ativo
    $(this).siblings().removeClass("active")
    // adicionar no clicado
    $(this).toggleClass("active");
    // se tiver submenu abrir
    $(this).find("ul").slideToggle();
    // fechar o submenu aberto se abrir outro
    $(this).siblings().find("ul").slideUp();
    // tirar classe active dos submenus
    $(this).siblings().find("ul").find("li").removeClass("active");
});

$(".menu-btn").click(function () {
    $(".sidebar").toggleClass("active");
})


document.addEventListener('DOMContentLoaded', function () {
    const themeSwitch = document.getElementById('theme-switch');
    const body = document.body;

    // Função para aplicar o tema escuro ou claro
    function applyTheme(isDark) {
        if (isDark) {
            body.classList.add('dark-theme');
            themeSwitch.checked = true;
        } else {
            body.classList.remove('dark-theme');
            themeSwitch.checked = false;
        }
    }

    // Verifica se o tema está salvo no localStorage
    const savedTheme = localStorage.getItem('dark-theme');

    if (savedTheme) {
        // Se houver um tema salvo, aplica-o
        applyTheme(savedTheme === 'true');
    } else {
        // Se não houver tema salvo, usa o tema do dispositivo
        const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
        applyTheme(prefersDarkScheme);
    }

    // Atualiza o tema ao mudar o switch
    themeSwitch.addEventListener('change', function () {
        if (themeSwitch.checked) {
            body.classList.add('dark-theme');
            localStorage.setItem('dark-theme', 'true'); // Salva a preferência do usuário
        } else {
            body.classList.remove('dark-theme');
            localStorage.setItem('dark-theme', 'false'); // Salva a preferência do usuário
        }
    });

    // Ouve mudanças no tema preferido do sistema e ajusta automaticamente
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (event) {
        if (!localStorage.getItem('dark-theme')) {
            applyTheme(event.matches);
        }
    });
});




document.addEventListener('DOMContentLoaded', function () {
    // Obtém o caminho da URL atual
    var currentPath = window.location.pathname;

    // Seleciona todos os itens da navbar
    var navItems = document.querySelectorAll('.menu > ul > li');

    navItems.forEach(function (item) {
        var link = item.querySelector('a');
        var href = link.getAttribute('href');

        // Verifica se o href do link corresponde ao caminho atual
        if (href === currentPath) {
            item.classList.add('active');

            // Abre o submenu se houver
            var submenu = item.querySelector('.sub-menu');
            if (submenu) {
                submenu.style.display = 'block';
            }
        } else {
            item.classList.remove('active');

            // Fecha o submenu se houver
            var submenu = item.querySelector('.sub-menu');
            if (submenu) {
                submenu.style.display = 'none';
            }
        }
    });
});
