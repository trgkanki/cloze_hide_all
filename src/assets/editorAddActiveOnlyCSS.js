require('anki/RichTextInput').lifecycle.onMount(async ({ customStyles }) => {
  const { addStyleTag } = await customStyles
  const { element: styleTag } = await addStyleTag('customStyles')
  styleTag.textContent = `
      .cz_on_active {
        border-collapse: collapse;
      }
      .cz_on_active td {
        border: 2px dashed #38f;
        border-collapse: collapse;
        min-height: .5em;
        padding: .1em;
      }

    `
})
