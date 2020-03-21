clean:
	@rm -rf ./.tmp/*.*

all: nasdaq.all nyse.all

%.all: clean %.download.json %.convert.csv %.dist
	@echo "Downloaded data for: $*"

%.download.json: clean
	@scrapy runspider ./markets/$*.py -o ./.tmp/$*.json
	@echo "Downloaded JSON data for: $*"

%.convert.csv: clean %.download.json
	@cat .tmp/$*.json | jq -r '(map(keys) | add | unique) as $$cols | map(. as $$row | $$cols | map($$row[.])) as $$rows | $$cols, $$rows[] | @csv' > .tmp/$*.csv
	@echo "Converted JSON data for $* into csv"

%.dist: %.download.json %.convert.csv
	@mkdir -p data/$*
	@cp .tmp/$*.json data/$*/
	@cp .tmp/$*.csv data/$*/

release: version=`date +'%Y.%M.%d'`
release:
	@git add --all data/
	@git commit -m "Release v$(version)"
	@git push
	@git tag "v$(version)"
	@git push --tag "v$(version)"

.PONY: all clean release
