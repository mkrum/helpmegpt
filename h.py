#! /usr/bin/env python

import sys
import fileinput
import os

from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep

import openai
import rich
from rich.console import Console
from rich import print as print_
from rich.markdown import Markdown


class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


openai.api_key = os.getenv("OPENAI_API_KEY")


def get_completion(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
    except openai.error.APIError:
        print_("\n[red]API is down[red]")
        exit()

    return response["choices"][0]["message"]["content"]


def main():
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant being run in a computer terminal.",
        }
    ]

    if len(sys.argv) > 1:
        message = sys.argv[1]
        loader = Loader("Praying to our new overlords", "", 0.1).start()
        messages.append({"role": "user", "content": message})
        out = get_completion(messages)
        loader.stop()

        console = Console()
        md = Markdown(out)
        console.print(md)
        exit()

    print_("[yellow]>>[yellow] ", end="")
    for line in fileinput.input():
        messages.append({"role": "user", "content": line})

        loader = Loader("Praying to our new overlords", "", 0.1).start()
        out = get_completion(messages)
        loader.stop()

        console = Console()
        md = Markdown(out)
        console.print(md)

        messages.append({"role": "assistant", "content": out})
        print_("\n[yellow]>>[yellow] ", end="")
