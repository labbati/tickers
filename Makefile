clean:
	@rm -rf ./.tmp/*

help:
	@echo "Help!"

%.dump: clean %.dump.json %.dump.csv %.dist
	@echo "Scraping data for: $@"
