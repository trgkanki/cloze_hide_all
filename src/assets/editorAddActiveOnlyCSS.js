if (!window._chaEditorAddActiveOnlyCSSInjected) {
  window._chaEditorAddActiveOnlyCSSInjected = true
  require('anki/RichTextInput').lifecycle.onMount(async ({ customStyles }) => {
    const { addStyleTag } = await customStyles
    const { element: styleTag } = await addStyleTag('chaStyle')
    styleTag.textContent = `
        .cz_on_active {
          outline: 2px dashed #38f;
          outline-offset: -1px;
          padding: .1em;
          min-height: 1em;
        }
        table.cz_on_active, span.cz_on_active {
          border: 2px dashed #f43;
        }
      `
  })
}
