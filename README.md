Python Script and associated GIMP Plugin to overlay one Image on top of another.
================================================================================

Throughout the remainder of this documentation, the image that is being overlaid on top of another image is referred to as the foreground image, while
the image that is being overlaid onto, is referred to as the background image.

Both the Python Script and its associated GIMP Plugin can be used to overlay one Image on top of another.

They can both be invoked either interactively from within GIMP, or non-interactively (aka Btch mode) from the command line.


Invoking the Python Script interactively from within GIMP.
----------------------------------------------------------

To invoke the Python Script interactively, start up GIMP and then click;

  Filters > Python-Fu > Console

Next, from within the Python Console Window, invoke the following two commands;

	>>> import sys
	>>> print("%s" % (sys.path))

The second command should display a list of those directories which Python searches for modules. If the directory which contains
the Python Script is not show in this list, then invoke the following command;

	>>> sys.path = <Name_of_dir_containing_Python_Script> + sys.path

This should add - by prepending to the front of the list of directories that Python searches for modules, the directory whics contains
the Python Script.

Now, just invoke the following two commands;

	>>> import HelloWorld
	>>> HelloWorld.displayMessage("Hello, World!")


Invoking the GIMP Plugin interactively from within GIMP.
--------------------------------------------------------

To invoke the GIMP Plugin interactively, start up GIMP and then use it to open the background image. Once this is done, select;

  Image > Craig's Utilities > Overlay Image

Doing this should cause the following panel to be displayed. 

![Test image](/images/Panel.png "Panel displayed by the Image Overlay Plugin")


Invoking this Plugin non-interactively from the command line.
-------------------------------------------------------------

To invoke this Plugin non-interactively, issue a command from the command line which is similar to the following;

	find /home/foo/images -name "foreground_image_[0-9].png" | \
	sort | \
	gimp --no-interface \
	     --verbose \
	     --console-messages \
	     --batch-interpreter="plug-in-script-fu-eval" \
	     --batch '(
	               python-fu-runPlugin-multiple-fromList
	               RUN-NONINTERACTIVE
	               "/home/foo/images/background_image.png"
	               "READ_LIST_FROM_STDIN"
	               ""
	               "/home/craig/temp/Animation_images_png/"
	               "PREPEND_FILENAME"
	               "Slide_"
	               "DIAGNOSTIC_DATA_NONE"
	              )' \
	     --batch '(
	               gimp-quit 0
	              )'

> A quick note about the syntax of this command.
>
> The arguments to a batch sub-command should be placed within the batch sub-command's parentheses. These arguments seem to get passed directly to
> GIMP, therefore they should not contain any shell special or control characters. For example, if the arguments contained one or more instances of the "\\"
> character, then GIMP might not know how to interpret them, and this could cause an error such as;
>
> batch command experienced an execution error:
> Error: ( : 1) eval: unbound variable: \

The command which was just presented, might seem a little overwhelming. So to try and help explain what it is doing, here is the same command but with comments added.

	find /home/foo/images -name "foreground_image_[0-9].png" | \  # Find the foreground image filenames of interest and redirect them.
	sort | \                                                      # Sort the list of foreground image filenmes.
	gimp --no-interface \                                         # Instruct GIMP to operate without using its (graphical user) interface. This causes GIMP to execute in a non-interactive manner.
	     --verbose \                                              # Instruct GIMP to operate in a verbose manner.
	     --console-messages \                                     # Instruct GIMP to process console messages.
	     --batch-interpreter="plug-in-script-fu-eval" \           # Instruct GIMP to use Python-Fu to interpret the following batch sub-commands.
	     --batch '(                                               # Start a batch sub-command.
	               python-fu-runPlugin-multiple-fromList          # Name of the Plugin the batch sub-command should execute.
	               RUN-NONINTERACTIVE                             # Instruct the Plugin to operate in a non-interactive manner.
	               "/home/foo/images/background_image.png"        # Filename which contains the background image.
	               "READ_LIST_FROM_STDIN"                         # Read the list of foreground image filenames from stdin.
	               ""                                             #
	               "/home/craig/temp/Animation_images_png/"       # Directory to save the resulting files into.
	               "PREPEND_FILENAME"                             # Create a new filename from a foreground image filename by prepending a suffix to the latter.
	               "Slide_"                                       # Suffix which should be used.
	               "DIAGNOSTIC_DATA_NONE"                         # Instruct the Plugin to not generate diagnostic data.
	              )' \                                            # End the current batch sub-command.
	     --batch '(                                               # Start another batch sub-command.
	               gimp-quit 0                                    # Instruct GIMP to quit, and in doing so, return a value of 0 to the program which invoked it.
	              )'                                              # End the current batch sub-command. 

As can be seen from the comments, the "READ_LIST_FROM_STDIN" argument to the Plugin, forces it to read the list of foreground image filenames from stdin. This is
the reason why stdin of the gimp command, is connected to stdout of the find command by way of a pipe.


Registering the Plugin with GIMP.
---------------------------------

The Plugin is implemented in Python by a function which is called "runPlugin_multiple_fromList".

Since this function is responsible for implementing the Plugin, it is this function which must therefore be registered with GIMP. As part of the registration
process, GIMP also needs to know some other information about the Plugin which is being registered, such as;

- a short description which is to be associated with the Plugin,
- a short Help message which is to be assocaited with the Plugin,
- whereabouts within its Menu system GIMP should place a menu entry for this Plugin,
- how the GUI Panel which is associated with the Plugin should be laid out.


How the Plugin is implemented.
------------------------------

	runPlugin-multiple-fromList
	 |
	 |- OverlayImageAgent Ctor
	 |
	 |- OverlayImageAgent.runMultipleFromList
	     |
	     |- OverlayImageAgent.__getForegroundImageAndDrawable
	     |
	     |- OverlayImageAgent.__displayDiagnosticData
	     |
	     |- OverlayImageAgent.__run
	         |
	         |- OverlayImageAgent.__copyAndPasteForegroundImage
	         |   |
	         |   |- OverlayImageAgent.__copyForegroundImageIntoBuffer
	         |   |
	         |   |- OverlayImageAgent.__pauseAndProgressDisplay
	         |
	         |- OverlayImageAgent.__copyAndPasteForegroundImageAsNew
	         |
	         |- OverlayImageAgent.__displayDiagnosticData
	         |
	         |- OverlayImageAgent.__flattenAndSaveImage
	             |
	             |- OverlayImageAgent.__displayDiagnosticData
	             |
	             |- OverlayImageAgent.__pauseAndProgressDisplay
	             |
	             |- OverlayImageAgent.__pauseAndProgressDisplay
