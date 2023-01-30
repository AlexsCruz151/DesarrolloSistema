var gId = null;

$(document).ready(function () {

    $("#btnAddEmpresa").click(function () {
        gId = null;
        $("#mdlEmpresa").modal("show");
        emptyInputs();
    });

    $('[data-toggle="tooltip"]').tooltip();

    $('#tblEmpresas').DataTable(window.configAjax);

    $("#btnSave").click(function () {
        if (gId == null)
            save();
        else
            update();
    });

    $(".btnEdit").click(function () {
        let id = $(this).data('id');
        gId = id;
        let descripcion = $(this).data('descripcion');
        let imagen = $(this).data('imagen');
        let estado = $(this).data('estado');
        $("#preview").attr("src", "/media/" + imagen);
        $("#txtCodigo").val(id);
        $("#txtDescripcion").val(descripcion);

        if (estado === 1)
            $("#checkActivo").prop("checked", true);
        else
            $("#checkActivo").prop("checked", false);

        $("#mdlEmpresa").modal("show");
    });

});

// GUARDAR EMPRESA
function save() {

    let codigo = $("#txtCodigo").val().trim();
    let descripcion = $("#txtDescripcion").val().trim();
    let estadoActivo = 0;
    let estadoSave = true

    if ($("#checkActivo").is(":checked"))
        estadoActivo = 1;

    if (descripcion === "")
        $("#txtDescripcion").addClass("is-invalid");

    if (descripcion === "")
        estadoSave = false

    if (document.getElementById("imagen").files.length === 0) {
        estadoSave = false;
        $("#file").addClass("is-invalid");
        return;
    }

    if (estadoSave) {
        let datos = new FormData();
        datos.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());
        datos.append('descripcion', descripcion);
        datos.append('estadoActivo', estadoActivo);
        datos.append('file', document.getElementById("imagen").files[0]);

        alertify.confirm('CONFIRMACIÓN', '¿Desea guardar la empresa?', function () {
                $.ajax({
                    type: 'POST',
                    url: "/empresa/",
                    data: datos,
                    dataType: 'json',
                    cache: false,
                    processData: false,  // importante
                    contentType: false, // importante
                    enctype: 'multipart/form-data',  // and here
                    success: function (respuesta) {
                        if (respuesta.error) {
                            if (respuesta.option == "1") {
                                Toast.fire({
                                    icon: 'error',
                                    title: respuesta.mensaje,
                                    timer: 5000
                                });

                            } else {
                                Toast.fire({
                                    icon: 'error',
                                    title: respuesta.mensaje,
                                    timer: 5000
                                });
                                showLoad(false);
                            }

                        } else {
                            Toast.fire({
                                icon: 'success',
                                title: respuesta.mensaje,
                                timer: 10000
                            });
                            showLoad(false);
                            window.reload();
                        }
                    },
                    error: function (error) {
                        Toast.fire({
                            icon: 'error',
                            title: 'Error de administraciónn',
                            timer: 10000
                        });
                    },
                });
            }
            , function () {
            }).set('labels', {ok: 'Aceptar', cancel: 'Cancelar'},);
    }


}

// ACTUALIZAR EMPRESA
function update() {
    let codigo = $("#txtCodigo").val().trim();
    let descripcion = $("#txtDescripcion").val().trim();
    let estadoActivo = 0;
    let estadoSave = true

    if ($("#checkActivo").is(":checked"))
        estadoActivo = 1;

    if (descripcion === "")
        $("#txtDescripcion").addClass("is-invalid");

    if (descripcion === "")
        estadoSave = false

    if (estadoSave) {
        let datos = new FormData();
        datos.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());
        datos.append('crud', 2);
        datos.append('id', codigo);
        datos.append('descripcion', descripcion);
        datos.append('estadoActivo', estadoActivo);
        datos.append('file', document.getElementById("imagen").files[0]);

        alertify.confirm('CONFIRMACIÓN', '¿Desea guardar la empresa?', function () {
                $.ajax({
                    type: 'POST',
                    url: "/actualizarempresa/",
                    data: datos,
                    dataType: 'json',
                    cache: false,
                    processData: false,  // importante
                    contentType: false, // importante
                    enctype: 'multipart/form-data',  // and here
                    success: function (respuesta) {
                        if (respuesta.error) {
                            if (respuesta.option == "1") {
                                Toast.fire({
                                    icon: 'error',
                                    title: respuesta.mensaje,
                                    timer: 5000
                                });

                            } else {
                                Toast.fire({
                                    icon: 'error',
                                    title: respuesta.mensaje,
                                    timer: 5000
                                });
                                showLoad(false);
                            }

                        } else {
                            Toast.fire({
                                icon: 'success',
                                title: respuesta.mensaje,
                                timer: 10000
                            });
                            showLoad(false);
                            window.reload();
                        }
                    },
                    error: function (error) {
                        Toast.fire({
                            icon: 'error',
                            title: 'Error de administraciónn',
                            timer: 10000
                        });
                    },
                });
            }
            , function () {
            }).set('labels', {ok: 'Aceptar', cancel: 'Cancelar'},);
    }
}

// ELIMINAR UNA EMPRESA
function deleteEmpresa(id) {

    let datos = new FormData();
    datos.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());
    datos.append('crud', 3);
    datos.append('id', id);

    alertify.confirm('CONFIRMACIÓN', '¿Desea eliminar la empresa?', function () {
            $.ajax({
                type: 'POST',
                url: "/actualizarempresa/",
                data: datos,
                dataType: 'json',
                cache: false,
                processData: false,  // importante
                contentType: false, // importante
                enctype: 'multipart/form-data',  // and here
                success: function (respuesta) {

                    if (respuesta.error) {
                        Toast.fire({
                            icon: 'error',
                            title: respuesta.mensaje,
                            timer: 5000
                        });

                    } else {
                        Toast.fire({
                            icon: 'success',
                            title: respuesta.mensaje,
                            timer: 10000
                        });

                        showLoad(false);
                        window.reload();
                    }
                },
                error: function (error) {
                    Toast.fire({
                        icon: 'error',
                        title: 'Error de administración',
                        timer: 10000
                    });
                },
            });
        }
        , function () {
        }).set('labels', {ok: 'Aceptar', cancel: 'Cancelar'},);
}

// CARGAR IMAGEN Y PREVISUALIZAR
function loadImage() {

    let preview = document.getElementById('preview');
    let file = document.getElementById('imagen').files[0];
    let reader = new FileReader();
    let fileType = file.type;

    if (!(fileType === "image/jpeg" || fileType === "image/png")) {
        $("#imagen").val("");
        Toast.fire({
            icon: 'error',
            title: 'Seleccione una imagen jpeg o png',
            timer: 10000
        });
    } else {

        reader.onloadend = function () {
            preview.src = reader.result;
            preview.style.display = 'block';
        }

        if (file) {
            reader.readAsDataURL(file);
        } else {
            preview.src = "";
        }
    }
}

// LIMPIAR FORMURARIOS
function emptyInputs() {

    let inputs = document.getElementsByTagName("input");

    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type === "text" || inputs[i].type === "file") {
            inputs[i].value = "";
        }
    }
    $("#preview").attr('src', '');

}