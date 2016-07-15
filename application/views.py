from application import app
from application import cache
import application.utils as utils
from flask import render_template, request
from operator import itemgetter


@app.route('/', methods=["GET"])
@cache.cached(timeout=300)
def index():
    title = 'Home'
    return render_template(
        'index.html',
        title=title
    )


@app.route('/petitions', methods=["GET"])
@cache.cached(timeout=300)
def petitions():
    title = 'Petitions'
    args = request.args.items()
    page = request.args.get('page')
    petitions = utils.get_petitions(args)
    return render_template(
        'petitions.html',
        title=title,
        data=petitions,
        page=page,
        args=args
    )


@app.route('/petitions/<id>', methods=["GET"])
@cache.cached(timeout=300)
def petition(id):
    petition = utils.get_petition(id)

    title = petition['data']['attributes']['action']

    countries = petition['data']['attributes']['signatures_by_country']
    sorted_countries = sorted(countries, key=itemgetter('signature_count'), reverse=True)

    constituencies = petition['data']['attributes']['signatures_by_constituency']
    sorted_constituencies = sorted(constituencies, key=itemgetter('signature_count'), reverse=True)

    # for constituency in sorted_constituencies[:10]:
    #     mp = utils.get_mp(constituency['name'])
    #     constituency['party'] = mp['party']
    #     constituency['url'] = mp['url']
    #     if 'image' in mp:
    #         constituency['mp_image'] = mp['image']

    extents = utils.constituency_collection(sorted_constituencies)

    events = utils.petition_events(petition)
    deadline = utils.petition_deadline(petition)

    return render_template(
        'petition.html',
        title=title,
        data=petition,
        countries=sorted_countries,
        constituencies=sorted_constituencies,
        extents=extents,
        events=events,
        deadline=deadline
    )


@app.route('/petitions/<id>/map', methods=["GET"])
@cache.cached(timeout=300)
def map(id):
    petition = utils.get_petition(id)

    title = petition['data']['attributes']['action']

    constituencies = petition['data']['attributes']['signatures_by_constituency']
    sorted_constituencies = sorted(constituencies, key=itemgetter('signature_count'), reverse=True)

    # for constituency in sorted_constituencies[:10]:
    #     mp = utils.get_mp(constituency['name'])
    #     constituency['party'] = mp['party']
    #     constituency['url'] = mp['url']

    extents = utils.constituency_collection(sorted_constituencies)

    return render_template(
        'map.html',
        title=title,
        extents=extents
    )


@app.route('/petitions/<id>/history', methods=["GET"])
@cache.cached(timeout=300)
def history(id):
    petition = utils.get_petition(id)

    title = petition['data']['attributes']['action']
    events = utils.petition_events(petition)
    deadline = utils.petition_deadline(petition)

    return render_template(
        'history.html',
        title=title,
        data=petition,
        events=events,
        deadline=deadline
    )


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error=error), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error=error), 500
