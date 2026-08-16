# this file using for import flask library and variables that going to use around in programm 

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import re # Regular Expression for check users data has correct expression

app = Flask (__name__)
