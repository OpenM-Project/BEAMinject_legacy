<div align=center>
    <h1>BEAMinject</h1>Memory injection unlocker for Minecraft: Windows 10 Edition</p>
</div>

-----

## :test_tube: ARM support
As of version 0.3.0, BEAMinject supports Windows ARM64!

Prebuilts are not avaiable yet,
but you can manually run it after installing Python:
```sh
pip install -r requirements.txt
py app.py
```

## :wrench: Versions
BEAMinject comes in 2 versions:
- **BEAMinject:** Used for silently launching Minecraft then exiting
    - Recommended for most users
- **BEAMinject_GUI:** GUI version, mostly used for debugging etc.
    - Includes toggles for launching Minecraft, displays injection logs

We recommend trying BEAMinject first, and if you have issues, you can move to the GUI version for debugging.

## :inbox_tray: Downloads
You can download the latest nightly release [here](https://nightly.link/OpenM-Project/BEAMinject/workflows/build/main?preview).

## :rotating_light: About AV detections
Some poorly designed AVs *(namely Microsoft, Avast and AVG)* might detect our packed Python executables as a trojan.

There is [**nothing we can do about this**](https://github.com/pyinstaller/pyinstaller/issues/6754#issuecomment-1100821249) except sign the binaries, which is [***really* expensive**](https://codesigncert.com/blog/code-signing-certificate-cost).

Since the code is open and all builds are distributed via GitHub Actions, you can confirm that the executable is safe and whitelist it in your AV software!

## :computer: Support
This only works on Windows,
and won't be ported to other platforms *(for obvious reasons)*.

For all support needed, you can open an issue!
And you can join our [Discord](https://dsc.gg/openm "OpenM Community") server
for further support needed.

## :page_with_curl: License
All code and assets are licensed under GNU AGPLv3.
