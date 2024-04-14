[app]

# (str) Title of your application
title = POSApp

# (str) Package name
package.name = TaptoPay

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (str) Main entry point of your application
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = assets/*,images/*.png

# (list) Application requirements
requirements = kivy, stripe, requests, pyjnius, android, python-dotenv, plyer

# (str) The version of your application, as used for versioning your app
version = 1.0.0

# (str) The Android API to use, run `buildozer android list-targets` to see the available options
android.api = 30

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
arch = arm64-v8a

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate whether the application should be fullscreen or not
fullscreen = 0

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (list) Pattern to whitelist for the whole project
#p4a.whitelist = 

# (bool) If True use the uncrustify tool to clean the code
#android.uncrustify = False

# (bool) Turn debug on
#debug = False

# (str) Android app theme, must be a valid android theme
#android.theme = '@android:style/Theme.NoTitleBar.Fullscreen'

# (str) Android Gradle version to use
# By default, it's gralde-4.10.3
#android.gradle = 4.10.3

# (bool) Indicate whether the application should be fullscreen or not
#fullscreen = 0

# (list) Services to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = False

# (str) Android additional Gradle parameters
# (This is an advanced feature and should be a list of key value pairs.)
#android.gradle_project_ext = {'archivesBaseName': 'POSApp', 'versionCode': '1'}

# (str) Android Gradle dependencies
# (This is an advanced feature and should be a list of comma separated strings.)
#android.gradle_dependencies = com.google.firebase:firebase-core:16.0.1, com.google.firebase:firebase-messaging:17.6.0

# (str) Android build tools version
#android.build_tools_version = 28.0.3

# (bool) Android add --no-window flag
#android.no_window = False

# (bool) Android disable automatic rotation
#android.rotation = 0
