from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask (__name__)