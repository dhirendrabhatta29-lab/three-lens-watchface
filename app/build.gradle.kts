plugins { id("com.android.application") version "8.9.0" }
android {
    namespace = "com.threelens.watchface"
    compileSdk = 36
    defaultConfig {
        applicationId = "com.threelens.watchface"
        minSdk = 35
        targetSdk = 36
        versionCode = 2
        versionName = "1.1"
    }
    buildTypes { release { isMinifyEnabled = false } }
}
