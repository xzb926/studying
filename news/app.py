#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask
from flask import render_template
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():

   title_list = {
            'title1':'Hello,Shiyanlou!',
            'title2':'Hello,World!'
            }
   return render_template('index.html', title_list=title_list)

@app.route('/files/<filename>')
def file(filename):
    
