# run-dev-client.ps1

# --- Set up Android SDK (if needed) ---
$env:ANDROID_HOME = "$env:USERPROFILE\AppData\Local\Android\Sdk"
$env:Path += ";$env:ANDROID_HOME\platform-tools;$env:ANDROID_HOME\emulator"

# --- Move to project directory ---
Set-Location "C:\Users\natha\Py_Coding_Projects\Keyhole_Automation_Platform\frontend\Keyhole-Solution-App"

# --- Start Expo Dev Client on Android ---
npx expo run:android
