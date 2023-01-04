# Cloze (hide all) config

## hiddenClozeStyle

Specify what to show for hidden styles. Currently these things are supported

- yellowBox: default style. yellow box
- yellowBoxShort: somewhat shorter yellow box
- threeGrayDots: `[...]` in grayish version

## clozeHideAllModelNames

List of model names you'd like "hide all" code to work with. Original model name (`Cloze (Hide all)`) is always included.

- Default: `[]`
- Example: `["Clone of Cloze (Hide all)"]`

## noModelMigration

Prevent auto-migration of card template/css. Sometimes automatic model migration
may revert user edits repeatedly. Enable this option to prevent automatic card
model update.

## alwaysHideback

Always turn on 'Hide others on the back side' option for all cloze cards.

# shortcutToggleMask (default: `"ctrl+r"`)

Shortcut for `Toggle Mask` button.