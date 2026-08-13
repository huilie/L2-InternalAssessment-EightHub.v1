from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import re
import logging
app = Flask (__name__)

log = logging.getLogger("awd")
log.disabled = True