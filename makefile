SHELL=/bin/bash

no_default:
	@echo "Available targets: init_py, build, publish, pdf, clean, dev"
init_py:
	@echo "Initializing python environment..."
	cd deployment && source setup.sh --venv=false
pdf:
	@echo "Rendering PDF..."
	@echo "> Installing dependencies..."
	cd deployment && cd pdf && npm install
	@cd deployment && cd pdf && for lang in 'en' 'es'; do \
		echo "> Rendering $$lang"; \
		node web2pdf.js $$lang; \
	done
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