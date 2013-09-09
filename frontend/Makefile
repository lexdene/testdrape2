STYLE_COMPILER = lessc --yui-compress
MKDIR = mkdir -p

TARGET_DIR = ../data/static

STYLE_TARGET_DIR = $(TARGET_DIR)/css
STYLE_LIST = \
		discuss2/filter_topic \
		discuss2/post_topic \
		discuss/List \
		discuss/Topic \
		frame/Layout \
		jdmd_widget \
		mail/ReceiveBox \
		newsfeed/Template \
		tag/tag_list_page \
		userinfo/MainPage \
		userinfo/UserPanel \
		usermsg/MyMsgList \

SCRIPT_TARGET_DIR = $(TARGET_DIR)/coffee
SCRIPT_LIST = \
		Common \
		discuss2/filter_topic \
		discuss2/post_topic \
		dje/dje.ajax_form \
		dje/dje.mask \
		dje/dje.pager \
		dje/dje.util \
		frame/Layout \
		frame/notice \
		hot/LoadHot \
		mail/ReceiveBox \
		mail/Write \
		tag/tag_list_page \
		TransText \
		userinfo/MainPage \
		userinfo/UserPanel \
		usermsg/MyMsgList \
		usermsg/Usermsg \

STYLE_TARGETS = $(foreach n, $(STYLE_LIST), $(STYLE_TARGET_DIR)/$n.css)
SCRIPT_TARGETS = $(foreach n, $(SCRIPT_LIST), $(SCRIPT_TARGET_DIR)/$n.js)
SCRIPT_COMPRESSED_TARGETS = $(foreach n, $(SCRIPT_LIST), $(SCRIPT_TARGET_DIR)/$n.min.js)

first : all

$(STYLE_TARGET_DIR)/%.css : less/%.less Makefile
	$(MKDIR) $$(dirname "$@")
	$(STYLE_COMPILER) "$<" > "$@"

$(SCRIPT_TARGET_DIR)/%.js : coffee/%.coffee Makefile
	$(MKDIR) $$(dirname "$@")
	coffee -b -c -o $$(dirname "$@") "$<"

$(SCRIPT_TARGET_DIR)/%.min.js : $(SCRIPT_TARGET_DIR)/%.js
	uglifyjs -o "$@" "$<"

all: $(STYLE_TARGETS) $(SCRIPT_TARGETS) $(SCRIPT_COMPRESSED_TARGETS)

$(STYLE_TARGETS) : less/common.less
