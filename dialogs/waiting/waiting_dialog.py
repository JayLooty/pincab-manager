#!/usr/bin/python3
"""Dialog to wait for a process"""

import threading
import time
import tkinter as tk
from tkinter import ttk

from libraries.constants.constants import Constants
from libraries.context.context import Context
from libraries.ui.ui_helper import UIHelper

# pylint: disable=attribute-defined-outside-init


class WaitingDialog:
    """Dialog to wait for a process"""

    def __init__(
        self,
        parent,
        process_name: str,
        process_function: any
    ):
        """Initialize dialog"""

        self.__process_name = process_name
        self.__process_function = process_function

        # Create dialog
        self.__dialog = tk.Toplevel(parent)

        try:
            self.__dialog.attributes("-toolwindow", True)
        except Exception as exc:
            print(exc)

        # Fix dialog's title
        self.__dialog.title(
            Context.get_text(
                'waiting'
            )
        )

        # Block manual closing
        self.__dialog.protocol(
            "WM_DELETE_WINDOW",
            self.__disable_close
        )

        # Fix dialog's size and position
        UIHelper.center_dialog(
            dialog=self.__dialog,
            width=320,
            height=80
        )

        # Add a label with a progress bar
        waiting_label = tk.Label(
            self.__dialog,
            text=Context.get_text(
                'waiting_for',
                process=self.__process_name)
        )
        waiting_label.pack(
            fill=tk.X,
            padx=Constants.UI_PAD_BIG,
            pady=Constants.UI_PAD_BIG
        )

        self.__transform_progress = ttk.Progressbar(
            self.__dialog,
            mode='indeterminate'
        )
        self.__transform_progress.pack(
            fill=tk.X,
            padx=Constants.UI_PAD_BIG,
            pady=Constants.UI_PAD_BIG
        )
        self.__transform_progress.start(10)

        # Run process in a Thread to avoid blocking UI
        threading.Thread(
            target=self.__run_process,
            daemon=True
        ).start()

    def __run_process(self):
        """Run process"""

        # Waiting 0.1 seconde to see the dialog if the process is quick
        time.sleep(0.1)

        # Waiting for the process
        self.__process_function()

        # Close the dialog after process
        UIHelper.close_dialog(self.__dialog)

    def __disable_close(self):
        pass
