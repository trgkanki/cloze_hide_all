// Reveal only current clozes here
setTimeout(function () {
  // Try getting current cloze number
  let currentClozeNumber = null

  {
    // 2.1.56+ - use 'data-ordinal' property.
    const clozeSpan = document.querySelector('span.cloze')
    if (clozeSpan) {
      currentClozeNumber = Number(clozeSpan.dataset.ordinal)
    }
  }

  // Fallback for older ankis
  if (currentClozeNumber === null) {
    const clozeBoxes = document.querySelector('.cloze cloze2_w') || document.querySelector('.cloze cz_hide')
    for (const cls of clozeBoxes.classList) {
      const m = cls.match(/^cz-(\d+)$/)
      if (m) {
        currentClozeNumber = Number(m[1])
        break
      }
    }
  }

  // Reveal current cloze
  for (const element of document.querySelectorAll('cloze2.cz-' + currentClozeNumber)) {
    element.classList.add('revealed')
  }
  for (const element of document.querySelectorAll('cloze2_w.cz-' + currentClozeNumber)) {
    element.classList.add('revealed')
  }


  // Show clozes with proper condition
  const clozeBoxWithConditionList = document.querySelectorAll('cloze2_w[data-reveal-condition]')
  for (const box of clozeBoxWithConditionList) {
    let { revealCondition, clozeId } = box.dataset
    revealCondition = revealCondition.replace('&gt;', '>')
    revealCondition = revealCondition.replace('&lt;', '<')
    let shouldReveal = false

    if (revealCondition === '') shouldReveal = true
    const m = revealCondition.match(/^(<|<=|>|>=|==)(\d*)$/)
    if (m) {
      const comparator = m[1]
      let rhs = NaN
      if (m[2]) rhs = Number(m[2])
      else {
        for (const cls of box.classList) {
          const m = cls.match(/^cz-(\d+)$/)
          if (m) {
            rhs = Number(m[1])
            break
          }
        }
      }

      shouldReveal = (
        (comparator === '>=' && currentClozeNumber >= rhs) ||
        (comparator === '>' && currentClozeNumber > rhs) ||
        (comparator === '<=' && currentClozeNumber <= rhs) ||
        (comparator === '<' && currentClozeNumber < rhs) ||
        (comparator === '==' && currentClozeNumber === rhs)
      )
    } if (shouldReveal) {
      for (const element of document.querySelectorAll('cloze2.czi-' + clozeId)) {
        element.classList.add('revealed')
      }
      box.classList.add('revealed')
    }
  }
}, 0)
