var piesiteFired = 0;
$(document).ready(function() {

    ///////////////////////////////////////
    // Bar Charts scroll activate, looking for .trigger class to fire.
    $(this).each(function(key, bar) {
        var percentage = $(this).data("percentage");
        $(this).css("height", percentage + "%");

        ///////////////////////////////////////
        //        Animated numbers
        $(this).prop("Counter", 0).animate(
            {
                Counter: $(this).data("percentage")
            },
            {
                duration: 5000,
                easing: "swing",
                step: function(now) {
                    $(this).text(Math.ceil(now));
                }
            }
        );
        //        Animated numbers
        ///////////////////////////////////////
    });









scrollReveal();
});



