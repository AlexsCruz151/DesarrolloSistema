const timer = 1500;
const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: timer
});

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function objectForm(form) {
    let formSerialized = form.serializeArray();
    let object = {};
    for (let i = 0; i < formSerialized.length; i++) {
        if (formSerialized[i]['name'])
            object[formSerialized[i]['name']] = formSerialized[i]['value'];
    }
    return object;
}

function serializeTable(table) {
    let rows = [];
    table.each(function () {
        let row = {};
        $(this).find('td').each(function () {
            if ($(this).data('name'))
                row[$(this).data('name')] = $(this).text().trim();
        });
        rows.push(row);
    });
    return rows;
}

function reload(time) {
    time = time || timer;
    setTimeout(function () {
        location.reload();
    }, time);
}

function redirect_to(url, time) {
    time = time || timer;
    setTimeout(function () {
        $(location).prop('href', url);
    }, time);
}

function showMessage(type, msg) {
    const alert_type = (type === 'error') ? 'danger' : type;
    const html_ =
        `<div class="alert alert-${alert_type} alert-dismissible fade show" role="alert">
            <strong>${msg}</strong>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`
    $('#message_loader').addClass('my-3').html(html_);
    setTimeout(function () {
        $('#message_loader').removeClass('my-3').html('');
    }, timer);
}

function messageError(error) {
    let msg = '';
    if (typeof (error) === 'object') {
        $.each(error, function (key, value) {
            if (typeof (value) === "object") {
                $('#id_' + key).addClass('is-invalid');
                msg = value[0];
            } else {
                msg = value;
            }
        });
    } else {
        msg = error;
    }
    Toast.fire({
        icon: 'error',
        title: msg
    });
}

function messageSuccess(msg) {
    Toast.fire({
        icon: 'success',
        title: msg
    });
}
