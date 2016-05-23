#files to be included in the distribution
DUA=$(wildcard dua/*)
COLL_KEYWORDS=$(patsubst %.csv,%,$(wildcard vocabulary/collection_keyword/*.csv))
VOC_ETHICAL_REVIEW_BOARD=vocabulary/ethics_review_board.json
VOC_PUBLICATION_SYSTEM=vocabulary/publication_system.json
CMS_HELP_INDEX=cms_help_index.json
CMS_SNIPPETS_MD=$(patsubst %.md,%,$(wildcard privacy/*.md))

#list of JSON files subject for validation
JSON_FILES=$(wildcard dua/*.json) $(VOC_ETHICAL_REVIEW_BOARD) $(VOC_PUBLICATION_SYSTEM) $(CMS_HELP_INDEX) $(patsubst %,%.json,$(COLL_KEYWORDS)) 

#constant
VERSION:=master

#targets
.PHONY: build validate_json dist

# convert contents into proper formats
build: $(COLL_KEYWORDS) $(CMS_SNIPPETS_MD)

$(COLL_KEYWORDS):
	@echo "--> converting $@.csv to JSON ..."
	@python $(shell pwd)/tools/csv2json.py $@.csv $@.json

$(CMS_SNIPPETS_MD):
	@echo "--> converting $@.md to CMS snippet ..."
	@python $(shell pwd)/tools/md2html.py $@.md

# validate JSON files
validate_json: $(JSON_FILES)

$(JSON_FILES): build 
	@echo "--> validating $@"

# make distribution tarball 
dist: build
	@tar cvzf rdm-ontology-$(VERSION).tgz $(DUA) $(patsubst %,%.json,$(COLL_KEYWORDS)) $(VOC_ETHICAL_REVIEW_BOARD) $(VOC_PUBLICATION_SYSTEM) $(CMS_HELP_INDEX) $(patsubst %,%.html,$(CMS_SNIPPETS_MD))
