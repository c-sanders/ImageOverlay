#!/usr/bin/env python

# Description
# ===========
#
# Scale an image and then set its size so that is 1920 x 1080 in resolution.
#
#
# Running this Plugin from the command line
# =========================================
#
# I think I once read somewhere, that when a GIMP Plugin is invoked from the command line, the
# arguments need to be passed to the Plugin as strings. Attempting to do otherwise can result in
# GIMP runtime errors, such as the following;
#
#   Error: ( : 1) eval: unbound variable: DO_NOTHING
#   Error: ( : 1) Invalid type for argument 5 to python-fu-runPlugin-multiple-fromFile
#
# To invoke this Plugin from the command line, use a command which is similar to the following;
#
#   gimp --no-interface \
#        --verbose \
#        --console-messages \
#        --batch-interpreter="plug-in-script-fu-eval" \
#        --batch '( \
#                  python-fu-runPlugin-multiple-fromList \
#                  RUN-NONINTERACTIVE \
#                  "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/slides/png/Eulers_formula_animation_slides-000001.png" \
#                  "READ_LIST_FROM_STDIN",
#                  "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/frames/png/animation_1/fileList.txt" \
#                  "/home/craig/temp/Animation_images_png/" \
#                  "DO_NOTHING" \
#                  "result" \
#                  "DIAGNOSTIC_DATA_NONE" \
#                 )' \
#        --batch '(gimp-quit 0)'
# 
# Alternatively, here is the same command presented all on one line so as to assist with a cut and
# paste of the command onto a command line.
# 
# gimp --no-interface --verbose --console-messages --batch-interpreter="plug-in-script-fu-eval" --batch '(python-fu-runPlugin-multiple-fromList RUN-NONINTERACTIVE "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/slides/png/Eulers_formula_animation_slides-000001.png" "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/frames/png/animation_1/fileList.txt" "/home/craig/temp/Animation_images_png/" "0" "result" "0")' --batch "(gimp-quit 0)"
#
#
# Analysis of Plugin arguments
# ============================
#
# The arguments which were presented to the Plugin in the above example, are as follows;
#
# Argument 1 = RUN-NONINTERACTIVE
# Argument 2 = "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/slides/png/Eulers_formula_animation_slides-000001.png"
# Argument 3 = "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/frames/png/animation_1/fileList.txt"
# Argument 4 = "/home/craig/temp/Animation_images_png/"
# Argument 5 = "DO_NOTHING
# Argument 6 = "result"
# Argument 7 = "DIAGNOSTIC_DATA_NONE"
#
# /home/foo/fileList.txt should be a file that contains a list of those files (one per line) which
# should be operated on by the Plugin.
#
#
# Plugin locations
# ================
#
# Exmples of locations within which Gimp Plugins can reside;
#
#   - /home/foo/.gimp-2.x/plug-ins
#   - /usr/lib/gimp/2.0/plug-ins


from   os     import path
import time
from   sys    import stdin

SPHINX_ACTIVE = False

if (SPHINX_ACTIVE == False) :

	from   gimpfu import register, main, pdb, gimp, PF_IMAGE, PF_DRAWABLE, PF_INT, PF_STRING, PF_FILE, PF_BOOL, INTERPOLATION_NONE, INTERPOLATION_LINEAR, INTERPOLATION_CUBIC, INTERPOLATION_LANCZOS, PF_RADIO
	from   diagnosticDataDialog import DiagnosticDataDialog, DIAGNOSTIC_DATA_STDOUT, DIAGNOSTIC_DATA_DIALOG, DIAGNOSTIC_DATA_BOTH, DIAGNOSTIC_DATA_NONE

else :

	PF_FILE        = 1004
	PF_STRING      = 0
	PF_RADIO       = 0

	DIAGNOSTIC_DATA_STDOUT = 0
	DIAGNOSTIC_DATA_DIALOG = 0
	DIAGNOSTIC_DATA_BOTH   = 0
	DIAGNOSTIC_DATA_NONE   = 0

	def register(

	  proc_name,
	  blurb,
	  help,
	  author,
	  copyright,
	  date,
	  label,
	  imagetypes,
	  params,
	  results,
	  function,
	  menu=None,
	  domain=None,
	  on_query=None,
	  on_run=None
	) :

		return(0)

READ_LIST_FROM_STDIN       = "0"
READ_LIST_FROM_FIELD       = "1"

DO_NOTHING                 = "0"
PREPEND_FILENAME           = "1"
APPEND_FILENAME            = "2"
PREPEND_FILENAME_EXTENSION = "3"
APPEND_FILENAME_EXTENSION  = "4"


def runPlugin_single(

  filename_background,
  filename_foreground,
  filename_result,
  display_stdout_or_dialog
) :

	"""
	This function gets registered with GIMP as it implements the following Plugin : Overlay Image
	
	This function will overlay a single foreground image onto a single background image. Once this is done, the function will save the resulting image into a file.


	Parameters:

	filename_background (String) :
	The filename of the background file.

	filename_foreground (String) :
	The filename of the forgreound file.

	filename_result (String) :
	The filename of the file into which the result will be saved.

	display_stdout_or_dialog (Boolean) :
	Whether diagnostic data should be displayed to stdout or in a dialog window.


	Returns:

	NA


	Invoked by : Checked

	GIMP


	Invokes:

	OverlayImageAgent Ctor
	OverlayImageAgent.runSingle
	"""


	nameProcedure = "runPlugin_single"


	print("%s : Enter" % (nameProcedure))

	overlayImageAgent = OverlayImageAgent(

	                      filename_background,
	                      filename_result,
	                      display_stdout_or_dialog
	                    )

	overlayImageAgent.runSingle()

	print("%s : Exit" % (nameProcedure))


def runPlugin_multiple_fromList(

  filename_background,
  list_source,
  list_filenames_foreground,
  dir_output,
  filename_manipulation_method,
  filename_suffix,
  display_stdout_or_dialog
) :

	"""
	This function gets registered with GIMP as it implements the following Plugin : Overlay Images (From List)

	This function will overlay a single foreground image onto a single background image. Once this is done, the function will save the resulting image into a file.
	This process is repeated for all of the foreground images whose filenames are specified in the list of semi-colon separated filenames.


	Parameters:

	filename_background (String) :
	The filename of the background file.

	filename_foreground_files (String) :
	A comma seperated list of the filenames of the forgreound files.

	dir_output (String) :
	The name of the directory into which the resulting files should be saved.


	Returns:

	NA


	Invoked by : Checked

	GIMP


	Invokes:

	OverlayImageAgent Ctor
	OverlayImageAgent.runMultipleFromList
	"""


	nameProcedure = "runPlugin_multiple_fromList"


	print("%s : Enter" % (nameProcedure))

	print("%s : list_source == %s" % (nameProcedure, list_source))
	print("%s : list_filenames_foreground = %s" % (nameProcedure, list_filenames_foreground))

	overlayImageAgent = OverlayImageAgent(

	                      filename_background,
	                      None,
	                      dir_output,
	                      filename_manipulation_method,
	                      filename_suffix,
	                      display_stdout_or_dialog
	                    )

	if (list_source == "READ_LIST_FROM_STDIN") :

		print("%s : list_source == \"READ_LIST_FROM_STDIN\"" % (nameProcedure))

	list_filenames_foreground = ""

	# Read the list of files from stdin

	for line in stdin :

		line = line.rstrip()

		print("%s : line = %s" % (nameProcedure, line))

		if list_filenames_foreground == "" :

			list_filenames_foreground = line

		else :

			list_filenames_foreground = list_filenames_foreground + ";" + line

	print("%s : list_filenames_foreground = %s" % (nameProcedure, list_filenames_foreground))

	overlayImageAgent.runMultipleFromList(list_filenames_foreground, ';')

	print("%s : Exit" % (nameProcedure))


def runPlugin_multiple_fromFile(

  filename_background,
  filename_foreground_files,
  dir_output,
  filename_manipulation_method,
  filename_suffix,
  display_stdout_or_dialog
) :

	"""
	This function gets registered with GIMP as it implements the following Plugin : Overlay Images (From File)


	Parameters:

	filename_background (String) :
	The filename of the background file.

	filename_foreground_files (String) :
	A comma seperated list of the filenames of the forgreound files.

	dir_output (String) :
	The name of the directory into which the resulting files should be saved.

	filename_manipulation_method (String) : 

	filename_suffix (String) :
	A string that will be used to manipulate the filename of the output file.


	Returns:

	NA


	Invoked by :

	GIMP


	Invokes :

	OverlayImageAgent Ctor
	OverlayImageAgent.runMultipleFromList
	"""


	nameProcedure = "runPlugin_multiple_fromFile"


	print("%s : Enter" % (nameProcedure))

	print("%s : Output dir = %s" % (nameProcedure, dir_output))
	print("%s : Filename manipulation method = %s" % (nameProcedure, filename_manipulation_method))
	print("%s : Filename suffix = %s" % (nameProcedure, filename_suffix))

	overlayImageAgent = OverlayImageAgent(

	                      filename_background,
	                      None,
	                      dir_output,
	                      filename_manipulation_method,
	                      filename_suffix,
	                      display_stdout_or_dialog
	                    )

	overlayImageAgent.runMultipleFromFile(filename_foreground_files)

	print("%s : Exit" % (nameProcedure))


class OverlayImageAgent :

	"""
	The OverlayImageAgent class is used to overlay one image on top of another.
	"""

	displayDiagnosticDataOnStdout = False

	filenames_foreground          = None

	filename_background           = None
	filename_foreground           = None
	filename_result               = None

	image_background              = None
	image_foreground              = None

	image_background_original     = None
	image_background_new          = None

	drawable_background           = None
	drawable_foreground           = None

	drawable_background_original  = None

	dir_output                    = ""
	filename_manipulation_method  = None
	filename_suffix               = ""

	use_gimp_edit_paste_as_new    = True

	sleep_timer                   = 0
	counter                       = 1


	def __init__(

	  self,
	  filename_background,
	  filename_result,
	  dir_output,
	  filename_manipulation_method,
	  filename_suffix,
	  display_stdout_or_dialog
	) :

		"""
		Constructor for class OverlayImageAgent.


		Parameters:

		filename_background (String) :
		The filename of the background file.

		filename_result (String) :
		The filename of the file into which the result will be saved.

		dir_output (String) :
		The name of the directory into which the resulting files should be saved.

		filename_manipulation_method (String) :
		The method which will be used to manipulate the filename of the foreground image, in order to construct the resulting filename.

		filename_suffix (String) :
		The suffix which will be used to construct the resulting filename.

		display_stdout_or_dialog (String) : 
		Whether diagnostic data should be displayed to stdout or in a Dialog panel.


		Returns:

		NA


		Invoked by :

		runPlugin_single
		runPlugin_multiple_fromList
		runPlugin_multiple_fromFile


		Invokes :

		NA
		"""


		nameProcedure = "OverlayImageAgent::Ctor"


		print("%s : Enter" % (nameProcedure))

		print("%s : filename_background = %s" % (nameProcedure, filename_background))
		print("%s : filename_result     = %s" % (nameProcedure, filename_result))
		print("%s : dir_output          = %s" % (nameProcedure, dir_output))

		if (dir_output == None) :

			print("%s : dir_output == None" % (nameProcedure))

		if (dir_output == "") :

			print("%s : not dir_output" % (nameProcedure))

		if (not path.isdir(dir_output)) :

			print("%s : not path.isdir(dir_output)" % (nameProcedure))

		if (
		    (not dir_output == None) and
		    (dir_output)             and
		    (not path.isdir(dir_output))
		   ) :

			exception_message = "\n\nAn Exception has been raised by the method;\n\n  " + \
			                    nameProcedure + \
			                    "\n\nThe directory specified does not exist;\n\n" + \
			                    dir_output

			raise Exception(exception_message)

		self.filename_background           = filename_background
		self.filename_result               = filename_result
		self.dir_output                    = dir_output
		self.filename_manipulation_method  = filename_manipulation_method
		self.filename_suffix               = filename_suffix
		self.displayDiagnosticDataOnStdout = display_stdout_or_dialog

		print("%s : self.dir_output = %s" % (nameProcedure, self.dir_output))

		print("%s : Exit" % (nameProcedure))


	def __run(

	  self
	) :

		"""
		Copy and paste the foreground image onto the background image, flatten the background image down into one layer, and
		then save the result to file.


		Parameters:

		NA


		Returns:

		NA


		Invoked by :

		OverlayImageAgent.runMultipleFromList
		OverlayImageAgent.runMultipleFromFile


		Invokes :

		OverlayImageAgent.__copyAndPasteForegroundImage
		OverlayImageAgent.__copyAndPasteForegroundImageAsNew
		OverlayImageAgent.__displayDiagnosticData
		OverlayImageAgent.__flattenAndSaveImage
		"""


		nameProcedure = "OverlayImageAgent::__run"


		print("%s : Enter" % (nameProcedure))

		# Copy and paste the foreground image onto the background image.

		self.__copyAndPasteForegroundImage()

		self.__displayDiagnosticData(nameProcedure + " : copyAndPasteForegroundImage just invoked")

		# Flatten the resulting image and then save it to file.

		self.__flattenAndSaveImage()

		print("%s : Exit" % (nameProcedure))


	def __run_copyAndPasteAsNew(

	  self
	) :

		"""
		Copy and paste the foreground image onto the background image, flatten the background image down into one layer, and
		then save the result to file. This process is repeated for each foreground image which is passed to this method.


		Parameters:

		NA


		Returns:

		NA


		Invoked by :

		OverlayImageAgent.runMultipleFromList
		OverlayImageAgent.runMultipleFromFile


		Invokes :

		OverlayImageAgent.__copyAndPasteForegroundImage
		OverlayImageAgent.__copyAndPasteForegroundImageAsNew
		OverlayImageAgent.__displayDiagnosticData
		OverlayImageAgent.__flattenAndSaveImage
		"""


		nameProcedure = "OverlayImageAgent::__run"


		print("%s : Enter" % (nameProcedure))

		# Copy and paste the foreground image onto the background image.

		self.__copyAndPasteForegroundImageAsNew()

		self.__displayDiagnosticData(nameProcedure + " : copyAndPasteForegroundImage just invoked")

		# Flatten the resulting image and then save it to file.

		self.__flattenAndSaveImage()

		print("%s : Exit" % (nameProcedure))


	def runMultipleFromList(

		  self,
		  filenames_foreground,
		  seperator_character
		) :
			"""
			Copy and paste the foreground image onto the background image, flatten the background image down into one layer, and
			then save the result to file.
	
	
			Parameters:
	
			NA
	
	
			Returns:
	
			NA


			Invoked by :

			runPlugin_multiple_fromList
			OverlayImageAgent.runMultipleFromFile


			Invokes :

			OverlayImageAgent.__getForegroundImageAndDrawable
			OverlayImageAgent.__displayDiagnosticData
			OverlayImageAgent.__run
			"""


			nameProcedure = "OverlayImageAgent::runMultipleFromList"


			print("%s : Enter" % (nameProcedure))

			print("%s : filenames_foreground = %s" % (nameProcedure, filenames_foreground))
			print("%s : seperator_character  = %s" % (nameProcedure, seperator_character))

			# Ascertain how many Foreground Images were passed to this Plugin.

			self.filenames_foreground = filenames_foreground.split(seperator_character)

			print("%s : Number of Foreground filenames = %d" % (nameProcedure, len(self.filenames_foreground)))

			gimp.progress_init("Have got image and drawable from Background Image file")

			# Start a GIMP Undo group.
			#
			# This will allow the actions of this Plugin to be undone in one step.

			# pdb.gimp_image_undo_group_start(self.image_background)

			for filename_foreground in self.filenames_foreground :

				print("%s : filename_foreground = %s" % (nameProcedure, filename_foreground))

				if path.isfile(filename_foreground) :

					self.filename_foreground = filename_foreground

					print("%s : Filename Foreground image = %s" % (nameProcedure, self.filename_foreground))
					print("%s : Length of filename        = %d chars" % (nameProcedure, len(self.filename_foreground)))

					self.filename_result = self.__constructFilenameResult(self.filename_foreground)
	
					self.image_background    = pdb.gimp_file_load(self.filename_background, self.filename_background)
					self.drawable_background = pdb.gimp_image_get_active_layer(self.image_background)

					print("%s : Filename background image = %s" % (nameProcedure, self.image_background.filename))

					self.__getForegroundImageAndDrawable(self.filename_foreground)

					message = "<span foreground=\"black\" style=\"italic\">" + nameProcedure + " : Processing next Foreground Image</span>"

					self.__displayDiagnosticData(message)

					self.__run()

					# Close the GIMP Images now that we have finished with them, otherwise they will use up
					# memory unnecessarily.

					pdb.gimp_image_delete(self.image_foreground)
					pdb.gimp_image_delete(self.image_background)

				else :

					print("%s : Filename Foreground image DOESN'T exist = %s" % (nameProcedure, self.filename_foreground))

			# ----------------------------------------------------------------------------------------------
			# End the GIMP Undo group which was started at the beginning of this Plugin.
			# ----------------------------------------------------------------------------------------------

			# pdb.gimp_image_undo_group_end(self.image_background)

			print("%s : Exit" % (nameProcedure))


	def runMultipleFromFile(

		  self,
		  filename_foreground_files
		) :

			"""
			Invoke this Plugin on those foreground images which are listed in a specific file.
	
	
			Parameters:
	
			filename_foreground_files (String) : The filename of a file which itself contains a list of filenames. The filenames in this list should contain the
			foreground images which are to be operated on by this Plugin.
	
	
			Returns:
	
			NA
	
	
			Invoked by : Checked
	
			runPlugin_multiple_fromFile
	
	
			Invokes :
	
			OverlayImageAgent.runMultipleFromList
			"""
			

			nameProcedure = "OverlayImageAgent::runMultipleFromFile"


			print("%s : Enter" % (nameProcedure))

			with open(filename_foreground_files, 'r') as file_handle :

				filenames_foreground = file_handle.read()

			self.runMultipleFromList(filenames_foreground, '\n')

			print("%s : Exit" % (nameProcedure))


	def __constructFilenameResult(

	  self,
	  filename
	) :

		"""
		Construct the filename for the file which the resulting image is to be saved into.

		The filename will be constructed, based on;

		- which filename manipulation method which was specified
		- if a filename suffix has been specified


		Parameters:

		filename (String) : The filename which is to be used as the basis for the creation of the new filename.


		Returns:

		NA


		Invoked by :

		OverlayImageAgent.runMultipleFromList - checked


		Invokes :

		NA
		"""


		nameProcedure = "OverlayImageAgent::__computeFilenameResult"


		print("%s : Enter" % (nameProcedure))

		print("%s : self.dir_output = %s" % (nameProcedure, self.dir_output))

		if self.dir_output == None :

			print("%s : Output directory = None" % (nameProcedure))

		# Get the filename from the fully qualified filename (fqfn).

		filename = path.realpath(filename)

		filename_base_fq, file_extension = path.splitext(filename)

		filename_base = path.basename(filename_base_fq)

		print("%s : Filename      = %s" % (nameProcedure, filename))
		print("%s : Filename base = %s" % (nameProcedure, filename_base))

		# Remove any leading '.' characters from the filename extension.

		if file_extension.startswith(".") :

			file_extension = file_extension[1:]

		# If requested, manipulate the filename.

		print("%s : ====================" % (nameProcedure))
		print("%s : Filename manipulation method = %s" % (nameProcedure, self.filename_manipulation_method))
		print("%s : ====================" % (nameProcedure))

		if self.filename_manipulation_method == "DO_NOTHING" :

			filename = filename_base + "." + file_extension

		if self.filename_manipulation_method == "PREPEND_FILENAME" :

			print("%s : Filename suffix = %s" % (nameProcedure, self.filename_suffix))

			filename = self.filename_suffix + filename_base + "." + file_extension

		if self.filename_manipulation_method == "APPEND_FILENAME" :

			filename = filename_base + self.filename_suffix + "." + file_extension

		if self.filename_manipulation_method == "PREPEND_FILENAME_EXTENSION" :

			filename = filename_base + "." + self.filename_suffix + file_extension

		if self.filename_manipulation_method == "APPEND_FILENAME_EXTENSION" :

			filename = filename_base + "." + file_extension + self.filename_suffix

		print("%s : --------------------" % (nameProcedure))
		print("%s : Filename base = %s" % (nameProcedure, filename_base))
		print("%s : Filename      = %s" % (nameProcedure, filename))
		print("%s : Dir output    = %s" % (nameProcedure, self.dir_output))
		print("%s : --------------------" % (nameProcedure))

		# Construct the new filename.

		filename_new  = path.join(self.dir_output, filename)
		filename_new  = path.normpath(filename_new)

		print("%s : ++++++++++++++++++++" % (nameProcedure))
		print("%s : Filename      = %s" % (nameProcedure, filename))
		print("%s : Filename new  = %s" % (nameProcedure, filename_new))
		print("%s : ++++++++++++++++++++" % (nameProcedure))

		print("%s : Exit" % (nameProcedure))
		
		return(filename_new)


	def __getForegroundImageAndDrawable(

	  self,
	  filename_foreground
	) :

		"""
		Use GIMP to get the image and drawable objects from the forground image.


		Parameters:

		filename_forground (String) : The filename of the forground image file.


		Returns:

		NA


		Invoked by :

		OverlayImageAgent.runMultipleFromList


		Invokes :

		NA
		"""


		nameProcedure = "OverlayImageAgent::__getImageAndDrawable"


		print("%s : Enter" % (nameProcedure))

		# Get the following from both the foreground image file;
		#
		#   - image
		#   - drawable
		#
		# and save them into the appropriate global variables.

		self.image_foreground = pdb.gimp_file_load(filename_foreground, filename_foreground)
		self.drawable_foreground = pdb.gimp_image_get_active_layer(self.image_foreground)

		print("Filename foreground image = %s" % self.image_foreground.filename)

		gimp.progress_init("Have got image and drawable from Foreground Image file")

		print("%s : Exit" % (nameProcedure))


	def __copyForegroundImageIntoBuffer(
	
	  self
	) :

		"""
		Instruct GIMP to copy the foreground image into its buffer.


		Parameters:

		NA


		Returns:

		NA


		Invoked by :

		OverlayImageAgent.__copyAndPasteForegroundImage
		OverlayImageAgent.__copyAndPasteForegroundImageAsNew
		OverlayImageAgent.__copyAndPasteForegroundImageIntoNewLayer


		Invokes :

		OverlayImageAgent.__pauseAndProgressDisplay
		"""


		nameProcedure = "OverlayImageAgent::__copyForegroundImageIntoBuffer"


		print("%s : Enter" % (nameProcedure))

		# Copy the Foreground Image into the Buffer.

		copy_result = pdb.gimp_edit_copy(self.drawable_foreground)

		print("%s : Copy result = %s" % (nameProcedure, str(copy_result)))

		# Update the Progress Bar in the Plugin Window.

		gimp.progress_init("Have copied foreground image into Buffer")

		self.__pauseAndProgressDisplay(self.sleep_timer)


	def __copyAndPasteForegroundImage(

	  self
	) :

		"""
		Paste the foreground image onto the background image.

		Instruct GIMP to copy the forground image into its buffer, then paste the contents of this buffer into the background image.


		Parameters:

		NA


		Returns:

		NA


		Invoked by :

		OverlayImageAgent.__run


		Invokes :

		OverlayImageAgent.__copyForegroundImageIntoBuffer

		"""


		nameProcedure = "OverlayImageAgent::__copyAndPasteForegroundImage"


		print("%s : Enter" % (nameProcedure))

		# Copy the Foreground Image into the Buffer.

		self.__copyForegroundImageIntoBuffer()

		# Paste the Foreground Image from the Buffer onto the Background Image.
		#
		# This operation will add a new Layer to the Image.
		#
		# self.image_background_new will be of type gimp.Layer

		[num_layers, list_layer_ids] = pdb.gimp_image_get_layers(self.image_background)
		print("%s : Number of layers in Background Image = %d" % (nameProcedure, num_layers))

		print("%s : Filename Background Image = %s" % (nameProcedure, self.image_background.filename))

		floating_selection = pdb.gimp_edit_paste(self.drawable_background, True)

		if (floating_selection == -1) :

			print("%s : Attempted to paste from the Edit buffer, but it appears to be empty." % (nameProcedure))

			exception_message = "\n\nAn Exception has been raised by the method;\n\n  " + \
			                    nameProcedure + \
			                    "\n\nThis method attempted to paste from the Edit buffer, but it appears to be empty.\n\nAs a result, this Plugin is about to terminate!"

			raise Exception(exception_message)

		pdb.gimp_floating_sel_anchor(floating_selection)

		[num_layers, list_layer_ids] = pdb.gimp_image_get_layers(self.image_background)
		print("%s : Number of layers in Background Image = %d" % (nameProcedure, num_layers))

		# Update the Progress Bar in the Plugin Window.

		gimp.progress_init("Have pasted Foreground Image from Buffer onto Background Image")

		print("%s : Exit" % (nameProcedure))


	def __copyAndPasteForegroundImageAsNew(

	  self
	) :

		"""
		Paste the foreground image onto a new background image.

		Instruct GIMP to copy the forground image into its buffer, then paste the contents of this buffer into a new background image.


		Parameters:

		NA


		Returns:

		NA


		Invoked by :

		__run


		Invokes :

		__copyForegroundImageIntoBuffer

		"""


		nameProcedure = "OverlayImageAgent::__copyAndPasteForegroundImageAsNew"


		print("%s : Enter" % (nameProcedure))

		# Copy the Foreground Image into the Buffer.

		self.__copyForegroundImageIntoBuffer()

		# Paste the Foreground Image from the Buffer onto the Background Image.

		self.image_background_new = pdb.gimp_edit_paste_as_new(self.drawable_background, True)

		print("%s : Type = %s" % (nameProcedure, type(self.image_background_new)))

		if (self.image_background_new == -1) :

			print("%s : Attempted to paste from the Edit buffer, but it appears to be empty." % (nameProcedure))

			exception_message = "\n\nAn Exception has been raised by the method;\n\n  " + \
			                    nameProcedure + \
			                    "\n\nThis method attempted to paste from the Edit buffer, but it appears to be empty.\n\nAs a result, this Plugin is about to terminate!"

			raise Exception(exception_message)

		gimp.progress_init("Have pasted foreground image from Buffer onto background image")

		print("%s : Exit" % (nameProcedure))


	def __copyAndPasteForegroundImageIntoNewLayer(

	  self
	) :

		"""
		Paste the foreground image onto a new layer of the background image.

		Instruct GIMP to copy the forground image into its buffer, then paste the contents of this buffer into a new layer of the background image.


		Parameters:

		NA


		Returns:

		NA


		Invoked by :

		__run


		Invokes :

		__copyForegroundImageIntoBuffer

		"""

		nameProcedure = "OverlayImageAgent::__copyAndPasteForegroundImageIntoNewLayer"


		print("%s : Enter" % (nameProcedure))

		# Copy the Foreground Image into the Buffer.

		self.__copyForegroundImageIntoBuffer()

		# Paste the Foreground Image from the Buffer onto the Background Image.

		# WORK OUT WHAT TO DO HERE!!!

		gimp.progress_init("Have pasted FG Image from Buffer into new Layer")

		print("%s : Exit" % (nameProcedure))


	def __flattenAndSaveImage(

	  self
	) :

		"""
		Flatten the current image and then save it to file.

		Instruct GIMP to flatten the current image by collapsing all of the image's layers down into one layer and then saving the resulting image to file.


		Parameters:

		NA


		Returns:

		NA


		Invoked by :

		__run


		Invokes :

		__pauseAndProgressDisplay

		"""


		nameProcedure = "OverlayImageAgent::flattenAndSaveImage"


		print("%s : Enter" % (nameProcedure))

		if (type(self.image_background) is not gimp.Image) :

			exception_message = "\n\nAn Exception has been raised by the method;\n\n  " + \
			                    nameProcedure + \
			                    "\n\n" + \
			                    "This method is attempting to flatten an Object which is not an Image." + \
			                    "\n\n" + \
			                    "Object is of type : " + type(self.image_background) + \
			                    "As a result, this Plugin is about to terminate!"

			raise Exception(exception_message)

		# Flatten the modified background image down into one layer.

		drawable_background = pdb.gimp_image_flatten(self.image_background)

		message = "<span foreground=\"black\" style=\"italic\"> Have flattened the image : " + self.image_background.filename + "</span>"

		self.__displayDiagnosticData(message)

		gimp.progress_init("Have flattened the background image")

		self.__pauseAndProgressDisplay(self.sleep_timer)

		# Save the background image into the specified file.

		pdb.gimp_file_save(

		  self.image_background,
		  drawable_background,
		  self.filename_result,
		  self.filename_result
		)

		gimp.progress_init("Have saved the background image")

		self.__pauseAndProgressDisplay(self.sleep_timer)

		print("%s : Enter" % (nameProcedure))


	def __pauseAndProgressDisplay(

	  self,
	  sleep_seconds
	) :

		"""
		Pause the execution of the program and update the Progress indicator in GIMPs GUI panel.


		Parameters:

		sleep_seconds (Int) : The number of seconds the program should sleep for.


		Returns:

		NA


		Invoked by :

		Many procedures.


		Invokes :

		NA

		"""


		nameProcedure = "OverlayImageAgent::pauseAndProgressDisplay"

		counter_max = 100

		counter     = 0


		print("%s : Enter" % (nameProcedure))

		if sleep_seconds > 0 :

			while counter < counter_max :

				time.sleep(float(sleep_seconds) / float(counter_max))

				counter = counter + 1

				gimp.progress_update(float(counter) / float(counter_max))

		print("%s : Exit" % (nameProcedure))


	def __displayDiagnosticData(

		  self,
		  invocationMessage
		) :


		DiagnosticDataDialog(

		  self.displayDiagnosticDataOnStdout,
		  self.counter,
		  invocationMessage,
		  self.image_background,
		  self.image_foreground
		)


register(
	"runPlugin_single",                                     # The name of the command.
	"Overlay a foreground image onto a background image.",  # A brief description of the command.
	"Overlay a foreground image onto a background image.",  # Help message.
	"Craig Sanders",                                        # Author.
	"Craig Sanders",                                        # Copyright holder.
	"2019",                                                 # Date.
	"Overlay Image",                                        # The way the script will be referred to in the menu.
	# "RGB*, GRAY*",                                        # Image mode
	"",                                                     # Create a new image, don't work on an existing one.
	[
		(PF_FILE,       "filename_background",        "Filename of Background Image",     "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/slides/png/Eulers_formula_animation_slides-000001.png"),
		(PF_FILE,       "filename_foreground",        "Filename of Foreground Image",     "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/frames/png/animation_1/Eulers_formula_000100.png"),
		(PF_STRING,     "filename_result",            "Filename of Resulting Image",      "/home/craig/temp/image_result.png"),
		(PF_RADIO,      "display_stdout_or_dialog",   "Where should this Plugin display\nits diagnostic data?",     DIAGNOSTIC_DATA_NONE,
			(
				("Stdout",                                  DIAGNOSTIC_DATA_STDOUT),
				("Dialog Window",                           DIAGNOSTIC_DATA_DIALOG),
				("Both (Both Stdout and Dialog Window)",    DIAGNOSTIC_DATA_BOTH),
				("None (Neither Stdout nor Dialog Window)", DIAGNOSTIC_DATA_NONE)
			)
		)
	],
	[],
	runPlugin_single,
	menu="<Image>/Image/Craig's Utilities/")


# runPlugin_multiple_fromList
#   OverlayImageAgent Ctor
#   OverlayImageAgent.runMultipleFromList
#     OverlayImageAgent.__getForegroundImageAndDrawable
#     OverlayImageAgent.__displayDiagnosticData
#     OverlayImageAgent.__run
#       OverlayImageAgent.__copyAndPasteForegroundImage
#         OverlayImageAgent.__copyForegroundImageIntoBuffer
#       OverlayImageAgent.__copyAndPasteForegroundImageAsNew
#       OverlayImageAgent.__displayDiagnosticData
#       OverlayImageAgent.__flattenAndSaveImage

register(
	"runPlugin_multiple_fromList",                                               # The name of the command.
	"Overlay a Foreground Image onto a Background Image." +  
	"\n\n"                                                +
	"(The Foreground Images to operate on will be read from the field below.)",  # A brief description of the command.
	"Overlay a Foreground Image onto a Background Image.",                       # Help message.
	"Craig Sanders",                                                             # Author.
	"Craig Sanders",                                                             # Copyright holder.
	"2019",                                                                      # Date.
	"Overlay Images (From List)",                                                # The way the script will be referred to in the menu.
	# "RGB*, GRAY*",                                                             # Image mode
	"",                                                                          # Create a new image, don't work on an existing one.
	[
		(PF_FILE,       "filename_background",        "Filename of Background Image",     "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/slides/png/Eulers_formula_animation_slides-000001.png"),
		(
		 PF_RADIO,
		 "list_source",
		 "Where should this Plugin read its list of\n" +
		 "foreground files from?",
		 READ_LIST_FROM_FIELD,
			(
				("From stdin",       READ_LIST_FROM_STDIN),
				("From field below", READ_LIST_FROM_FIELD)
			)
		),
		(
		 PF_FILE,
		 "filename_foreground",
		 "Filenames of Foreground Images\n" + 
		 "(Seperate filenames with ';' characters)\n",
		 "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/frames/png/animation_1/Eulers_formula_000100.png"
		),
		(PF_STRING,     "dir_output",                 "Directory to save Files into\n(Leave empty for same directory)", ""),
		(PF_RADIO,      "filename_manipulation",      "How should this Plugin manipulate the\nForeground Image's filename to generate\nthe Resulting Image's filename?", PREPEND_FILENAME,
			(
				("By prepending suffix to filename base",                PREPEND_FILENAME),
				("By appending suffix to filename base",                 APPEND_FILENAME),
				("By prepending suffix to filename extension",           PREPEND_FILENAME_EXTENSION),
				("By appending suffix to filename extension",            APPEND_FILENAME_EXTENSION)
			)
		),
		(PF_STRING,     "filename_suffix",            "Suffix string",      "result"),
		(PF_RADIO,      "display_stdout_or_dialog",   "Where should this Plugin display\nits diagnostic data?",     DIAGNOSTIC_DATA_NONE,
			(
				("Stdout",                                  DIAGNOSTIC_DATA_STDOUT),
				("Dialog Window",                           DIAGNOSTIC_DATA_DIALOG),
				("Both (Both Stdout and Dialog Window)",    DIAGNOSTIC_DATA_BOTH),
				("None (Neither Stdout nor Dialog Window)", DIAGNOSTIC_DATA_NONE)
			)
		)
	],
	[],
	runPlugin_multiple_fromList,
	menu="<Image>/Image/Craig's Utilities/")


register(
	"runPlugin_multiple_fromFile",                                      # The name of the command.
	"Overlay a Foreground Image onto a Background Image." +
	"\n\n"                                                +
	"(The Foreground Images to operate on will be read from a File.)",  # A brief description of the command.
	"Overlay a Foreground Image onto a Background Image.",              # Help message.
	"Craig Sanders",                                                    # Author.
	"Craig Sanders",                                                    # Copyright holder.
	"2019",                                                             # Date.
	"Overlay Images (From File)",                                       # The way the script will be referred to in the menu.
	# "RGB*, GRAY*",                                                    # Image mode
	"",                                                                 # Create a new image, don't work on an existing one.
	[
		(PF_FILE,
		 "filename_background",
		 "Filename of Background Image",
		 "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/slides/png/Eulers_formula_animation_slides-000001.png"
		),
		(PF_FILE,       "filename_foreground_files",    "Filename of file which contains a list of\nForeground Images", "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/frames/png/animation_1/fileList.txt"),
		(PF_STRING,     "dir_output",                   "Directory to save Files into\n(Leave empty for same directory)", ""),
		(PF_RADIO,      "filename_manipulation_method", "How should this Plugin manipulate the\nForeground Image's Filename to generate\nthe Resulting Image's Filename?", DO_NOTHING,
			(
				("Don't do anything",                                    DO_NOTHING),
				("By prepending suffix to filename base",                PREPEND_FILENAME),
				("By appending suffix to filename base",                 APPEND_FILENAME),
				("By prepending suffix to filename extension",           PREPEND_FILENAME_EXTENSION),
				("By appending suffix to filename extension",            APPEND_FILENAME_EXTENSION)
			)
		),
		(PF_STRING,     "filename_suffix",            "Suffix string",      "result"),
		(PF_RADIO,      "display_stdout_or_dialog",   "Where should this Plugin display\nits diagnostic data?",     DIAGNOSTIC_DATA_NONE,
			(
				("Stdout",                                  DIAGNOSTIC_DATA_STDOUT),
				("Dialog Window",                           DIAGNOSTIC_DATA_DIALOG),
				("Both (Both Stdout and Dialog Window)",    DIAGNOSTIC_DATA_BOTH),
				("None (Neither Stdout nor Dialog Window)", DIAGNOSTIC_DATA_NONE)
			)
		)
	],
	[],
	runPlugin_multiple_fromFile,
	menu="<Image>/Image/Craig's Utilities/")

if (SPHINX_ACTIVE == False) :

	main()
