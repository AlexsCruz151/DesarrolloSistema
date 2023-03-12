var gId = null;


$(document).ready(function () {

    validarInputs();
    estadoContenedorPrecios(0);

    $("#btnAddEntradaPiezas").click(function () {
        gId = null;
        emptyInputs(); // Vaciamos valores ingresados en inputs
        estadoContenedorPrecios(0); // Mostramos detalle de precios
        $("#mdlEntradaPiezas").modal("show");
    });

    $('[data-toggle="tooltip"]').tooltip();

    $('#tblPiezas').DataTable({
        "oLanguage": {
            "sSearch": "Buscar",
            "sProcessing": "Procesando",
            "sLoadingRecords": "Cargando",
            "sInfo": "Mostrando _START_ a _END_ de _TOTAL_ registros",
            "sLengthMenu": "Mostrar _MENU_ registros",
            "oPaginate": {
                "sFirst": "Primera",
                "sLast": "Última",
                "sNext": "Siguiente",
                "sPrevious": "Anterior"
            }
        },
    });

    $(".btnSelectPieza").click(function () {
        let id = parseInt($(this).data('id'));
        let descripcion = $(this).data('descripcion');
        let precio = $(this).data('piezas_precio');

        $("#cantidadTxtCodigo").val(id);
        $("#cantidadTxtDescripcion").val(descripcion);
        $("#cantidadTxtCantidad").val("");

        if (!!precio == false)
            precio = 0.0;
        $("#cantidadTxtPrecio").val(precio);

        let encontrado = false;

        $("#tblEntradaPiezasTemporal tbody tr").each(function () {
            var valorPrimeraColumna = $(this).find("td:first").text();
            if (parseInt(valorPrimeraColumna) === id) {
                encontrado = true;
                return false;
            }
        });


        if (encontrado === false)
            $("#mdlCantidad").modal("show");
        else
            Toast.fire({
                icon: 'error',
                title: 'La pieza ya existe en la tabla',
                timer: 5000
            });

        $("#cantidadTxtCantidad").val("").focus();

    });

    $("#btnSaveCantidad").click(function () {
        let cantidad = $("#cantidadTxtCantidad").val().trim();
        let codigo = $("#cantidadTxtCodigo").val().trim();
        let descripcion = $("#cantidadTxtDescripcion").val().trim();
        let precio = $("#cantidadTxtPrecio").val().trim();
        let estadoSave = true;

        if (cantidad === "" || cantidad==="0") {
            $("#cantidadTxtCantidad").addClass("is-invalid");
            estadoSave = false;
        }

        if (precio === "" || precio==="0" || precio==="0.0" || precio==="0.00") {
            $("#cantidadTxtPrecio").addClass("is-invalid");
            estadoSave = false;
        }

        // Formateando valores
        cantidad = parseInt(cantidad);
        precio = parseFloat(precio);

        // Guardar pieza en tabla temporal
        if (estadoSave) {

            var encontrado = false;

            $("#tblEntradaPiezasTemporal tbody tr").each(function () {
                var valorPrimeraColumna = $(this).find("td:first").text();
                if (valorPrimeraColumna === codigo) {
                    encontrado = true;
                    return false;
                }
            });

            if (!encontrado)
                $("#tblEntradaPiezasTemporal tbody").append("<tr><td>" + codigo + "</td><td>" + descripcion + "</td><td>" + cantidad + "</td><td>" + precio + "</td><td><button onclick='deletePiezaTemporal(this)' class='btn btn-danger'><i class='fas fa-trash'></i></button> </td></th></tr>");
            else
                Toast.fire({
                    icon: 'error',
                    title: 'La pieza ya existe en la tabla',
                    timer: 5000
                });

            $("#mdlCantidad").modal("hide");
        }

    });

    $("#btnSave").click(function () {
        if (gId == null)
            save();
        else
            update()
    });

    $(".btnEdit").click(function () {
        estadoContenedorPrecios(1); // Mostramos detalle de precios
        let id = $(this).data('id');
        gId = id;
        let descripcion = $(this).data('descripcion');
        let codigoReferencia = $(this).data('codigo');
        $("#txtCodigo").val(id);
        $("#txtCodigoReferencia").val(codigoReferencia);
        $("#txtDescripcion").val(descripcion);
        $("#mdlPieza").modal("show");

        getDetallePrecios(); // Muestra los detalles de los precios
    });

    // Mostrar detalle de la entrada
    $(".btnDetalle").click(function () {
        let id = $(this).data('id');
        let descripcionBodega = $(this).data('descripcionbodega');
        let descripcion = $(this).data('descripcion');
        console.log(estado);

        $("#txtDetalleCodigo").val(id);
        $("#txtDetalleBodega").val(descripcionBodega);
        $("#checkDetalleActivo").val(estado);
        $("#mdlDetalleEntrada").modal("show");
    });


});

// ELIMINAR PIEZA TEMPORAL
function deletePiezaTemporal() {

}

// LEE LOS DETALLES DE LOS PRECIOS
function getDetallePrecios() {

    $('#tblDetallePrecios').empty();

    let datos = new FormData();
    datos.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());
    datos.append('get', 1); // Leer detalle de precios
    datos.append('id', gId); // Id de la pieza


    $.ajax({
        type: 'POST',
        url: "{% url 'public:getPieza'%} ",
        data: datos,
        dataType: 'json',
        cache: false,
        processData: false,  // importante
        contentType: false, // importante
        enctype: 'multipart/form-data',  // and here
        success: function (data) {

            if (data.length === 0) {
                Toast.fire({
                    icon: 'error',
                    title: 'Esta pieza no posee entradas',
                    timer: 10000
                });

                var tr = $('<tr>');
                tr.append('<td><div class="alert alert-danger" role="alert"> No hay entradas para esta pieza </div></td>');
                $('#tblDetallePrecios').append(tr);

            } else {
                $.each(data, function (index, element) {
                    var tr = $('<tr>');
                    tr.append($('<td>').text(element.cantidad));
                    tr.append($('<td>').text(element.precio));
                    $('#tblDetallePrecios').append(tr);
                });
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

// GUARDAR USUARIO
function save() {

    let descripcion = $("#txtDescripcion").val().trim();
    let id_bodega = $("#selectBodega").val().trim();
    let entradas = [];
    let estadoActivo = 0;
    let estadoSave = true

    if ($("#checkActivo").is(":checked"))
        estadoActivo = 1;

    if (descripcion === "") {
        estadoSave = false;
        $("#txtDescripcion").addClass("is-invalid");
    }

    if(id_bodega === "0")
    {
        estadoSave = false;
        Toast.fire({
            icon: 'error',
            title: 'Seleccione bodega',
            timer: 5000
        });

    }

    $('#tblEntradaPiezasTemporal tbody tr').each(function () {
        var row = [];
        // Recorrer todas las celdas de la fila
        $(this).find('td:not(:last-child)').each(function () {
            // Agregar el valor de la celda al arreglo
            row.push($(this).text());
        });
        // Agregar la fila al arreglo de datos
        entradas.push(row);
    });

    if (entradas.length === 0) {
        Toast.fire({
            icon: 'error',
            title: 'No ha seleccionado piezas',
            timer: 5000
        });
        estadoSave = false;
    }

    if (estadoSave) {

        let datos = new FormData();
        datos.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());
        datos.append('descripcion', descripcion);
        datos.append('id_bodega', id_bodega);
        datos.append('estadoActivo', estadoActivo);
        datos.append('entradas', JSON.stringify(entradas));

        alertify.confirm('CONFIRMACIÓN', '¿Dsea guardar la Entrada?', function () {
                $.ajax({
                    type: 'POST',
                    url: "/entradapiezas/",
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

                            showLoad(false);

                        } else {

                            Toast.fire({
                                icon: 'success',
                                title: respuesta.mensaje,
                                timer: 10000
                            });

                            showLoad(false);
                            location.reload();
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

// GUARDAR USUARIO
function update() {

    let codigo = $("#txtCodigo").val().trim();
    let descripcion = $("#txtDescripcion").val().trim();
    let estadoActivo = false;
    let estadoSave = true

    if ($("#checkActivo").is(":checked"))
        estadoActivo = true;

    if (descripcion == "")
        $("#txtDescripcion").addClass("is-invalid");

    if (descripcion == "")
        estadoSave = false

    if (estadoSave) {
        let datos = {};
        datos['csrfmiddlewaretoken'] = $("input[name='csrfmiddlewaretoken']").val();
        datos['id'] = gId;
        datos['descripcion'] = descripcion;
        datos['estadoActivo'] = estadoActivo;

        alertify.confirm('CONFIRMACIÓN', '¿Desea actualizar la Pieza?', function () {
                $.ajax({
                    type: 'POST',
                    url: "{% url 'public:updatePieza'%} ",
                    data: datos,
                    dataType: 'json',
                    success: function (respuesta) {
                        if (respuesta.error) {
                            if (respuesta.option == "1") {
                                Toast.fire({
                                    icon: 'error',
                                    title: respuesta.mensaje,
                                    timer: 5000
                                });

                                $("#txtDescripcion").addClass("is-invalid");

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

// ELIMINAR UNA EMPRESA
function deletePieza(id) {

    let datos = new FormData();
    datos.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());
    datos.append('crud', 3);
    datos.append('id', id);

    alertify.confirm('CONFIRMACIÓN', '¿Desea eliminar la empresa?', function () {
            $.ajax({
                type: 'POST',
                url: "{% url 'public:updatePieza'%} ",
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

// VALIDA INPUTS
function validarInputs() {

    // Solamente letra
    $("#txtDescripcion").on("input", function () {
        var value = $(this).val().replace(/[^a-zA-Z0-9\s]+/g, '');
        $(this).val(value);
    });

    // Solamente numero
    $("#txtCodigoReferencia").on("input", function () {
        var value = $(this).val();
        if (!/^[a-zA-Z0-9]+$/.test(value)) {
            $(this).val(value.replace(/[^a-zA-Z0-9]+/g, ''));
        }
    });

    // Solamente nùmeros
    $("#cantidadTxtCantidad").on("input", function () {
        var value = $(this).val();
        if (!/^[0-9]+$/.test(value)) {
            $(this).val(value.replace(/[^0-9]+/g, ''));
        }
    });

    // Números decimales con punto y dos decimales
    $("#precioTxt").on("input", function () {
        var value = $(this).val();
        if (!/^(\d+)?([.]?\d{0,2})?$/.test(value)) {
            $(this).val(value.replace(/[^\d.]/g, ''));
        }
    });

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

// ESTADO CONTENEDOR PRECIOS
function estadoContenedorPrecios(accion) {
    const method = accion === 0 ? 'hide' : 'show';
    $("#contenedorCantidad, #contenedorTablaPrecios")[method]();
}