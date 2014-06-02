var $ = require('jquery'),
    Filter = require('filter');

// Collapsible articles
$('article').each(function () {
    var that = $(this);
    var header = that.children('a');
    var body = that.children('.body');
    body.hide();
    header.toggle(
        function () { body.slideDown('fast'); that.addClass('active'); },
        function () { body.slideUp('fast'); that.removeClass('active'); }
    );
});

var anchor = window.location.hash.substring(1);
if (anchor) $('article a[name=' + anchor + ']').trigger('click');

// Expanding the article on link click and scrolling down to it
$('#sidebar a').each(function () {
    var that = $(this);
    var id = that.attr('href').substring(1);
    that.click(function (e) {
        var header = $('article a[name="'+ id +'"]')
        if (!header.parent().hasClass('active')) header.trigger('click');
        $('html, body').animate({ scrollTop: header.offset().top }, 'fast');
    });

    // If we find a link in the body with similar anchor, add the same behavior
    $('.body a[href=#'+ id +']').click(function (e) {
        $('#sidebar a[href=#'+ id +']').trigger('click');
    });
});

// Hide all/Show all/Printable links
var show = $('<a class=\'control show\'>Show all</a>');
show.click(function () {
  $('#content article:not(".active") > a').trigger('click');
});

var hide = $('<a class=\'control hide\'>Hide all</a>');
hide.click(function () {
  $('#content article.active > a').trigger('click');
});

var printable = $('<a class="control printable">Printable</a>')
printable.click(function() {
  $('#toc-label').css({
    display: 'block'
  });
  show.trigger('click');
  $('#sidebar').css({
    float: 'none',
    height: 'auto',
    position: 'static',
    width: 'auto',
    'max-width': '7.0in',
    margin: '0 auto'
  });
  $('#content').css({
    'padding-left': '20px',
    'max-width': '7.0in',
    margin: '0 auto'
  });
  $('ul#links input').hide();
  $('#content > a.control').hide();
});

$('#content').prepend(printable);
$('#content').prepend(show);
$('#content').prepend(hide);

// Making our navigation sticky
new Filter($('#sidebar > ul'));
