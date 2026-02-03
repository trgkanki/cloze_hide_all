require('anki/RichTextInput').lifecycle.onMount(async ({ customStyles }) => {
  const { addStyleTag } = await customStyles
  const { element: styleTag } = await addStyleTag('customStyles')
  styleTag.textContent = `
      .cz_on_active {
        border: 2px dashed #38f;
        padding: .1em;
        min-height: 1em;
      }
      table.cz_on_active, span.cz_on_active {
        border: 2px dashed #f43;
      }
    `
})
