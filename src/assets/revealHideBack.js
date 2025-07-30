setTimeout(function() {
  if (
    !document.querySelector('*[cha-enable]') &&
    !document.querySelector('img[src="_cha_cha-enable.png"]')
  ) return
  if (document.getElementById('cloze2-toggle')) return

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

  const toggleButton = document.createElement('button')
  toggleButton.id = 'cloze2-toggle'
  toggleButton.innerHTML = 'Toggle mask'
  toggleButton.addEventListener('click', function() {
    const elements = document.querySelectorAll('cloze2, cloze2_w')
    for (let i = 0; i < elements.length; i++) {
      elements[i].classList.toggle('reveal-cloze2')
    }
  })

  const scriptElements = document.getElementsByClassName('cha-hideback-js')
  const lastScriptElement = scriptElements[0]
  lastScriptElement.parentNode.insertBefore(toggleButton, lastScriptElement)
}, 0)
