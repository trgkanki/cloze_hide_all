setTimeout(function () {
  if (!document.querySelector('*[cha-enable]')) return

  function scrollToCloze () {
    const element = document.getElementsByClassName('cloze')[0]
    const elementRect = element.getBoundingClientRect()
    const absoluteElementTop = elementRect.top + window.pageYOffset
    const middle = absoluteElementTop - (window.innerHeight / 2)
    window.scrollTo(0, middle)
  }
  if (typeof window.onShownHook !== 'undefined') {
    // for Anki 2.1.x
    window.onShownHook.push(scrollToCloze)
  } else {
    // for AnkiDroid
    setTimeout(scrollToCloze, 10)
  }
}, 0)
