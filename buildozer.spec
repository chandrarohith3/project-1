[app]

title = MyApp
package.name = myapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3==3.7.6,hostpython3==3.7.6,kivy,kivymd,plyer,pillow

orientation = portrait
fullscreen = 0
osx.python_version = 3
osx.kivy_version = 2.1.0

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/splash.png

# Supported orientation options: landscape, portrait, all, sensor
orientation = portrait

# Android
android.api = 33
android.minapi = 22
android.ndk = 23b
android.ndk_path =
android.sdk_path =
android.gradle_dependencies = 
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,FOREGROUND_SERVICE,WAKE_LOCK,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.archs = armeabi-v7a,arm64-v8a
android.entrypoint = org.kivy.android.PythonActivity
android.logcat_filters = *:S python:D
android.wakelock = True
android.allow_backup = True
android.support = False

# (str) Path to a custom Java class that implements PythonActivity
# android.activity_class_name = org.kivy.android.PythonActivity

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (bool) Hide the statusbar
# android.hide_statusbar = 1

# Build options
# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) Android entry point, default is ok
# android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is 'import android' (crash fix)
# android.theme = '@android:style/Theme.NoTitleBar'

# (list) Pattern to whitelist for the whole project
android.whitelist =

# (list) List of gradle dependencies to be included
# android.gradle_dependencies = com.google.android.gms:play-services-location:17.0.0

# Set this to True if you want to compile with Crystax NDK
# android.use_crystax = False

# (list) Application java .jars to add to the libs dir
# android.add_jars =

# (str) Path to custom build.gradle file
# android.gradle_file =

# (list) Permissions
# android.permissions = INTERNET,ACCESS_FINE_LOCATION

# (str) Entry point where the main.py file is located
# source.include_exts = py,png,jpg,kv,atlas

[buildozer]
log_level = 2
warn_on_root = 1
# (str) Path to build artifact storage, default is ./.buildozer
build_dir = ./.buildozer

# (str) Log file to output Buildozer log
# log_filename = buildozer.log

# (str) Specify which version of python for buildozer
# python_version = 3

# (str) Path to virtualenvs
# virtualenv_dir =

# (bool) Enable the use of GitHub tarball
# use_git_tarball = False

# (str) Additional directory to look for requirements
# requirements_path =

# (bool) Clean before building
# clean_build = False

# (str) Custom source dir
# source.dir = .

# (str) Directory to put the final apk
# bin_dir = ./bin

# (str) Directory to put the .buildozer
# build_dir = ./.buildozer
