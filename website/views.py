from flask import Blueprint, render_template, request, flash
import requests

# create a view object
views = Blueprint("views", __name__)

# /home endpoint
@views.route("/")
def home():
    return render_template("base.html")

# /maps endpoint
@views.route("/maps")
def maps():

    info = requests.get('https://api.mozambiquehe.re/maprotation?',
                        params=[('auth', '9139cb7e0dc0f2243066a047510d9137')])

    print(info)
    info = info.json()
    
    return render_template("maps.html",
             current_map=info['current']['map'],
             remain_time=info['current']['remainingMins'],
             map_image=info['current']['asset'])

# /to-pred endpoint that accepts get and post requests
@views.route("/to-pred", methods=['GET', 'POST'])
def to_pred():
    gathered = False

    # for post requests
    if request.method == 'POST':

        # grabs username and platform from form input
        player_name = request.form.get('playername')
        player_platform = request.form.get('playerplatform')

        # parameters for API get request
        params = [('auth', '9139cb7e0dc0f2243066a047510d9137'), ('player', player_name), ('platform', player_platform)]
        
        # get request for player info
        info = requests.get('https://api.mozambiquehe.re/bridge?',
                        params=params)

        # get request for baseline predator rp
        pred_info = requests.get('https://api.mozambiquehe.re/predator?',
                        params=[('auth', '9139cb7e0dc0f2243066a047510d9137')])

        # validates both get requests' status codes
        if info.status_code == requests.codes.ok and pred_info.status_code == requests.codes.ok:
            
            # converts content of the get requests into json
            pred_info = pred_info.json()
            print(info.text)
            info = info.json()
            

            # extra validation for 202 status code but player not found
            if 'Error' in info:
                flash(f'{info["Error"].lower()}', category='error')
                return render_template("to_pred.html", gathered=gathered)

            # flashes a successful method and sets gathered info to True
            gathered = True
            flash('Search successful!', category='success')

            # shows to-pred endpoint with needed data
            return render_template("to_pred.html", 
            rank=info['global']['rank'], 
            pred_info=pred_info['RP'][player_platform], 
            gathered=gathered,
            player=player_name)

        else:
            # convert get request content into json
            info = info.json()

            # flash error message and render to-pred endpoint
            flash(f'{info["Error"].lower()}', category='error')
            return render_template("to_pred.html",
            gathered=gathered)

    else:
        # render to-pred endpoint
        return render_template("to_pred.html")

@views.route("/services")
def services():
    return render_template("services.html")

@views.route("/crafter")
def crafter():
    info = requests.get('https://api.mozambiquehe.re/crafting?',
                        params=[('auth', '9139cb7e0dc0f2243066a047510d9137')])

    #print(info.text)
    info = info.json()
    #print(info)
    daily_items = []
    weekly_items = []
    permanent_items = []

    for item in info:
        if item['bundleType'] == 'daily':
            content = item['bundleContent']
            for cont in content:
                item_name, item_asset, item_price = cont['itemType']['name'], cont['itemType']['asset'], cont['cost']
                group = (item_name, item_asset, item_price)
                if group in daily_items:
                    continue
                else:
                    daily_items.append(group)
        elif item['bundleType'] == 'weekly':
            content = item['bundleContent']
            for cont in content:
                item_name, item_asset, item_price = cont['itemType']['name'], cont['itemType']['asset'], cont['cost']
                group = (item_name, item_asset, item_price)
                if group in weekly_items:
                    continue
                else:
                    weekly_items.append(group)
        else:
            content = item['bundleContent']
            for cont in content:
                item_name, item_asset, item_price = cont['itemType']['name'], cont['itemType']['asset'], cont['cost']
                group = (item_name, item_asset, item_price)
                if group in permanent_items:
                    continue
                else:
                    permanent_items.append(group)

    return render_template("crafter.html", items=[daily_items, weekly_items, permanent_items])


@views.route("/player", methods=['GET', 'POST'])
def player():
    gathered = False

    # for post requests
    if request.method == 'POST':

        # grabs username and platform from form input
        player_name = request.form.get('playername')
        player_platform = request.form.get('playerplatform')

        # parameters for API get request
        params = [('auth', '9139cb7e0dc0f2243066a047510d9137'), ('player', player_name), ('platform', player_platform)]
        
        # get request for player info
        info = requests.get('https://api.mozambiquehe.re/bridge?',
                        params=params)

        # get request for baseline predator rp
        # pred_info = requests.get('https://api.mozambiquehe.re/predator?',
        #                 params=[('auth', '9139cb7e0dc0f2243066a047510d9137')])

        # validates both get requests' status codes
        if info.status_code == requests.codes.ok:
            
            # converts content of the get requests into json
            # pred_info = pred_info.json()
            print(info.text)
            info = info.json()
            

            # extra validation for 202 status code but player not found
            if 'Error' in info:
                flash(f'{info["Error"].lower()}', category='error')
                return render_template("player.html", gathered=gathered)

            # flashes a successful method and sets gathered info to True
            gathered = True
            flash('Search successful!', category='success')

            # shows to-pred endpoint with needed data
            return render_template("player.html",   
            gathered=gathered,
            player_info=info)

        else:
            # convert get request content into json
            info = info.json()

            # flash error message and render to-pred endpoint
            flash(f'{info["Error"].lower()}', category='error')
            return render_template("player.html",
            gathered=gathered)

    else:
        # render to-pred endpoint
        return render_template("player.html",
        gathered=gathered)