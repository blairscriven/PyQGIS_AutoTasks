import os, logging, time, glob, pandas as pd
from qgis.core import QgsVectorLayer, QgsField, QgsExpression, QgsExpressionContextUtils, QgsExpressionContext
from PyQt5.QtCore import QVariant

import processing
from processing.core.Processing import Processing

def set_logger(
		pathlogfile,  # filepath where logger will be created
		):
	# Set up a basic Logger
	logging.basicConfig(filename=pathlogfile, filemode='w', format='%(asctime)s-%(levelname)s-%(message)s',
						level=logging.INFO)
	logger = logging.getLogger()
	logger.addHandler(logging.StreamHandler())
	logger.info('BEGIN RUN')

	return logger

def change_filenames():
	# Change names of files (in this case, delete old date and add new date to filename)
	for file_name in glob.glob("*.gpkg"):
		new_filename = file_name[:-13] + "03262050.gpkg"
		os.rename(file_name, new_filename)

def del_nulls(file, logger):
	Vector_data = QgsVectorLayer(file, "", "ogr")
	logger.info('File: %s', file)
	int_feilds = Vector_data.fields() # Identify attribute fields
	field_names = int_feilds.names() # list of field names

	 # Example of a list Comprehension; find each feature (row in table) and find its value for each column; outputs a generator
	datagen = ([f[col] for col in field_names] for f in Vector_data.getFeatures())

	# Following code block will convert attribute data into pandas dataframe, then the Null fields will be identified
	df = pd.DataFrame.from_records(data=datagen, columns=field_names)
	#df = df.replace('NULL', np.nan, regex=True)
	df.to_csv("temp.csv")
	df1 = pd.read_csv("temp.csv", na_values= "NULL")
	Null_list = df1.columns[df1.isna().all()].tolist()
	os.remove('temp.csv')
	del_index = []
	
	for field in Null_list:
		del_index.append(int_feilds.indexFromName(field)) # create a list of attribute feild indices

	data_provider = Vector_data.dataProvider() # access the real datasource behind your layer
	data_provider.deleteAttributes(del_index)
	Vector_data.commitChanges()

	logger.info('Deleted the NULL-fields(%s) from the %s file', str(Null_list), file)

def delete_fields(file, fields, logger):
	Vector_data = QgsVectorLayer(file, "", "ogr")
	tmp_feilds = Vector_data.fields() # Identify attribute fields
	field_index = []

	for field in fields:
		field_index.append(tmp_feilds.indexFromName(field)) # create a list of attribute feild indices

	data_provider = Vector_data.dataProvider() # access the real datasource behind your layer
	data_provider.deleteAttributes(field_index)
	Vector_data.commitChanges()

	logger.info('Deleted the following fields: ' + str(fields) + ' from ' + file)

def add_fields(file, logger):
	Vector_data = QgsVectorLayer(file, "", "ogr")

	# add new feild
	data_provider = Vector_data.dataProvider() # access the real datasource behind your layer
	data_provider.addAttributes([QgsField('Test',  QVariant.Int)])
	Vector_data.commitChanges()
	logger.info('Added new fields to ' + file)

def update_field(file, update_field_name, field_exp, logger):
	Vector_data = QgsVectorLayer(file, "", "ogr")
	Field_Calculation = QgsExpression(field_exp)
	
	# Check to make sure the field calculation is valid, else skip the update run
	if Field_Calculation.isValid() is True:
		pass
	else:
		logger.warning('Field calculation expression is NOT valid for ' + file)
		return
	
	# Provide context - make sure your expression can be applied to layer
	context = QgsExpressionContext()
	context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(Vector_data))
	
	# update field
	for feature in Vector_data.getFeatures():
		Vector_data.startEditing()
		context.setFeature(feature)
		feature[update_field_name] = Field_Calculation.evaluate(context)
		Vector_data.updateFeature(feature)
	Vector_data.commitChanges()
	logger.info('Updated field in ' + file)

def QGIS_geoprocessing(file, logger): # as a demo, only runs the 'fix geometry' tool
	Vector_data = QgsVectorLayer(file, "", "ogr")
	str_ind = file.find('.')
	out_name = file[ : str_ind] + "_fixgeom" + file[str_ind : ] # add '_fixgeom' before the filename extention
	logger.info('filename: %s', out_name)
	fix_geom = processing.run("native:fixgeometries", {'INPUT':Vector_data ,
                                                    	'OUTPUT':out_name}) # use 'memory:' for a temporary output

def run(
		INPUT_PATH = 'inputfolder/',
		delete_fields_list = ['old_field1', 'old_field2'],
		update_field_name = "Test",
		update_field_expression = '"field1" + "field2"' # CASE example: 'CASE WHEN "field1" = \'No\' THEN 1 else 5 END'
	):
	# Nicely formatted time string
	def hms_string(sec_elapsed):
		h = int(sec_elapsed / (60 * 60))
		m = int((sec_elapsed % (60 * 60)) / 60)
		s = sec_elapsed % 60
		return "{}:{:>02}:{:>05.2f}".format(h, m, s)
	start_time = time.time()

	# Set paths and create logger
	os.chdir(INPUT_PATH)
	pathLogFile = os.path.join('Processing.log')
	logger = set_logger(pathLogFile)

	# Change name of files - go to class to define the new naming convention
	#change_filenames()

	# Create a list of the vector or raster files
	FILES_LIST = glob.glob("*.gpkg") # *.gpkg *.shp *.tiff
	Processing.initialize()

	for file in FILES_LIST:
		#delete_fields(file, delete_fields_list, logger)
		del_nulls(file, logger)
		#add_fields(file, logger) # go to class to define new field names and QVarient types (e.g. Int)
		#update_field(file, update_field_name, update_field_expression, logger)
		#QGIS_geoprocessing(file, logger) # go to class to define the geoprocessing procedure you want

	# End the timer
	time_took = time.time() - start_time
	time_took_pretty = hms_string(time_took)
	logger.info('Total Runtime: %s', time_took_pretty)
	logger.info('END RUN')


if __name__ == '__main__':
	run()  # run the script