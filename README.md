GIMP Plugin to overlay one image on top of another.
===================================================

The image that is being used to overlay itself onto another image, is referred to as the foreground image; while
the image that is being overlaid onto, is referred to as the background image.

This Plugin can either be invoked interactively from within GIMP, or non-interactively from the command line.


Invoking this Plugin interactively from within GIMP.
----------------------------------------------------

To invoke this Plugin interactively, start up GIMP and then use it to open the background image. Once this is done, select;

  Image > Craig's Utilities > Overlay Image

Doing this should cause the following panel to be displayed. 

![Test image](/images/Panel.png)


Invoking this Plugin non-interactively from the command line.
-------------------------------------------------------------

To invoke this Plugin non-interactively, issue a command from the command line which is similar to the following;

	find /home/foo/images -name "foreground_image_[0-9].png" | \
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
	     --batch '(gimp-quit 0)'

> A quick note about the syntax of this command.
>
> The arguments to a batch sub-command should be placed within the batch sub-command's parentheses. It appears as though these arguments get passed directly to
> GIMP, therefore they should not contain any shell special or control characters. For example, if the arguments contained one or more instances of the "\\"
> character, then GIMP might not know how to interpret them, and this could cause an error such as;
>
> batch command experienced an execution error:
> Error: ( : 1) eval: unbound variable: \

	find /home/foo/images -name "foreground_image_[0-9].png" | \  # Send list of foreground image filenames to stdout.
	gimp --no-interface \                                         # Instruct GIMP to operate in a non-interactive manner.
	     --verbose \                                              # Instruct GIMP to operate in a verbose manner.
	     --console-messages \                                     # Instruct GIMP to display console messages.
	     --batch-interpreter="plug-in-script-fu-eval" \           # Instruct GIMP to use Python-Fu to interpret any batch commands.
	     --batch '(                                               # Start a batch command.
	               python-fu-runPlugin-multiple-fromList          # Name of the Plugin to execute.
	               RUN-NONINTERACTIVE                             # Run the Plugin in a non-interactive manner.
	               "/home/foo/images/background_image.png"        # Filename which contains the background image.
	               "READ_LIST_FROM_STDIN"                         # Read the list of foreground image filenames from stdin.
	               ""                                             #
	               "/home/craig/temp/Animation_images_png/"       # Directory to save files into.
	               "PREPEND_FILENAME"                             # Create new filenames by prepending a suffix to existing filenames.
	               "Slide_"                                       # Suffix to use.
	               "DIAGNOSTIC_DATA_NONE"                         # Instruct the Plugin to not generate diagnostic data.
	              )' \
	     --batch '(gimp-quit 0)'

The Plugin is invoked in such a way that it reads its list of files to operate on from stdin. This is the reason why the input of the gimp command, is connected
to the outut of the find command by way of a pipe.


The Plugin is instructed to do so by way of the "READ_LIST_FROM_STDIN"
sub-command argument.
