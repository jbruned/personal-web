no_default:
	@echo "Available targets: init_py, build, publish, pdf, clean, dev"
init_py:
	@echo "Initializing python environment..."
	cd deployment && source setup.sh --venv=false
pdf:
	@echo "Rendering PDF..."
	cd deployment && cd pdf && npm install && node web2pdf.js
dev:
	@echo "Starting development server..."
	cd deployment && source build.py --live
build:
	@echo "Building site..."
	cd deployment && python build.py
publish:
	@echo "Publishing build..."
	cd deployment && python publish.py -v
clean:
	@echo "Cleaning generated files..."
	cd deployment && python clean.py