(function () {
  const hideBackCaption = 'Hide others on the back side'

  const fieldNames = document.querySelectorAll('#fields .fname')
  for (const fieldNameEl of fieldNames) {
    if (fieldNameEl.innerHTML === hideBackCaption) {
      const fieldNameTr = fieldNameEl.parentElement
      const fieldContentTr = fieldNameTr.nextElementSibling

      // Little paler.
      fieldNameEl.classList.add('cha-hideback-disabled-fieldname')
      fieldContentTr.classList.add('cha-hideback-disabled-field')
    }
  }

  // Add stylesheet for fn-cha
  let styleEl = document.getElementById('fn-cha-stylesheet')
  if (!styleEl) {
    styleEl = document.createElement('style')
    styleEl.id = 'fn-cha-stylesheet'
    document.head.appendChild(styleEl)
  }
  styleEl.innerHTML = `
.cha-hideback-disabled-fieldname {
  font-style: italic;
  opacity: 0.8;
}

.cha-hideback-disabled-fieldname:after {
  padding-left: 2em;
  opacity: 0.5;
  content: '(unused, hidden)';
}

.cha-hideback-disabled-field {
  display: none;
}
  `
})()
