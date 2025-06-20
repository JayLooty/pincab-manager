#!/usr/bin/python3
"""Context"""

import atexit
import json
import os
from pathlib import Path
import re
import socket
import configparser
import locale

from selenium import webdriver

from libraries.constants.constants import Action, Category, Component, Emulator, Constants, Media

# pylint: disable=unnecessary-comprehension, too-many-public-methods
# pylint: disable=too-many-branches


class Context:
    """Class to store context"""

    __initialized: bool = False
    __hostname: str = None
    __app_version: str = None
    __lang_code: str = None
    __monitor: int = None
    __texts = {}
    __vpinball_path: Path = None
    __data_path: Path = None
    __selected_category: Category = None
    __selected_emulator: Emulator = None
    __selected_action: Action = None
    __selected_components = []
    __selected_tables_rows = []
    __selected_playlists_rows = []
    __selected_bdd_tables_rows = []
    __selected_configs_rows = []
    __selected_folder_path = None
    __simulated: bool = False
    __auto_refresh: bool = False
    __available_emulators = []
    __available_media = []
    __screen_number_by_media = {}
    __selenium_web_browser = None

    @staticmethod
    def init():
        """Initialize context"""

        if Context.__initialized:
            raise Exception(Context.get_text(
                'error_context_initialized'
            ))

        # Retrieve hostname
        Context.__hostname = socket.gethostname().lower()

        # Retrieve application's version
        try:
            with open('CHANGELOG', 'r', encoding='utf-8') as file:
                first_line = file.readline().strip()
                match = re.search(r'R(\d+\.\d+\.\d+)', first_line)
                if not match:
                    raise Exception('Cannot find app_version in CHANGELOG')
                Context.__app_version = match.group(1)
        except Exception:
            Context.__app_version = 'UNKNOWN'

        # Retrieve lang's code from OS language
        lang = locale.getlocale()[0]
        Context.__lang_code = 'fr' if lang.startswith('fr') else 'en'

        # Initialize selenium's web browser
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-logging"]
        )
        Context.__selenium_web_browser = webdriver.Chrome(
            options=chrome_options
        )
        Context.__selenium_web_browser.minimize_window()
        atexit.register(Context.__selenium_web_browser.quit)

        # Initialize paths
        Context.__vpinball_path = ''
        Context.__data_path = ''

        # Initialize monitor
        Context.__monitor = 0

        # Initialize boolean simulated
        Context.__simulated = False

        # Initialize boolean auto refresh
        Context.__auto_refresh = False

        # Specify that context is initialized
        Context.__initialized = True

        # Update context from setup
        Context.update_context_from_setup()

    @staticmethod
    def destroy():
        """Destroy context"""

        if Context.__initialized:
            Context.__selenium_web_browser.quit()
            Context.__initialized = False

    @staticmethod
    def get_hostname() -> str:
        """Get hostname"""

        if not Context.__initialized:
            Context.init()

        return Context.__hostname

    @staticmethod
    def get_app_version() -> str:
        """Get application's version"""

        if not Context.__initialized:
            Context.init()

        return Context.__app_version

    @staticmethod
    def get_lang_code() -> str:
        """Get lang code"""

        if not Context.__initialized:
            Context.init()

        return Context.__lang_code

    @staticmethod
    def get_text(text_id: str, **kwargs) -> str:
        """Get text from its id"""

        if not Context.__initialized:
            Context.init()

        return Context.__texts[text_id].format(**kwargs)

    @staticmethod
    def get_selected_category() -> Category:
        """Get selected category"""

        if not Context.__initialized:
            Context.init()

        return Context.__selected_category

    @staticmethod
    def set_selected_category(category: Category):
        """Set selected category"""

        if not Context.__initialized:
            Context.init()

        Context.__selected_category = category

    @staticmethod
    def get_selected_emulator() -> Emulator:
        """Get selected emulator"""

        if not Context.__initialized:
            Context.init()

        return Context.__selected_emulator

    @staticmethod
    def set_selected_emulator(emulator: Emulator):
        """Set selected emulator"""

        if not Context.__initialized:
            Context.init()

        Context.__selected_emulator = emulator

    @staticmethod
    def get_selected_action() -> Action:
        """Get selected action"""

        if not Context.__initialized:
            Context.init()

        return Context.__selected_action

    @staticmethod
    def set_selected_action(action: Action):
        """Set selected action"""

        if not Context.__initialized:
            Context.init()

        Context.__selected_action = action

    @staticmethod
    def get_selected_components() -> list[Component]:
        """Get selected components"""

        if not Context.__initialized:
            Context.init()

        return Context.__selected_components

    @staticmethod
    def set_selected_components(components_items: list):
        """Set selected components"""

        if not Context.__initialized:
            Context.init()

        components_labels = []
        for components_item in components_items:
            components_labels.append(
                components_item[Constants.UI_TABLE_KEY_COL_NAME]
            )

        result = []
        for component in Component:
            if Context.get_text(component.value) in components_labels:
                result.append(component)

        Context.__selected_components = result

    @staticmethod
    def get_selected_tables_rows() -> list:
        """Get selected tables rows"""

        if not Context.__initialized:
            Context.init()

        return Context.__selected_tables_rows

    @staticmethod
    def set_selected_tables_rows(tables_rows: list):
        """Set selected tables rows"""

        if not Context.__initialized:
            Context.init()

        Context.__selected_tables_rows = tables_rows

    @staticmethod
    def get_selected_playlists_rows() -> list:
        """Get selected playlists rows"""

        if not Context.__initialized:
            Context.init()

        return Context.__selected_playlists_rows

    @staticmethod
    def set_selected_playlists_rows(playlists_rows: list):
        """Set selected playlists rows"""

        if not Context.__initialized:
            Context.init()

        Context.__selected_playlists_rows = playlists_rows

    @staticmethod
    def get_selected_bdd_tables_rows() -> list:
        """Get selected BDD Tables rows"""

        if not Context.__initialized:
            Context.init()

        return Context.__selected_bdd_tables_rows

    @staticmethod
    def set_selected_bdd_tables_rows(bdd_tables_rows: list):
        """Set selected BDD Tables rows"""

        if not Context.__initialized:
            Context.init()

        Context.__selected_bdd_tables_rows = bdd_tables_rows

    @staticmethod
    def get_selected_configs_rows() -> list:
        """Get selected configs rows"""

        if not Context.__initialized:
            Context.init()

        return Context.__selected_configs_rows

    @staticmethod
    def set_selected_configs_rows(configs_rows: list):
        """Set selected configs rows"""

        if not Context.__initialized:
            Context.init()

        Context.__selected_configs_rows = configs_rows

    @staticmethod
    def get_selected_folder_path() -> str:
        """Get selected folder's path"""

        if not Context.__initialized:
            Context.init()

        return Context.__selected_folder_path

    @staticmethod
    def set_selected_folder_path(folder_path: str):
        """Set selected folder's path"""

        if not Context.__initialized:
            Context.init()

        Context.__selected_folder_path = folder_path

    @staticmethod
    def get_selected_rows_csv_path():
        """Get CSV path describing rows for selection"""

        file_name = 'rows_'
        file_name += Context.get_selected_category().value.split('_')[
            1].lower()
        if Context.get_selected_category() == Category.TABLES:
            file_name += '_'
            file_name += Context.get_selected_emulator().value.lower()
        file_name += '_'
        file_name += Context.get_selected_action().value.split('_')[1].lower()
        return Path(os.path.join(
            Constants.CACHE_PATH,
            f'{file_name}.csv'
        ))

    @staticmethod
    def get_vpinball_path() -> Path:
        """Get vpinball path"""

        if not Context.__initialized:
            Context.init()

        return Context.__vpinball_path

    @staticmethod
    def get_data_path() -> Path:
        """Get data path"""

        if not Context.__initialized:
            Context.init()

        return Context.__data_path

    @staticmethod
    def get_config_paths(
        components: list[Component],
        config_text: str
    ) -> list[Path]:
        """Get config paths"""

        if not Context.__initialized:
            Context.init()

        config_path = ''
        for config in Constants.CONFIGS:
            if Context.get_text(Constants.CONFIG_TEXT_PREFIX + config) == config_text:
                config_path = config
                break

        paths: list[Path] = []
        if Component.SYSTEM_32_BITS in components:
            component_path = '32 bits'
            paths.append(Path(os.path.join(
                Context.get_data_path(),
                Constants.CONFIGS_PATH,
                component_path,
                config_path
            )))
            paths.append(Path(os.path.join(
                Constants.BDD_PATH,
                Constants.COMMON_PATH,
                component_path,
                config_path
            )))

        if Component.SYSTEM_64_BITS in components:
            component_path = '64 bits'
            paths.append(Path(os.path.join(
                Context.get_data_path(),
                Constants.CONFIGS_PATH,
                component_path,
                config_path
            )))
            paths.append(Path(os.path.join(
                Constants.BDD_PATH,
                Constants.COMMON_PATH,
                component_path,
                config_path
            )))

        return paths

    @staticmethod
    def get_monitor() -> int:
        """Get monitor"""

        if not Context.__initialized:
            Context.init()

        return Context.__monitor

    @staticmethod
    def get_setup_file_path() -> Path:
        """Get setup file path"""

        if not Context.__initialized:
            Context.init()

        return Path(os.path.join(
            Constants.SETUP_PATH,
            f'{Context.get_hostname()}.cfg'
        ))

    @staticmethod
    def get_csv_path() -> Path:
        """Get CSV path"""

        if not Context.__initialized:
            Context.init()

        match(Context.get_selected_category()):
            case Category.TABLES:
                return Path(os.path.join(
                    Context.get_data_path(),
                    Constants.CONFIGS_PATH,
                    Constants.PINCAB_MANAGER_PATH,
                    Constants.BDD_PATH,
                    Context.get_selected_emulator().value,
                    'tables.csv'
                ))

            case Category.PLAYLISTS:
                return Path(os.path.join(
                    Context.get_data_path(),
                    Constants.CONFIGS_PATH,
                    Constants.PINCAB_MANAGER_PATH,
                    Constants.BDD_PATH,
                    Constants.COMMON_PATH,
                    'playlists.csv'
                ))

        return None

    @staticmethod
    def get_pinup_bdd_path() -> Path:
        """Get PinUp BDD path"""

        if not Context.__initialized:
            Context.init()

        return Path(os.path.join(
            Context.get_vpinball_path(),
            'PinUPSystem',
            'PUPDatabase.db'
        ))

    @staticmethod
    def get_pinup_media_path() -> Path:
        """Get PinUp media path"""

        if not Context.__initialized:
            Context.init()

        match(Context.get_selected_category()):
            case Category.TABLES:
                return Path(os.path.join(
                    Context.get_vpinball_path(),
                    'PinUPSystem',
                    'POPMedia',
                    Context.get_selected_emulator().value
                ))

            case Category.PLAYLISTS:
                return Path(os.path.join(
                    Context.get_vpinball_path(),
                    'PinUPSystem',
                    'POPMedia',
                    'Default'
                ))

        return None

    @staticmethod
    def get_emulator_path() -> Path:
        """Get emulator path"""

        if not Context.__initialized:
            Context.init()

        match(Context.get_selected_emulator()):
            case Emulator.VISUAL_PINBALL_X:
                return Path(os.path.join(
                    Context.get_vpinball_path(),
                    'VisualPinball'
                ))

            case Emulator.PINBALL_FX:
                return Path(os.path.join(
                    Context.get_vpinball_path(),
                    'Steam',
                    'steamapps',
                    Constants.COMMON_PATH,
                    'Pinball FX'
                ))

            case Emulator.PINBALL_FX2:
                return Path(os.path.join(
                    Context.get_vpinball_path(),
                    'Steam',
                    'steamapps',
                    Constants.COMMON_PATH,
                    'Pinball FX2'
                ))

            case Emulator.PINBALL_M:
                return Path(os.path.join(
                    Context.get_vpinball_path(),
                    'Steam',
                    'steamapps',
                    Constants.COMMON_PATH,
                    'Pinball M'
                ))

            case Emulator.FUTURE_PINBALL:
                return Path(os.path.join(
                    Context.get_vpinball_path(),
                    'FuturePinball'
                ))

        return None

    @staticmethod
    def is_simulated() -> bool:
        """Specify if app is simulated"""

        if not Context.__initialized:
            Context.init()

        return Context.__simulated

    @staticmethod
    def is_auto_refresh() -> bool:
        """Specify if app is auto refresh"""

        if not Context.__initialized:
            Context.init()

        return Context.__auto_refresh

    @staticmethod
    def list_available_emulators() -> list:
        """List available emulators"""

        if not Context.__initialized:
            Context.init()

        return Context.__available_emulators

    @staticmethod
    def list_available_media() -> list:
        """List available media"""

        if not Context.__initialized:
            Context.init()

        return Context.__available_media

    @staticmethod
    def get_screen_number_by_media() -> dict:
        """Get screen number by media"""

        if not Context.__initialized:
            Context.init()

        return Context.__screen_number_by_media

    @staticmethod
    def update_context_from_setup():
        """Update context from setup"""

        if not Context.__initialized:
            Context.init()

        # If setup file exists, retrieve context from it
        if Context.get_setup_file_path().exists():
            setup = configparser.ConfigParser()
            with open(Context.get_setup_file_path(), encoding='utf-8') as file:
                setup.read_file(file)

            setup_items = {
                key: value for key, value in setup.items('DEFAULT')
            }
            if Constants.SETUP_LANG_CODE in setup_items:
                Context.__lang_code = setup_items[
                    Constants.SETUP_LANG_CODE
                ]

            if Constants.SETUP_MONITOR in setup_items:
                Context.__monitor = int(setup_items[
                    Constants.SETUP_MONITOR
                ])

            if Constants.SETUP_VPINBALL_PATH in setup_items:
                Context.__vpinball_path = Path(setup_items[
                    Constants.SETUP_VPINBALL_PATH
                ])

            if Constants.SETUP_DATA_PATH in setup_items:
                Context.__data_path = Path(setup_items[
                    Constants.SETUP_DATA_PATH
                ])

            if Constants.SETUP_SIMULATED in setup_items:
                Context.__simulated = setup_items[
                    Constants.SETUP_SIMULATED
                ] == 'True'

            if Constants.SETUP_AUTO_REFRESH in setup_items:
                Context.__auto_refresh = setup_items[
                    Constants.SETUP_AUTO_REFRESH
                ] == 'True'

            if Constants.SETUP_AVAILABLE_EMULATORS in setup_items:
                Context.__available_emulators = []
                for emulator in Emulator:
                    if emulator.value in setup_items[
                        Constants.SETUP_AVAILABLE_EMULATORS
                    ]:
                        Context.__available_emulators.append(emulator.value)

            if Constants.SETUP_AVAILABLE_MEDIA in setup_items:
                Context.__available_media = []
                for media in Media:
                    if media.value in setup_items[
                        Constants.SETUP_AVAILABLE_MEDIA
                    ]:
                        Context.__available_media.append(media.value)

            if Constants.SETUP_SCREEN_NUMBER_BY_MEDIA in setup_items:
                Context.__screen_number_by_media = json.loads(
                    setup_items[
                        Constants.SETUP_SCREEN_NUMBER_BY_MEDIA
                    ].replace('\'', '\"')
                )

        # Retrieve texts properties from lang's code
        texts_properties = configparser.ConfigParser()
        lang_path = os.path.join(
            Constants.RESOURCES_PATH,
            'lang',
            f'messages_{Context.__lang_code}.properties'
        )
        with open(lang_path, encoding='utf-8') as file:
            texts_properties.read_file(file)
        Context.__texts = {
            key: value for key, value in texts_properties.items('DEFAULT')
        }

    @staticmethod
    def get_selenium_web_browser() -> dict:
        """Get selenium web browser"""

        if not Context.__initialized:
            Context.init()

        return Context.__selenium_web_browser
