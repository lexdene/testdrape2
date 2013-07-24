STYLE_COMPILER = lessc --yui-compress
MKDIR = mkdir -p

TARGET_DIR = ../data/static

STYLE_TARGET_DIR = $(TARGET_DIR)/css
STYLE_LIST = frame/Layout \
		jdmd_widget \
		discuss/List \
		userinfo/UserPanel \
		userinfo/MainPage \
		discuss/Topic \
		newsfeed/Template \
		usermsg/MyMsgList \
		mail/ReceiveBox \

SCRIPT_TARGET_DIR = $(TARGET_DIR)/coffee
SCRIPT_LIST = usermsg/Usermsg \
		usermsg/MyMsgList \
		Common \
		hot/LoadHot \
		TransText \
		mail/ReceiveBox \
		dje.pager \

STYLE_TARGETS = $(foreach n, $(STYLE_LIST), $(STYLE_TARGET_DIR)/$n.css)
SCRIPT_TARGETS = $(foreach n, $(SCRIPT_LIST), $(SCRIPT_TARGET_DIR)/$n.js)
SCRIPT_COMPRESSED_TARGETS = $(foreach n, $(SCRIPT_LIST), $(SCRIPT_TARGET_DIR)/$n.min.js)

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
