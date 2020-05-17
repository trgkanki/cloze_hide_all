var qFade, $

(function () {
  function scrollToCurrentCloze () {
    const $clozes = $('.cloze')

    // Code from https://stackoverflow.com/a/10130707
    function scrollIntoViewIfNeeded ($target) {
      if ($target.position()) {
        if ($target.position().top < $(window).scrollTop()) {
          // scroll up
          $('html,body').scrollTop($target.position().top - 30)
        } else if (
          $target.position().top + $target.height() >
          $(window).scrollTop() + (
            window.innerHeight || document.documentElement.clientHeight
          )
        ) {
          // scroll down
          $('html,body').scrollTop(
            $target.position().top -
            (window.innerHeight || document.documentElement.clientHeight) +
            $target.height() + 30
          )
        }
      }
    }
    if ($clozes[0]) {
      // Maybe selector .cloze may select multiple elements?
      scrollIntoViewIfNeeded($($clozes[0]))
    }
  }
  window.setTimeout(scrollToCurrentCloze, (qFade | 0) + 100)
})()
