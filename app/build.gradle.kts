plugins { id("com.android.application") version "8.9.0" }
android {
    namespace = "com.threelens.watchface"
    compileSdk = 36
    defaultConfig {
        applicationId = "com.threelens.watchface"
        minSdk = 36
        targetSdk = 36
        versionCode = 4
        versionName = "1.3"
    }
    buildTypes { release { isMinifyEnabled = false } }
}
