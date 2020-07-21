var onShownHook

(function () {
  function scrollToCloze () {
    const element = document.getElementsByClassName('cloze')[0]
    const elementRect = element.getBoundingClientRect()
    const absoluteElementTop = elementRect.top + window.pageYOffset
    const middle = absoluteElementTop - (window.innerHeight / 2)
    window.scrollTo(0, middle)
  }
  if (typeof onShownHook !== 'undefined') {
    // for Anki 2.1.x
    onShownHook.push(scrollToCloze)
  } else {
    // for AnkiDroid
    setTimeout(scrollToCloze, 10)
  }
})()
