from mash_petitions import app
from mash_petitions import cache
from mash_petitions.models import Petitions, TheyWorkForYou, MapIt
from flask import render_template, request
from operator import itemgetter

petitions_url = app.config['PETITIONS_API_URL']
petitions_api = Petitions(petitions_url)

twfy_url = app.config['TWFY_API_URL']
twfy_key = app.config['TWFY_API_KEY']
twfy_api = TheyWorkForYou(twfy_url, twfy_key)

mapit_url = app.config['MAPIT_API_URL']
mapit_api = MapIt(mapit_url)


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
    data = petitions_api.get_petitions(args)
    return render_template(
        'petitions.html',
        title=title,
        data=data,
        page=page,
        args=args
    )


@app.route('/petitions/<id>', methods=["GET"])
@cache.cached(timeout=300)
def petition(id):
    petition = petitions_api.get_petition(id)

    title = petition['data']['attributes']['action']

    countries = petition['data']['attributes']['signatures_by_country']
    sorted_countries = sorted(countries, key=itemgetter('signature_count'), reverse=True)

    constituencies = petition['data']['attributes']['signatures_by_constituency']
    sorted_constituencies = sorted(constituencies, key=itemgetter('signature_count'), reverse=True)

    # for constituency in sorted_constituencies[:10]:
    #     mp = twfy_api.get_mp(constituency['name'])
    #     constituency['party'] = mp['party']
    #     constituency['url'] = mp['url']
    #     if 'image' in mp:
    #         constituency['mp_image'] = mp['image']

    extents = mapit_api.constituency_collection(sorted_constituencies)

    events = petitions_api.petition_events(petition)
    deadline = petitions_api.petition_deadline(petition)

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
    petition = petitions_api.get_petition(id)

    title = petition['data']['attributes']['action']

    constituencies = petition['data']['attributes']['signatures_by_constituency']
    sorted_constituencies = sorted(constituencies, key=itemgetter('signature_count'), reverse=True)

    # for constituency in sorted_constituencies[:10]:
    #     mp = twfy_api.get_mp(constituency['name'])
    #     constituency['party'] = mp['party']
    #     constituency['url'] = mp['url']

    extents = mapit_api.constituency_collection(sorted_constituencies)

    return render_template(
        'map.html',
        title=title,
        extents=extents
    )


@app.route('/petitions/<id>/history', methods=["GET"])
@cache.cached(timeout=300)
def history(id):
    petition = petitions_api.get_petition(id)

    title = petition['data']['attributes']['action']
    events = petitions_api.petition_events(petition)
    deadline = petitions_api.petition_deadline(petition)

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
