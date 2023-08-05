"""Main script for the execution of this task"""
import sys

from .buildPayload import buildPayload


def main():
    buildPayload(*sys.argv)
