SHELL=/bin/bash

no_default:
	@echo "Available targets: init_py, build, publish, pdf, clean, dev"
init_py:
	@echo "Initializing python environment..."
	cd deployment && source setup.sh --venv=false
dev:
	@echo "Starting development server..."
	cd deployment && python build.py --live
build:
	@echo "Building site..."
	cd deployment && python build.py
font:
	@echo "Generating font files..."
	cd deployment && cd font && npm install && rm -rf .fontello-session && \
		npx fontello-cli --config ../../assets/fonts/jbruned-icons.json --css ../../assets/fonts --font ../../assets/fonts install && \
		cd ../../assets/fonts && rm -rf animation.css *-codes.css *-embedded.css *-ie7.css *-ie7-codes.css && \
		sed 's/..\/font\///' jbruned-icons.css > jbruned-icons.css.tmp && mv jbruned-icons.css.tmp jbruned-icons.css
pdf:
	@echo "Rendering PDF..."
	@echo "> Installing dependencies..."
	cd deployment && cd pdf && npm install
	@cd deployment && cd pdf && for lang in 'en' 'es'; do \
		echo "> Rendering $$lang"; \
		node web2pdf.js $$lang; \
	done
publish:
	@echo "Publishing build..."
	cd deployment && python publish.py -v
clean:
	@echo "Cleaning generated files..."
	cd deployment && python clean.py
