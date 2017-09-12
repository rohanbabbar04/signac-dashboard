# Copyright (c) 2017 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.
from signac_dashboard.module import Module
from signac_dashboard.util import ellipsis_string
from flask import render_template, url_for, redirect, request
from flask_assets import Bundle
from jinja2 import escape
from collections import OrderedDict

class Notes(Module):

    def __init__(self, max_chars=None, **kwargs):
        super().__init__(name='Notes',
                         context='JobContext',
                         template='cards/notes.html',
                         **kwargs)
        self.max_chars = max_chars

    def get_cards(self, job):
        note_text = job.document.get('notes', '')
        notes_action = url_for('update_notes')
        return [{'name': self.name, 'content': render_template(
            self.template, notes_action=notes_action, note_text=note_text,
            jobid=str(job) )}]

    def register_routes(self, dashboard):
        @dashboard.app.route('/notes/update', methods=['POST'])
        def update_notes():
            note_text = request.form.get('note_text')
            jobid = request.form.get('jobid')
            job = dashboard.project.open_job(id=jobid)
            job.document['notes'] = note_text
            return "Saved." #redirect(request.form.get('redirect', url_for('home')))

