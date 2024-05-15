(function () {
  const cssContent = `
  cloze2.reveal-cloze2 {
    display: inline;
  }

  cloze2_w.reveal-cloze2 {
    display: none;
  }

  #cloze2-toggle {
    display: block;
    font-size: 1.5em !important;
    padding: .5em 1em;
    margin: auto;
  }
`
  let styleEl = document.getElementById('cha-rhb-stylesheet')
  if (!styleEl) {
    styleEl = document.createElement('style')
    styleEl.id = 'cha-rhb-stylesheet'
    styleEl.innerHTML = cssContent
    document.head.appendChild(styleEl)
  }

  const toggleButton = document.getElementById('cloze2-toggle')
  toggleButton.addEventListener('click', function () {
    const elements = document.querySelectorAll('cloze2, cloze2_w')
    for (let i = 0; i < elements.length; i++) {
      elements[i].classList.toggle('reveal-cloze2')
    }
  })
})()
