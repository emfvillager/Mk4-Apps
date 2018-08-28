"""Official TiLDA MK4 Badge Store App

switches between app libraries, updates and installs apps.

To publish apps use https://badge.emfcamp.org"""

___license___      = "MIT"
___title___        = "Badge Store"
___dependencies___ = ["badge_store", "dialogs", "ugfx_helper", "app", "database"]
___categories___   = ["System"]
___bootstrapped___ = True

import ugfx_helper, os, database, wifi, app
from dialogs import *
from lib.badge_store import BadgeStore

### VIEWS ###

ugfx_helper.init()

url = database.get("badge_store.url", "http://badgeserver.emfcamp.org/2018")
repo = database.get("badge_store.repo", "emfcamp/Mk4-Apps")
ref = database.get("badge_store.ref", "master")
store = BadgeStore(url=url, repo=repo, ref=ref)
title = "TiLDA Badge Store"

def clear():
    ugfx.clear(ugfx.html_color(0x7c1143))

def show_categories():
    with WaitingMessage():
        menu_items = [{"title": c, "category": c} for c in store.get_categories()]

    option = prompt_option(menu_items, none_text="Back", text="Categories", title=title)

    if option:
        show_apps(option["category"])
    else:
        return

def show_apps(c):
    menu_items = [{"title": a, "app": a} for a in store.get_apps(c)]

    option = prompt_option(menu_items, none_text="Back", title=title)

    if option:
        show_app(option["app"])
    else:
        return

def show_app(a):
    with WaitingMessage():
        app_info = store.get_app(a)

    install = prompt_boolean(app_info["description"], title=a, true_text="Install", false_text="Back")

    if install:
        with WaitingMessage(title="Installing %s" % a, text="Please wait...") as message:
            installers = store.install(_get_current_apps() + [a])
            n = len(installers)
            for i, installer in enumerate(installers):
                message.text = "%s (%s/%s)" % (installer.path, i + 1, n)
                installer.download()

    notice("App %s has been successfully installed" % a, title=title, close_text="Back")

def show_update():
    None

def show_remove():
    None

def main_menu():
    while True:
        clear()

        print()

        menu_items = [
            {"title": "Install Apps", "function": show_categories},
            {"title": "Update", "function": show_update},
            {"title": "Manage Apps", "function": show_remove}
        ]

        option = prompt_option(menu_items, none_text="Exit", text="What do you want to do?", title=title)

        if option:
            option["function"]()
        else:
            app.restart_to_default()

def _get_current_apps():
    return [a.name for a in app.get_apps()]

wifi.connect(show_wait_message=True)
main_menu()
#show_app("launcher")
