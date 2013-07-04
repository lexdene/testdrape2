STYLE_COMPILER = lessc --yui-compress
MKDIR = mkdir -p

TARGET_DIR = ../data/static

STYLE_TARGET_DIR = $(TARGET_DIR)/css
STYLE_TARGETS = $(STYLE_TARGET_DIR)/frame/Layout.css \
		$(STYLE_TARGET_DIR)/jdmd_widget.css \
		$(STYLE_TARGET_DIR)/discuss/List.css \
		$(STYLE_TARGET_DIR)/userinfo/UserPanel.css \
		$(STYLE_TARGET_DIR)/userinfo/MainPage.css \
		$(STYLE_TARGET_DIR)/discuss/Topic.css \
		$(STYLE_TARGET_DIR)/newsfeed/Template.css \
		$(STYLE_TARGET_DIR)/usermsg/MyMsgList.css \

SCRIPT_TARGET_DIR = $(TARGET_DIR)/coffee
SCRIPT_LIST = $(SCRIPT_TARGET_DIR)/usermsg/Usermsg \
		$(SCRIPT_TARGET_DIR)/usermsg/MyMsgList

SCRIPT_TARGETS = $(foreach n,$(SCRIPT_LIST), $n.js)
SCRIPT_COMPRESSED_TARGETS = $(foreach n,$(SCRIPT_LIST), $n.min.js)

first : all

$(STYLE_TARGET_DIR)/%.css : less/%.less Makefile
	$(MKDIR) $$(dirname "$@")
	$(STYLE_COMPILER) "$<" > "$@"

$(SCRIPT_TARGET_DIR)/%.js : coffee/%.coffee Makefile
	$(MKDIR) $$(dirname "$@")
	coffee -c -o $$(dirname "$@") "$<"

$(SCRIPT_TARGET_DIR)/%.min.js : $(SCRIPT_TARGET_DIR)/%.js
	uglifyjs -o "$@" "$<"

all: $(STYLE_TARGETS) $(SCRIPT_TARGETS) $(SCRIPT_COMPRESSED_TARGETS)

$(STYLE_TARGETS) : less/common.less

.PRECIOUS: %.js
.SECONDARY: %.js
