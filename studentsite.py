import flask
import colander
import deform
from werkzeug.datastructures import OrderedMultiDict
import peppercorn
import js.deform

#Deriving from flask.Request
class theRequest(flask.Request):
	parameter_storage_class = OrderedMultiDict #This is the only parameter that is going to be different


class simpleRecord(colander.MappingSchema):
	description = colander.SchemaNode(colander.String(), validator = colander.Length())
	amount = colander.SchemaNode(colander.Int())
	'''styling:
text_input = deform.widget.TextInputWidget(
    css_class='yourdivnamehere')
first_name = colander.SchemaNode(colander.String(),
            widget = text_input)

'''
css_widget = deform.widget.TextInputWidget(css_class="deform-widget-with-style")

class dataList(colander.SequenceSchema):
	item = simpleRecord()

class topList(colander.MappingSchema):
	items = dataList()
'''
class Schema(colander.Schema):
            text = colander.SchemaNode(colander.String(),
                                       validator=colander.Length(max=100),
                                       widget=css_widget,
                                       description='Enter some text')
'''

class Mapping(colander.Schema):
	#Firstname = colander.SchemaNode(colander.String(), css_class='deform-widget-with-style')
	#Lastname = colander.SchemaNode(colander.String(), css_class='deform-widget-with-style')
	#Email = colander.SchemaNode(colander.String(), css_class='deform-widget-with-style')
	Firstname = colander.SchemaNode(colander.String(), validator=colander.Length(min = 5, max=100), widget=css_widget, description='Enter some text')
	Email = colander.SchemaNode(colander.String(), validator=colander.Length(min = 5, max=100), widget=css_widget, description='Enter some text')
	Lastname = colander.SchemaNode(colander.String(), validator=colander.Length(min = 5, max=100), widget=css_widget, description='Enter some text')



	date = colander.SchemaNode(colander.Date(), widget = deform.widget.DatePartsWidget(), description = "content date")

class Schema(colander.Schema):
	Age = colander.SchemaNode(colander.Integer(), validator=colander.Length(min = 5, max=100), widget=css_widget, description='Enter some text')
	Firstname = colander.SchemaNode(colander.String(), validator=colander.Length(min = 5, max=100), widget=css_widget, description='Enter some text')
	Lastname = colander.SchemaNode(colander.String(), validator=colander.Length(min = 5, max=100), widget=css_widget, description='Enter some text')
	Email = colander.SchemaNode(colander.String(), validator=colander.Length(min = 5, max=100), widget=css_widget, description='Enter some text')

#	Number = colander.SchemaNode(colander.Integer())

	#mapping = Mapping(widget = deform.widget.MappingWidget(template="mapping_accordion", open=True))
class Schema1(colander.Schema):
	password = colander.SchemaNode(colander.String(), validator=colander.Length(min=5), widget=deform.widget.CheckedPasswordWidget(redisplay=True), description='Type your password and confirm it')
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

		print "controlData", controlData #this is it!!!!!!!!!!!!!!!!!!!!
		#Now, create the form to be returned to the user according to the schema defined before and populating it with the data that were posted by the user and processed by the application so far.
		form = deform.Form(topList(),buttons=('submit',)).render(controlData)
		aMess="Processed Data" #Just a string to define a message
		return flask.render_template("index.html", theForm = form, title = "HI")

	else:
		#Just return an empty form

		schema = Schema1()
		form = deform.Form(schema, buttons=('submit',)).render() #used to be	form = deform.Form(schema, buttons=('submit',)).render()

		return flask.render_template("index.html", theForm = form, theMessage = "HI")



@app.route("/")
def home_page():
    return flask.render_template('home.html')

@app.route("/get_skills", methods=["POST","GET"])
def skils():
	return flask.render_template("skills.html")

if __name__=="__main__":
	app.debug = True;
app.run()
