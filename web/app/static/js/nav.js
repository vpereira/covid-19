$(document).ready(function() {
    $('a.nav-link').click(function(e) {
        e.preventDefault();
        $(document.body).load($(this).attr('href'));
        $('.nav-link.active').removeClass('active');
        $(this).addClass('active');
    });
    dfType = $('#country-title').data('dftype');
    country = $('#country-title').data('country')
    $('a.nav-link.active').removeClass('active')
    $.each($('.nav-item'), function() {
        if($(this).find('a').attr('href') == '/country/' + dfType + '/' + country) {
            $(this).find("a").addClass("active");
        }
    });
});