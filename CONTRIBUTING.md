# Contributing

Issues and pull requests are welcome.

- Do not edit `app/src/main/res/raw/watchface.xml` by hand. Change `tools/generate_watchface.py` and re-run it
  (see `docs/ARCHITECTURE.md`), then commit both files.
- Keep the XML valid for Watch Face Format version 3 unless you also raise the declared version in the manifest.
- When you add a customization option, add its label strings (the generator does this for the lists in the script) and
  describe it in `docs/CUSTOMIZATION.md`.
- For bugs, attach the `adb logcat` output described in `docs/TROUBLESHOOTING.md`.

By contributing you agree that your contribution is released under the MIT license.
