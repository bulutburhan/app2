[app]
title = Odak Sayaci
package.name = odakapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3, kivy, android
orientation = portrait
android.permissions = ACCESS_NOTIFICATION_POLICY
android.api = 31
android.minapi = 21

[buildozer]
log_level = 2

warn_on_root = 1

