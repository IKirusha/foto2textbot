from aiogram import types, Dispatcher, Bot, executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import cv2
import pytesseract

import os, time, shutil
import sqlite3

from datetime import datetime

myid = 913070769