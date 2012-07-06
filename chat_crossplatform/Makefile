CSS_FILE = ./static/css/main.css
LESS_FILE = ./static/less/main.less

DATE=$(shell date +%I:%M%p)
CHECK=✔
HR=\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#


#
# BUILD DOCS
#

build:
	@echo "${HR}"
	@echo "Building Bootstrap..."
	@echo "${HR}"
	@recess --compile ${LESS_FILE} > ${CSS_FILE}
	@echo "Compiling LESS with Recess...               ${CHECK} Done"
	@echo "${HR}"
	@coffee -o ./static/js/ -c ./static/coffee/*.coffee
	@echo "Compiling CoffeeScript...                   ${CHECK} Done"
	@echo "${HR}"
	@echo "built success at ${DATE}."
	@echo "${HR}"


#
# WATCH LESS FILES
#

watch:
	echo "Watching less files..."; \
	watchr -e "watch('less/.*\.less') { system 'make' }"
