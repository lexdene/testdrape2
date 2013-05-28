STYLE_COMPILER = lessc --yui-compress
SCRIPT_COMPILER = coffee

MKDIR = mkdir -p
COPY = cp -f

TARGET_DIR = ../data/static

STYLE_TARGETS = $(TARGET_DIR)/css/frame/Layout.css \
		$(TARGET_DIR)/css/jdmd_widget.css \
		$(TARGET_DIR)/css/discuss/List.css \
		$(TARGET_DIR)/css/userinfo/UserPanel.css \
		$(TARGET_DIR)/css/userinfo/MainPage.css \
		$(TARGET_DIR)/css/discuss/Topic.css \

SCRIPT_TARGETS = 

first : all

$(TARGET_DIR)/css/%.css : less/%.less Makefile
	$(MKDIR) $$(dirname "$@")
	$(STYLE_COMPILER) "$<" > "$@"

$(TARGET_DIR)/image/% : ../static/image/%
	$(MKDIR) $$(dirname "$@")
	$(COPY) "$<" "$@"

all: $(STYLE_TARGETS) $(SCRIPT_TARGETS) $(IMAGE_TARGETS)

$(STYLE_TARGETS) : less/common.less
