function listadoUsuarios(){
    $.ajax({
        /* url donde se realiza la peticion */
        url:"/listar_usuarios/",
        /* Método HTTP que se realizara */
        type: "get", 
        /* Tipo de dato con el que se trabaja, generalmente json */
        dataType:"json",
        /* Lo que va  pasar si la peticion que realizamos es correcta */
        success: function(response){
            console.log(response);
        },
        error: function(error){
            console.log(error);
        }
    });
}

/* Se ejecuta la funconi listadoUsuarios una vez que el documento está cargado */
$(document).ready(function(){
    listadoUsuarios();
})