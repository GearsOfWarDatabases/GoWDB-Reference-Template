# GoWDB-Reference-Template

A template for the screenshots behind a game database site: one repository per database, made from
[GoWDB-Template](https://github.com/GearsOfWarDatabases/GoWDB-Template), kept as that site's `ref/` submodule.
Like [GoW5DB-Reference](https://github.com/GearsOfWarDatabases/GoW5DB-Reference) for
[GoW5DB](https://github.com/GearsOfWarDatabases/GoW5DB), without its Gears 5 screenshots and sorting rules.

## Set it up

1. **Use this template** → name it after the database, e.g. `GoW4DB-Reference`.
2. In the database repository: `git submodule add https://github.com/<owner>/GoW4DB-Reference.git ref`, then
   commit. Its Reference update workflow keeps `ref/` up to date every day.
3. Set `SOURCE` at the top of `import-screenshots.py` to the game's Steam screenshots folder:
   `Steam\userdata\<your id>\760\remote\<the game's app id>\screenshots`.

## Adding screenshots

```
python import-screenshots.py              import from SOURCE (or double-click import-screenshots.bat)
python import-screenshots.py D:\shots     import from another folder
python import-screenshots.py --dry-run    show what would happen
```

Needs `pip install pillow`. Each new screenshot is saved as `shot-NNNN.jpg` with no metadata and its file dates
set to 2000-01-01, so nothing shows who took it or when; `_import-log.csv` remembers what was imported (by
content) so nothing comes in twice. Then move them into the section folders (`Characters/`, `Weapons/`, ...: add
any your site has) and commit.

GoW5DB-Reference's `sort-screenshots.py` sorts Gears 5 screenshots by reading them (OCR); a script like that is
game-specific, so start from it if you want the same for another game.

## Running the site locally (Windows)

`start-jekyll.bat` starts the database site from wherever this folder is inside it (it walks up to the folder with
`_config.yml`), fills in the revision line in the header, and stops an old server still using port 4000.

## License

The scripts and notes: Copyright (C) 2026 [Ryan Turner (TheSCREWEDSoftware)](https://github.com/TheSCREWEDSoftware)
and the GoW5DB contributors, under the GNU Affero General Public License, version 3 or (at your option) any later
version. See [LICENSE](LICENSE).

Screenshots show their games, whose names, images and other content belong to their owners. They are kept as
reference for non-commercial fan projects and are not covered by this license.

## Made with

Made with the help of [Claude](https://claude.ai), Anthropic's AI assistant: written and reviewed together with it,
then tested and published by [Ryan Turner (TheSCREWEDSoftware)](https://github.com/TheSCREWEDSoftware).
