from antplanner2 import app
from antplanner2 import websoc
from flask import flash, render_template, request, jsonify
from google.appengine.api import memcache
import logging

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/websoc/search', methods=['GET'])
def websoc_search_form():
    form_html = memcache.get('search')
    if not form_html:
        form_html = websoc.get_search()
        memcache.add('search', form_html, 60 * 60 * 24)

    return render_template('websoc/search.html', form_content=form_html)

@app.route('/websoc/search', methods=['POST'])
def websoc_search():
    key = str(request.form)
    listing_html = memcache.get(key)
    if not listing_html:
        listing_html = websoc.get_listing(request.form)
        memcache.add(key, listing_html, 60 * 60 * 24)
    return render_template('websoc/listing.html', listing=listing_html)

@app.route('/test')
def qunit():
    return render_template('test.html')

# @app.route('/schedules/save', methods=['POST'])
# def save_schedule():
#     username = request.form.get('username')
#     events = request.form.get('events')
#     s = models.Schedule(key_name=username, events=events)
#     s.put()
#     return jsonify({'success': True})

# @app.route('/schedules/<key>/load')
# def load_schedule(key):
#     data = Schedule.get_by_key_name(key)
#     if data:
#         return ''.join(['{"success": "true", ', '"events": ', data.caldata, '}'])
#     else:
#         return '{"success":"false"}'
