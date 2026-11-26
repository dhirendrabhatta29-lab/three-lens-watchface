plugins { id("com.android.application") version "8.9.0" }
android {
    namespace = "com.threelens.watchface"
    compileSdk = 36
    defaultConfig {
        applicationId = "com.threelens.watchface"
        minSdk = 35
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"
    }
    buildTypes { release { isMinifyEnabled = false } }
}
