# Troubleshooting

**The face does not appear in the picker.**
Make sure the install says `Success`, then restart the watch. Long-press the face, swipe to the end and tap **+**.

**The face is blank or crashes after selecting it.**
Capture the error right after selecting it:

```bash
adb logcat -d | findstr -i watchface     # Windows
adb logcat -d | grep -i watchface        # macOS / Linux
```

The runtime reports the element it rejects. Please attach that output to a bug report.

**The rings do not rotate.**
Open Customize and check that *Seconds ring motion* and *Minutes ring motion* are not set to Hidden / Instant.

**A complication shows nothing.**
The data provider may need a permission (for example Samsung Health for heart rate). Open the provider's app once and
grant the requested permissions, then re-select the complication.

**Text in some other language looks different.**
The bundled font is subset to Latin scripts to keep the APK small. Other scripts fall back to the system font.

**It uses a lot of battery.**
Use *Tick* or *Hidden* for the seconds ring, a dark palette with *Pure black* background, and one of the sparse always-on styles.
