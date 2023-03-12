var gId = null;

$(document).ready(function () {

    $("#btnAddBodega").click(function () {
        gId = null;
        $("#mdlBodega").modal("show");
        emptyInputs();
    });

    $('[data-toggle="tooltip"]').tooltip();

    $('#tblBodegas').DataTable(window.configAjax);

    $("#btnSave").click(function () {
        if (gId == null)
            save();
        else
            update();
    });

    $(".btnEdit").click(function () {
        let id = $(this).data('id');
        gId = id;
        let nombre = $(this).data('nombre');
        let descripcion = $(this).data('descripcion');
        let estado = $(this).data('estado');
        $("#txtCodigo").val(id);
        $("#txtNombre").val(nombre);
        $("#txtDescripcion").val(descripcion);

        if (estado === 1)
            $("#checkActivo").prop("checked", true);
        else
            $("#checkActivo").prop("checked", false);

        $("#mdlBodega").modal("show");
    });

});

// GUARDAR BODEGA
function save() {

    let codigo = $("#txtCodigo").val().trim();
    let nombre = $("#txtNombre").val().trim();
    let descripcion = $("#txtDescripcion").val().trim();
    let estadoActivo = 0;
    let estadoSave = true

    if ($("#checkActivo").is(":checked"))
        estadoActivo = 1;

    if (nombre === "")
        $("#txtNombre").addClass("is-invalid");

    if (descripcion === "")
        $("#txtDescripcion").addClass("is-invalid");

    if (descripcion === "" || nombre === "")
        estadoSave = false

    if (estadoSave) {
        let datos = new FormData();
        datos.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());
        datos.append('nombre', nombre);
        datos.append('descripcion', descripcion);
        datos.append('estadoActivo', estadoActivo);

        alertify.confirm('CONFIRMACIÓN', '¿Desea guardar la bodega?', function () {
                $.ajax({
                    type: 'POST',
                    url: "/bodega/",
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
                            title: 'Error de administración',
                            timer: 10000
                        });
                    },
                });
            }
            , function () {
            }).set('labels', {ok: 'Aceptar', cancel: 'Cancelar'},);
    }


}

// ACTUALIZAR BODEGA
function update() {
    let codigo = $("#txtCodigo").val().trim();
    let nombre = $("#txtNombre").val().trim();
    let descripcion = $("#txtDescripcion").val().trim();
    let estadoActivo = 0;
    let estadoSave = true

    if ($("#checkActivo").is(":checked"))
        estadoActivo = 1;

    if (nombre === "")
        $("#txtNombre").addClass("is-invalid");

    if(descripcion === "")
        $("#txtDescripcion").addClass("is-invalid");

    if (nombre==="" || descripcion === "")
        estadoSave = false

    if (estadoSave) {
        let datos = new FormData();
        datos.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());
        datos.append('crud', 2);
        datos.append('id', codigo);
        datos.append('nombre', nombre);
        datos.append('descripcion', descripcion);
        datos.append('estadoActivo', estadoActivo);

        alertify.confirm('CONFIRMACIÓN', '¿Desea actualizar bodega?', function () {
                $.ajax({
                    type: 'POST',
                    url: "/updatebodega/",
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
                            title: 'Error de administración',
                            timer: 10000
                        });
                    },
                });
            }
            , function () {
            }).set('labels', {ok: 'Aceptar', cancel: 'Cancelar'},);
    }
}

// ELIMINAR UNA BODEGA
function deleteBodega(id) {

    let datos = new FormData();
    datos.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());
    datos.append('crud', 3);
    datos.append('id', id);

    alertify.confirm('CONFIRMACIÓN', '¿Desea eliminar la bodega?', function () {
            $.ajax({
                type: 'POST',
                url: "/updatebodega/",
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