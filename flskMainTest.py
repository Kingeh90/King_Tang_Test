# Import the Flask web framework
import flask, urllib, json


app = flask.Flask(__name__)
# Turn on debugging messages
app.config["DEBUG"] = True

# Initialise the dictionary
people_state = {'act': 'allen',
                'nsw': 'sudipta, nikhil',
                'qld': 'brett',
				'tas': ''}

# Create an API called task3 that will take state as a parameter
# This will return the name of people who live in that state
@app.route('/task3/<state>')
def task3(state):
	# Convert the input to lowercase for comparison
	state = state.lower()
	
	# If state exists
	if state in people_state:
		# If state is not empty
		if people_state[state] != "":
			# Return list of people who live in that state
			return people_state[state]
		else:
			return "No people found in " + state
	# Else if state does not exist
	else:
		return "The state " + state + " could not be found. Please enter a valid state."

# Create an API that will take a person's name as a parameter
# This will return the state corresponding to the name that is entered if it is found
@app.route('/GetState/<name>')
def GetState(name):
	# Set flag to False to indicate a match has not been found
	notFound = True
	# Convert the input to lowercase for comparison
	name = name.lower()
	# For each person in people_state keys
	for person in people_state.keys():
		# If the value is a list of names, split on "," and trim whitespace
		for item in people_state[person].split(","):
			# If found a match, set flag to False
			if item.strip() == name:
				notFound = False
				return person
	
	# If no person was found, print error
	if notFound:
		return name + " was not found"

# Create an API that will use the Google Places API to show the 5 best restaurants around an Australian postcode
# For rankings, assign a weighting to each of the "popularity" scores
# Check reviews and weight reviews based on how recent they were along with the star rating. More recent means higher bonus weighting.
# Take star ranking and multiply by 20 to get % score
# Take sum of popularity/business per hour and average it per hour, then rank by average "busy-ness" per hour. Ranking provides points towards overall score
# Take average score of above to produce overall score
# Take the top 5 results after ranking
# Was not able to get this response working, need to work out how to convert the response into a string or other format to use the output
@app.route('/food/<city>')
def food(city):
	key = 'AIzaSyCTGkw3sLgpfS2oOIPmgC4x6Hu8xmwyJq8'
	# Location to base the search on
	location = city
	# Search radius
	radius = 1000
	# Type of place to search for
	type = "restaurant"
	url = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json'
		'?location=%s'
		'&radius=%s'
		'&type=%s'
		'&key=%s') % (location, radius, type, key)
	response = urllib.request.urlopen(url)
	#return response.read()
	jsonRaw = response.read()
	jsonData = json.dumps(jsonRaw)
	return jsonData

	# This displays the query written for the SQL question
@app.route('/SQLQuery')
def SQLQuery():
	return ('SELECT ru.name, ra.event<br />'
	'FROM races ra<br />'
	'JOIN runners ru ON ra.winner_id=ru.id<br />'
	'ORDER BY ru.name')



app.run()