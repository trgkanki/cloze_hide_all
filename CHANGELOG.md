# Changelog of cloze_hide_all

In case you're using this addon well, consider supporting me via [patreon](https://www.patreon.com/trgk) :)
If you encounter any bugs, submit through [Github issues](https://github.com/trgkanki/remaining_time/issues) page.

-----

[comment]: # (DO NOT MODIFY. new changelog goes here)

## 20.11.12i127 (2020-11-12)

- fix: another template bug fixer
- feat: option to reset broken templates. If your card is broken, try following [this instruction](docs/bad_template/instruction.html).
  ![example](docs/bad_template/bad_example.png)

## 20.10.21i160 (2020-10-21)

- Fix: supports deleted hideback field ( :( )
- Fix: Scroll to cloze on back side of the card

## 20.10.19i72 (2020-10-19)

- Fix: 'Reveal all' button not working
- Fix: 'Reveal all' button looks more native
- Feature: addon asks if you want to disable model migration script.

## 20.10.12i16 (2020-10-12)

- Feature: `Hide others on the back side` field will be disabled when `alwaysHideback` is on.
- Fix: CSS being piled up on every Anki run
- Fix: Compatibility with Anki 2.1.28 : Note type update fixed
- Typo: *Toogle* mask →  ***Toggle*** mask

## 20.9.26i168 (2020-09-27)

- addon related html won't be shown on html edit windows
- AMBOSS compatibility: new syntax for always-shown closes. `{{c1::?text}}`

## 20.7.21i30 (2020-07-21)

- Proper cloze color on dark mode.
- Bug fix: Flash of other cloze contents on ankidroid fixed.
- Bug fix: Proper scrolling to cloze site on ankidroid.
- Bug fix: Compatibility with old anki version: `addon_meta` error fixed.
- Bug fix: When setting alwaysHideback option to false from true, template were not being
  reverted to its original state.

## 20.7.6i110 (2020-07-06)

- Added option to always turn on 'Hide others on the back side' option
- Added option to disable automatic template update/migration, as it seems to effect some people's card styling issues.

## 20.6.24i65 (2020-06-24)

- Bug hotfix: yellow box on the current cloze, even on the back side

## 20.6.23i103 (2020-06-23)

- Hotfix: cloze custom style not found on linux

## 20.6.20i63 (2020-06-20)

Fixed packager coe :(

## 20.6.20i59 (2020-06-20)

- Feature: Change cloze styles via addon config
- Bugfix: some clozes not applied after edits
