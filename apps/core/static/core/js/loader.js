function showLoad(option) {
    if (option) {
        //
        $("#loader-wrapper").css("display", "block");
        $(".section-left").show("slide", {direction: "left"}, 500);
        $(".section-right").show("slide", {direction: "right"}, 500, function () {
            $("#loader").fadeIn();
        });
    } else {
        $("#loader").hide();
        $(".section-left").hide("slide", {direction: "left"}, 500);
        $(".section-right").hide("slide", {direction: "right"}, 500, function () {
            //$("#loader-wrapper").remove();
            $("#loader-wrapper").css("display", "none");
        });
    }
}