setTimeout(function () {
  var clozeBoxes = document.querySelector('.cloze cloze2_w')
  var elements = document.querySelectorAll('cloze2.' + clozeBoxes.className)
  for (var i = 0; i < elements.length; i++) {
    elements[i].style.display = 'inline'
  }
}, 0)
