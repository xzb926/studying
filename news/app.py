#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, abort
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)

class  File(db.Model):
    __tablename__ = 'article'
    article_id = db.Column(db.Integer, primary_key=True)
    title = db.Conlumn(db.String(80))
    created_time = db.Conlumn(db.DateTime)
    category_id = (db.Integer, db.ForeignKey('categories_id')
#    content = (db.Text)
    def __repr__(self):
        return '<File %s>' % self.name

class Category(db.Model):
    __tablename__ = 'categories'
    categories_id = (db.Integer)
    categories_name = (db.String(80))
    def __repr__(self):
        return '<Category %s>' % self.name

class Files(object):
    file_path = os.path.join(os.path.abspath(os.path.dirname(__name__)), '..', 'files')
    def __init__(self):
        self._files = self._read_all_files() 
    
    def _read_all_files(self):
        files = {}
        for filename in os.listdir(self.file_path):
            file_all_path = os.path.join(self.file_path, filename)
            with open(file_all_path, 'r') as f:
                files[filename[:-5]] = json.load(f)

        return files
            
        

    def get_list(self):
        return [item['title'] for item in self._files.values()]

    def get_content(self, filename):
        return self._files.get(filename)


files = Files()

@app.route('/')
def index():
    return render_template('index.html', title_list = files.get_list())
    
@app.route('/files/<filename>')
def file(filename):
    file_item = files.get_content(filename)
    if not file_item:
        abort(404)
    return render_template('file.html', file_item=file_item)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
