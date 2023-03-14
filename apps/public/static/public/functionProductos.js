var gId = null;

$(document).ready(function () {

    validarInputs(); // Añadir validaciones a los inputs

    $("#btnAddProducto").click(function () {
        gId = null;
        $("#mdlProducto").modal("show");
        emptyInputs();
    });

    $('[data-toggle="tooltip"]').tooltip();

    $('#tblProductos').DataTable(window.configAjax);

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

        $("#mdlProducto").modal("show");
    });

});

// GUARDAR PRODUCTOS
function save() {

    let codigoReferencia = $("#txtCodigoReferencia").val().trim();
    let descripcion = $("#txtDescripcion").val().trim();
    let tipo = $("#selectTipo").val().trim();
    let cantidad = $("#txtCantidad").val().trim();
    let precio = $("#txtPrecio").val().trim();
    let estadoActivo = 0;
    let estadoSave = true

    if (cantidad === "")
        cantidad = 0;

    if (precio === "")
        precio = 0;

    if (codigoReferencia === "")
        $("#txtCodigoReferencia").addClass("is-invalid");

    if (descripcion === "")
        $("#txtDescripcion").addClass("is-invalid");

    if ($("#checkActivo").is(":checked"))
        estadoActivo = 1;

    if (tipo === "0")
        $("#selectTipo").addClass("is-invalid");

    if (codigoReferencia === "" || descripcion === "" || tipo === "0")
        estadoSave = false

    if (estadoSave) {
        let datos = new FormData();
        datos.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());
        datos.append('codigo', codigoReferencia);
        datos.append('descripcion', descripcion);
        datos.append('cantidad', cantidad);
        datos.append('precio', precio);
        datos.append('tipo', tipo);
        datos.append('estadoActivo', estadoActivo);
        datos.append('file', document.getElementById("imagen").files[0]);

        alertify.confirm('CONFIRMACIÓN', '¿Desea guardar el producto?', function () {
                $.ajax({
                    type: 'POST',
                    url: "/productos/",
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

    if (descripcion === "")
        $("#txtDescripcion").addClass("is-invalid");

    if (nombre === "" || descripcion === "")
        estadoSave = false

    if (estadoSave) {
        let datos = new FormData();
        datos.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());
        datos.append('crud', 2);
        datos.append('id', codigo);
        datos.append('nombre', nombre);
        datos.append('descripcion', descripcion);
        datos.append('estadoActivo', estadoActivo);

        alertify.confirm('CONFIRMACIÓN', '¿Desea actualizar el producto?', function () {
                $.ajax({
                    type: 'POST',
                    url: "/productos/",
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
function deleteProducto(id) {

    let datos = new FormData();
    datos.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());
    datos.append('crud', 3);
    datos.append('id', id);

    alertify.confirm('CONFIRMACIÓN', '¿Desea eliminar el producto?', function () {
            $.ajax({
                type: 'POST',
                url: "/updateproducto/",
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

// VALIDAR IMPUTS
function validarInputs() {

    // Números decimales con punto y dos decimales
    $("#txtPrecio").on("input", function () {
        var value = $(this).val();
        if (!/^(\d+)?([.]?\d{0,2})?$/.test(value)) {
            $(this).val(value.replace(/[^\d.]/g, ''));
        }
    });

    // Solamente nùmeros
    $("#txtCantidad").on("input", function () {
        var value = $(this).val();
        if (!/^[0-9]+$/.test(value)) {
            $(this).val(value.replace(/[^0-9]+/g, ''));
        }
    });
}