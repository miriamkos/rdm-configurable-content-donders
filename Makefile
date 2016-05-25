#files to be included in the distribution
DUA=$(wildcard dua/*)
COLL_KEYWORDS=$(patsubst %.csv,%.json,$(wildcard vocabulary/collection_keyword/*.csv))
VOC_ETHICAL_REVIEW_BOARD=vocabulary/ethics_review_board.json
VOC_PUBLICATION_SYSTEM=vocabulary/publication_system.json
CMS_HELP_INDEX=cms_help_index.json
CMS_SNIPPETS_MD=$(patsubst %.md,%.html,$(wildcard privacy/*.md))

#list of JSON files subject for validation
JSON_FILES=$(wildcard dua/*.json) $(VOC_ETHICAL_REVIEW_BOARD) $(VOC_PUBLICATION_SYSTEM) $(CMS_HELP_INDEX) $(COLL_KEYWORDS)

JSON_SCHEMAS=$(wildcard $(patsubst %.json,%.schema,$(JSON_FILES)))

#list of files to be included in distribution or installation
DIST_FILES=$(DUA) $(COLL_KEYWORDS) $(VOC_ETHICAL_REVIEW_BOARD) $(VOC_PUBLICATION_SYSTEM) $(CMS_HELP_INDEX) $(CMS_SNIPPETS_MD)

#constant
VERSION:=master
INSTALL_PREFIX:=/tmp/rdm-ontology
DIST_TARBALL:=rdm-ontology-$(VERSION).tgz

#targets
.PHONY: build dist install $(JSON_SCHEMAS)

# convert contents into proper formats
build: $(COLL_KEYWORDS) $(CMS_SNIPPETS_MD)

$(COLL_KEYWORDS):
	@echo "--> converting keyword: $@"
	@python $(shell pwd)/tools/csv2json.py $(patsubst %.json,%.csv,$@) $@

$(CMS_SNIPPETS_MD):
	@echo "--> converting CMS snippet: $@"
	@python $(shell pwd)/tools/md2html.py $(patsubst %.html,%.md,$@)

# validate JSON file when the corresponding .schema file is presented
validate_json: $(JSON_SCHEMAS)

$(JSON_SCHEMAS):
	@echo "--> validating JSON document: $(patsubst %.schema,%.json,$@)"
	@python $(shell pwd)/tools/json-validator.py $(patsubst %.schema,%.json,$@) $@

# make distribution tarball 
dist: $(DIST_TARBALL) 

$(DIST_TARBALL): build validate_json
	@tar cvzf $@ $(DIST_FILES)

# install
install: build validate_json
	$(foreach d,$(dir $(DIST_FILES)),install -d -m 0755 $(INSTALL_PREFIX)/$(d);)
	$(foreach f,$(DIST_FILES),install -m 0644 $(f) $(INSTALL_PREFIX)/$(f);)

# clean 
clean:
	rm -f $(DIST_TARBALL)
	$(foreach f,$(COLL_KEYWORDS),rm -f $(f);)
	$(foreach f,$(CMS_SNIPPETS_MD),rm -f $(f);)
