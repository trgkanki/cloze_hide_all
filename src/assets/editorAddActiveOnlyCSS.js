require('anki/RichTextInput').lifecycle.onMount(async ({ customStyles }) => {
  const { addStyleTag } = await customStyles
  const { element: styleTag } = await addStyleTag('customStyles')
  styleTag.textContent = `
      .cz_on_active {
        border: 2px dashed #38f;
        min-height: 1em;
        padding: .1em;
        margin: .1em;
      }
    `
})
