#!/usr/bin/python3
"""Windows Registry Helper"""

import os
import winreg
import subprocess
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper
from libraries.logging.logging_helper import LoggingHelper


class WinRegHelper:
    """Class to help usage of Windows Registry"""

    @staticmethod
    def __convert_value_to_reg_format(name, value, value_type):
        """Convert values for registry"""
        if value_type == winreg.REG_SZ:
            return f'"{name}"="{value}"'
        if value_type == winreg.REG_DWORD:
            return f'"{name}"=dword:{value:08x}'
        if value_type == winreg.REG_BINARY:
            value_hex = ",".join([f'{b:02x}' for b in value])
            return f'"{name}"=hex:{value_hex}'
        return f'Unknown type for {name}'

    @staticmethod
    def is_user_key_exists(
        key: str
    ):
        """Specify if user key exists"""

        try:
            winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key,
                0,
                winreg.KEY_READ
            )
            return True
        except Exception:
            return False

    @staticmethod
    def extract_user_key(
        extracted_file_path: str,
        key: str
    ):
        """Extract user key"""

        export_content = ''
        try:
            # Open the registry key
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key,
                0,
                winreg.KEY_READ
            )

            # Read all values from the key
            i = 0
            while True:
                try:
                    if len(export_content) == 0:
                        # Header for .reg
                        export_content += "Windows Registry Editor Version 5.00\n\n"

                        # Add key
                        export_content += f"[HKEY_CURRENT_USER\\{key}]\n"

                    name, value, value_type = winreg.EnumValue(registry_key, i)
                    export_content += WinRegHelper.__convert_value_to_reg_format(
                        name, value, value_type) + "\n"
                    i += 1
                except OSError:
                    break

            winreg.CloseKey(registry_key)
        except WindowsError:
            return

        if len(export_content) == 0:
            return

        if Context.is_simulated():
            LoggingHelper.log_info(
                message=Context.get_text(
                    'extract_user_key_simulation',
                    file=str(extracted_file_path)
                )
            )
            return

        LoggingHelper.log_info(
            message=Context.get_text(
                'extract_user_key_in_progress',
                file=str(extracted_file_path)
            )
        )
        os.makedirs(os.path.dirname(extracted_file_path), exist_ok=True)
        FileHelper.write_file(
            file_path=extracted_file_path,
            content=export_content
        )

    @staticmethod
    def delete_user_key(
        key: str
    ):
        """Delete user key"""

        if Context.is_simulated():
            LoggingHelper.log_info(
                message=Context.get_text(
                    'delete_user_key_simulation',
                    key=key
                )
            )
            return

        LoggingHelper.log_info(
            message=Context.get_text(
                'delete_user_key_in_progress',
                key=key
            )
        )
        try:
            winreg.DeleteKey(
                winreg.HKEY_CURRENT_USER,
                key
            )
        except Exception:
            return

    @staticmethod
    def import_user_key(
        extracted_file_path: str
    ):
        """Import user key"""

        if Context.is_simulated():
            LoggingHelper.log_info(
                message=Context.get_text(
                    'import_user_key_simulation',
                    file=str(extracted_file_path)
                )
            )
            return

        LoggingHelper.log_info(
            message=Context.get_text(
                'import_user_key_in_progress',
                file=str(extracted_file_path)
            )
        )

        try:
            subprocess.run(
                ["reg", "import", extracted_file_path],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception:
            return
