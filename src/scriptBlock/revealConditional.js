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

  // Show clozes with proper constraints
  const clozeBoxWithConstraintList = document.querySelectorAll('cloze2_w[data-reveal-constraint]')
  for (const box of clozeBoxWithConstraintList) {
    let { revealConstraint, clozeId } = box.dataset
    revealConstraint = revealConstraint.replace('&gt;', '>')
    revealConstraint = revealConstraint.replace('&lt;', '<')
    let shouldReveal = false

    if (revealConstraint === '') shouldReveal = true
    const m = revealConstraint.match(/^(<|<=|>|>=|==)(\d*)$/)
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
        element.style.display = 'inline'
      }
      box.style.display = 'none'
    }
  }
}, 0)
