STYLE_COMPILER = lessc
SCRIPT_COMPILER = coffee -b -c -o
MIN_SCRIPT_COMPILER = uglifyjs -o
TEMPLATE_COMPILER = haml
MKDIR = mkdir -p

# dir
SOURCE_DIR = .
TARGET_DIR = ../data/compiled

# dir for less
STYLE_SOURCE_DIR = $(SOURCE_DIR)/less
STYLE_TARGET_DIR = $(TARGET_DIR)/css

# dir for coffee script
SCRIPT_SOURCE_DIR = $(SOURCE_DIR)/coffee
SCRIPT_TARGET_DIR = $(TARGET_DIR)/js

# dir for template
TEMPLATE_SOURCE_DIR = $(SOURCE_DIR)/haml
TEMPLATE_TARGET_DIR = $(TARGET_DIR)/html

# less file list
STYLE_SOURCES = $(shell find $(STYLE_SOURCE_DIR) -name '*.less')
STYLE_TARGETS = $(patsubst $(STYLE_SOURCE_DIR)/%.less, $(STYLE_TARGET_DIR)/%.css, $(STYLE_SOURCES))

# coffee script file list
SCRIPT_SOURCES = $(shell find $(SCRIPT_SOURCE_DIR) -name '*.coffee')
SCRIPT_TARGETS = $(patsubst $(SCRIPT_SOURCE_DIR)/%.coffee, $(SCRIPT_TARGET_DIR)/%.js, $(SCRIPT_SOURCES))
SCRIPT_COMPRESSED_TARGETS = $(patsubst $(SCRIPT_TARGET_DIR)/%.js, $(SCRIPT_TARGET_DIR)/%.min.js, $(SCRIPT_TARGETS))

# haml file list
TEMPLATE_SOURCES = $(shell find $(TEMPLATE_SOURCE_DIR) -name '*.haml')
TEMPLATE_TARGETS = $(patsubst $(TEMPLATE_SOURCE_DIR)/%.haml, $(TEMPLATE_TARGET_DIR)/%.html, $(TEMPLATE_SOURCES))

TARGETS = $(STYLE_TARGETS) $(SCRIPT_TARGETS) $(SCRIPT_COMPRESSED_TARGETS) $(TEMPLATE_TARGETS)

first : all

# compile for files
$(STYLE_TARGET_DIR)/%.css : $(STYLE_SOURCE_DIR)/%.less Makefile
	$(STYLE_COMPILER) "$<" > "$@"

$(SCRIPT_TARGET_DIR)/%.js : $(SCRIPT_SOURCE_DIR)/%.coffee Makefile
	$(SCRIPT_COMPILER) $$(dirname "$@") "$<"

$(SCRIPT_TARGET_DIR)/%.min.js : $(SCRIPT_TARGET_DIR)/%.js
	$(MIN_SCRIPT_COMPILER) "$@" "$<"

$(TEMPLATE_TARGET_DIR)/%.html : $(TEMPLATE_SOURCE_DIR)/%.haml Makefile
	$(TEMPLATE_COMPILER) "$<" "$@"

# auto make dir
define depend_on_dir
$(1): | $(dir $(1))
ifndef $(dir $(1))_DIRECTORY_RULE_IS_DEFINED
$(dir $(1)):
	$(MKDIR) $$@

$(dir $(1))_DIRECTORY_RULE_IS_DEFINED := 1
endif
endef

$(foreach file, $(TARGETS), $(eval $(call depend_on_dir, $(file))))

# all
all: $(TARGETS)

# common.less
$(STYLE_TARGETS) : less/common.less

clean:
	rm -rv $(TARGET_DIR)
