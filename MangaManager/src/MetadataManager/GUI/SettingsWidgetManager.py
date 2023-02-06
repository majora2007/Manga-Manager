from __future__ import annotations

import tkinter
from tkinter.ttk import LabelFrame, Label

from ExternalSources.MetadataSources.metadata import ScraperFactory
from src import MM_PATH
from src.Common.utils import open_folder
from src.MetadataManager.GUI.utils import center
from src.MetadataManager.GUI.widgets import ButtonWidget
from src.MetadataManager.GUI.widgets.FormBundleWidget import FormBundleWidget
from src.Settings.SettingHeading import SettingHeading
from src.Settings.SettingControl import SettingControl
from src.Settings.SettingControlType import SettingControlType
from src.Settings.SettingSection import SettingSection
from src.Settings.Settings import Settings

setting_control_map = {
    SettingHeading.Main: {
        "library_path": SettingControl("library_path", "Library Path", SettingControlType.Text, "", "The path to your library. This location will be opened by default when choosing files"),
        "covers_folder_path": SettingControl("covers_folder_path", "Covers folder path", SettingControlType.Text, "", "The path to your covers. This location will be opened by default when choosing covers"),
        "cache_cover_images": SettingControl("cache_cover_images", "Cache cover images", SettingControlType.Bool, False, "If enabled, the covers of the file will be cached and shown in the ui"),
        "selected_layout": SettingControl("selected_layout", "* Active layout", SettingControlType.Options, "", "Selects the layout to be displayed"),
    },
    SettingHeading.WebpConverter: {
        "default_base_path": SettingControl("default_base_path", "Default base path", SettingControlType.Text, "", "The starting point where the glob will begin looking for files that match the pattern"),

    },
    SettingHeading.ExternalSources: {
        "default_metadata_source": SettingControl("default_metadata_source", "Default metadata source", SettingControlType.Options, "The source that will be hit when looking for metadata"),
        "default_cover_source": SettingControl("default_cover_source", "Default cover source", SettingControlType.Options, "The source that will be hit when looking for cover images"),
    },
}

# TODO: Load dynamically loaded extensions (this will be moved in another PR)
providers = [ScraperFactory().get_scraper("MangaUpdates"), ScraperFactory().get_scraper("AniList")]


def populate_default_settings():
    default_settings = {}

    for section in setting_control_map:
        if section not in default_settings:
            controls = []
            for (key, value) in setting_control_map[section].items():
                setting = Settings().get(section, key)
                if setting is None:
                    continue

                controls.append(value)
        default_settings[section] = SettingSection(section, section, controls)
    return default_settings


class SettingsWidgetManager:
    validation_messages = ''

    def save_settings(self):
        """
        Saves the settings from the GUI to Setting provider and extensions that dynamically loaded their settings
        """
        # Validate the setting is correct before allowing any persistence
        is_errors = False
        for bundle in self.bundles:
            if bundle.control:
                if not bundle.validate():
                    is_errors = True
        if is_errors:
            return

        for bundle in self.bundles:
            if bundle.control:
                Settings().set(bundle.section.key, bundle.control.key, str(bundle.input_var.get()))

        # Tell Extensions that an update to Settings has occurred
        for provider in providers:
            provider.save_settings()

        Settings().save()

    def __init__(self, parent):
        self.strings_vars: list[tkinter.Variable] = []
        self.bundles: list[FormBundleWidget] = []

        settings_window = self.settings_window = tkinter.Toplevel(parent, pady=30, padx=30)
        settings_window.geometry("900x420")
        settings_window.title("Settings")

        main_frame = tkinter.Frame(settings_window)
        main_frame.pack(fill="both")
        self.widgets_frame = tkinter.Frame(main_frame, pady=30, padx=30)
        self.widgets_frame.pack(fill="y", expand=True)
        control_frame = tkinter.Frame(settings_window)
        control_frame.pack()
        ButtonWidget(master=control_frame, text="Save", tooltip="Saves the settings to the config file",
                     command=self.save_settings).pack()
        ButtonWidget(master=control_frame, text="Open Settings Folder",
                     tooltip="Opens the folder where Manga Manager stores it's files",
                     command=lambda x=None: open_folder(folder_path=MM_PATH)).pack()

        default_settings = populate_default_settings()

        self.settings_widget = {}
        print('Setting up settings for Manga Manager')
        for setting_section in default_settings:
            section = default_settings[setting_section]

            print('Setting up settings for ' + section.pretty_name)
            frame = LabelFrame(master=self.widgets_frame, text=section.pretty_name)
            frame.pack(expand=True, fill="both")

            self.settings_widget[section.pretty_name] = {}
            self.build_setting_entries(frame, section.values, section)

        print('Setting up settings for Extensions')
        for provider in providers:
            settings = provider.settings
            for section in settings:
                print('Setting up settings for ' + provider.name)
                frame = LabelFrame(master=self.widgets_frame, text=section.pretty_name)
                frame.pack(expand=True, fill="both")

                self.settings_widget[default_settings[SettingHeading.ExternalSources].pretty_name][section.pretty_name] = {}
                self.build_setting_entries(frame, section.values, section)

        center(settings_window)
        frame = Label(master=control_frame, text="\nNote: Fields marked with * need a restart to take effect")
        frame.pack(expand=True, fill="both")
        # TODO: Refactor this so each validation_message is packed under the setting control and is mapped via key
        self.validation_messages = tkinter.StringVar()
        self.validation_messages.set("")
        frame = Label(master=control_frame, textvariable=self.validation_messages)
        frame.pack(expand=True, fill="both")

    def build_setting_entry(self, parent_frame, control: SettingControl, section):
        # Update the control's value from Settings
        control.value = Settings().get(section.key, control.key)

        row = FormBundleWidget(parent_frame)\
            .with_label(control.name, control.tooltip)\
            .with_input(control, section)\
            .build()

        self.bundles.append(row)

    def build_setting_entries(self, parent_frame, settings, section):
        for i, setting in enumerate(settings):
            self.build_setting_entry(parent_frame, setting, section)