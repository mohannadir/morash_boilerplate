/**
 * @fileoverview Helper functions for translations.
 */

window.addEventListener('load', function () {
    initLanguagePicker();
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function initLanguagePicker() {
    let language_select_element = document.getElementsByClassName('set-language');

    for (let i = 0; i < language_select_element.length; i++) {
        language_select_element[i].addEventListener('click', function () {
            let language_code = this.dataset.language;
            setLanguage(language_code);
        });
    }
}

function setLanguage(language_code) {

    let formData = new FormData();
    formData.append('language', language_code);

    fetch('/i18n/setlang/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData
    }).then(function (response) {
        if (response.ok) {
            location.reload();
        }
    }).catch(function (error) {
        console.log(error);
    }
    );
}