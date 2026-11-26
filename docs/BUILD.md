# Building and installing

You do **not** need Android Studio. GitHub builds the APK for you.

## Build with GitHub Actions (no tools needed)

1. Push this repository to your GitHub account.
2. Open the **Actions** tab. The *Build watch face* workflow runs on every push (or press **Run workflow**).
3. When it turns green, open the run and download the **noma-watchface-apk** artifact. Unzip it to get `app-debug.apk`.

### Publishing a release

Create and push a tag such as `v1.3` (or use *Releases > Draft a new release* on GitHub). The *Release* workflow builds the
APK and attaches it to the release automatically.

```bash
git tag v1.3
git push origin v1.3
```

## Build locally

Requirements: JDK 17, Android SDK (platform 36), Gradle 8.11+.

```bash
gradle :app:assembleDebug
# output: app/build/outputs/apk/debug/app-debug.apk
```

## Install on the watch

1. On the watch: Settings > About watch > Software, tap **Software version** (or Build number) 7 times to enable developer mode.
2. Settings > Developer options: turn on **ADB debugging** and **Debug over Wi-Fi**. Note the IP address and port.
3. On your computer install Google's [platform-tools](https://developer.android.com/tools/releases/platform-tools) and run:

```bash
adb connect <watch-ip>:<port>
adb install -r app-debug.apk
```

4. Long-press the current watch face, swipe to the end, tap **+** and choose **Noma Wheels**.

If pairing is requested first (`adb pair <ip>:<pairing-port>`), use the code shown in *Wireless debugging*.
