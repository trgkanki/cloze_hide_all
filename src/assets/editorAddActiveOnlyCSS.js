require('anki/RichTextInput').lifecycle.onMount(async ({ customStyles }) => {
  const { addStyleTag } = await customStyles
  const { element: styleTag } = await addStyleTag('customStyles')
  styleTag.textContent = `
      .cz_on_active {
        border: 2px dashed #38f;
        border-collapse: collapse;
        min-height: 1em;
        padding: .1em;
      }
      table..cz_on_active, div.cz_on_active {
        border: 2px dashed #f43;
      }
    `
})
