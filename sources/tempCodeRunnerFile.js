function closeAbout() {
    const aboutModal = document.getElementById("aboutModal");
    aboutModal.style.display = "none";
}

function openAbout() {
    const aboutModal = document.getElementById("aboutModal");
    aboutModal.style.display = "block";
}

function toggleNav() {
    const sidebar = document.getElementById("mySidebar");
    sidebar.style.width = sidebar.style.width === "250px" ? "0" : "250px";
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
}

function logout() {
    fetch('http://gimron34-b473cd9e-bfb8-45c0-a153-06c888b9c177.socketxp.com/logout')
        .then(response => {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error('Ошибка при выполнении запроса');
            }
        })
        .then(data => {
            console.log(data);
            window.location.href = "Autorezation.html";
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

fetch('http://gimron34-b473cd9e-bfb8-45c0-a153-06c888b9c177.socketxp.com/get_login')
    .then(response => response.json())
    .then(data => {
        const userLogin = document.getElementById('userLogin');
        if (data.login == '') {
            window.location.href = "Autorezation.html";
        } else {
            userLogin.textContent = data.login;
        }
    })
    .catch(error => {
        userLogin.textContent = "Оффлайн";
    });

function simulateLoading() {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 14;
        if (progress > 100) {
            clearInterval(interval);
            document.getElementById("loader-wrapper").style.display = "none";
            document.getElementById("black-bg").style.display = "none";
            document.getElementById("main-content").style.display = "block";
        }
        document.getElementById("progressText").textContent = `${Math.round(progress)}%`;
        updateLoader(progress); // Вызываем функцию для обновления анимации спрайта
    }, 100);
}

simulateLoading();

fetch('http://gimron34-b473cd9e-bfb8-45c0-a153-06c888b9c177.socketxp.com/get_info_user')
    .then(response => response.json())
    .then(data => {
        const userLogin = document.getElementById('user_login');
        const solvedTasks = document.getElementById('solvedTasks');
        userLogin.textContent = data.login;
        solvedTasks.textContent = data.count;
        const elements = document.querySelectorAll('[id*="user_name"]');
        elements.forEach(element => {
            element.textContent = data.name;
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });

function showFullText(newsId) {
    const fullText = document.getElementById(newsId + "Full");
    const showBtn = document.querySelector(`#${newsId}Container .show-btn`);
    const hideBtn = document.querySelector(`#${newsId}Container .hide-btn`);

    fullText.style.display = "block";
    showBtn.style.display = "none";
    hideBtn.style.display = "inline-block";
    fullText.style.maxHeight = fullText.scrollHeight + "px"; // Установка максимальной высоты для показа всего текста
}

function hideFullText(newsId) {
    const fullText = document.getElementById(newsId + "Full");
    const showBtn = document.querySelector(`#${newsId}Container .show-btn`);
    const hideBtn = document.querySelector(`#${newsId}Container .hide-btn`);
    fullText.style.maxHeight = 0; // Установка максимальной высоты 0, чтобы скрыть текст
    fullText.style.display = "none";
    showBtn.style.display = "inline-block";
    hideBtn.style.display = "none";
}



    function showLanguagePopup() {
            var languageList = document.getElementById("languageList");
            if (languageList.style.display === "block") {
                languageList.style.display = "none";
            } else {
                languageList.style.display = "block";
            }
        }
