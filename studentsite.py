import flask
import colander
from deform import Form
from werkzeug.datastructures import OrderedMultiDict
import peppercorn

#Deriving from flask.Request
class theRequest(flask.Request):
	parameter_storage_class = OrderedMultiDict #This is the only parameter that is going to be different

#Building a very simple "dummy" schema using Colander
class simpleRecord(colander.MappingSchema):
	description = colander.SchemaNode(colander.String(), validator = colander.Length(min = 1,max=50))
	amount = colander.SchemaNode(colander.Int())

class dataList(colander.SequenceSchema):
	item = simpleRecord()

#This may seem redundant but is actually required by Deform
class topList(colander.MappingSchema):
	items = dataList()

#Creating the flask "application"
app = flask.Flask(__name__)

#Configuring the application
app.request_class = theRequest #This is what actually effects the change of the form object's type


#A standard entry point to be served accepting both GET and POST calls.
@app.route("/form_data", methods=["POST","GET"])
def index():
	if flask.request.method == "POST":
		#Please note the "multi=True"
		controlData = peppercorn.parse(flask.request.form.items(multi=True))
		#Now just sort the data just to do some kind of processing
		controlData['items'] = sorted(controlData['items'],key=lambda x:int(x['amount']))
		#Now, create the form to be returned to the user according to the schema defined before and populating it with the data that were posted by the user and processed by the application so far.
		someForm = Form(topList(),buttons=('submit',)).render(controlData)
		aMess="Processed Data" #Just a string to define a message
	else:
		#Just return an empty form
		someForm = Form(topList(),buttons=('submit',)).render()
		aMess = "You can use this form to sort a list of simple records"
	return flask.render_template("index.html", theForm = someForm, theMessage = aMess)

@app.route("/", methods=["GET"])
def home_page():
    return flask.render_template('home.html')

if __name__=="__main__":
	app.debug = True;
app.run()
