GIMP Plugin to overlay one image on top of another.
===================================================

The image that is being used to overlay itself onto another image, is referred to as the foreground image; while
the image that is being overlaid onto, is referred to as the background image.

This Plugin can either be invoked interactively from within GIMP, or non-interactively from the command line.


Invoking this Plugin interactively from within GIMP
---------------------------------------------------

Start by opening the background image within GIMP. Then click on;

  Image > Craig's Utilities > Overlay Image

Doing this should ...


Invoking this Plugin non-interactively from the command line
------------------------------------------------------------

To invoke this Plugin from the command line, use a command which is similar to the following;

	find /home/craig/Pictures/ -name "Wicket the Ewok.jpeg" | \
	gimp --no-interface \
	     --verbose \
	     --console-messages \
	     --batch-interpreter="plug-in-script-fu-eval" \
	     --batch '(
	               python-fu-runPlugin-multiple-fromList
	               RUN-NONINTERACTIVE
	               "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/slides/png/Eulers_formula_animation_slides-000001.png"
	               "READ_LIST_FROM_STDIN"
	               ""
	               "/home/craig/temp/Animation_images_png/"
	               "PREPEND_FILENAME"
	               "Slide_"
	               "DIAGNOSTIC_DATA_NONE"
	              )' \
	     --batch '(gimp-quit 0)'

The arguments to a batch sub-command should be placed within the batch sub-command's parentheses. It appears as though these arguments get passed directly to
GIMP, therefore they should not contain any shell special or control characters. For example, if the arguments contained one or more instances of the "\\"
character, then GIMP might not know how to interpret them and this could cause an error such as;

> batch command experienced an execution error:
> Error: ( : 1) eval: unbound variable: \
