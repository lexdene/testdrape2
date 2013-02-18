var request = null;
var cache = {};

function previous() {
  if (request) {
    return false;
  }

  var select = document.getElementById('themeSelect');
  var selectedIndex = select.selectedIndex;
  var length = select.length;
  if (selectedIndex === 0) {
    select.selectedIndex = length - 1;
  }
  else {
    select.selectedIndex = selectedIndex - 1;
  }
  loadStyle();
  return false;
}

function next() {
  if (request) {
    return false;
  }

  var select = document.getElementById('themeSelect');
  var selectedIndex = select.selectedIndex;
  var length = select.length;
  if (selectedIndex === length - 1) {
    select.selectedIndex = 0;
  }
  else {
    select.selectedIndex = selectedIndex + 1;
  }
  loadStyle();
  return false;
}

function setStyle(text) {
  var style = document.getElementById('style_sh');
  if (style.styleSheet) {
    style.styleSheet.cssText = text;
  }
  else {
    while (style.hasChildNodes()) {
      style.removeChild(style.firstChild);
    }
    style.appendChild(document.createTextNode(text));
  }
}

function handler() {
  if (request.readyState === 4) {
    try {
      if (request.status === 0 || request.status === 200) {
        setStyle(request.responseText);
        var select = document.getElementById('themeSelect');
        var value = select.options[select.selectedIndex].innerHTML;
        cache[value] = request.responseText;
      }
    }
    finally {
      request = null;

      var select = document.getElementById('themeSelect');
      select.disabled = false;

      var throbber = document.getElementById('throbberImg');
      throbber.style.display = 'none';
    }
  }
}

function loadStyle() {
  var select = document.getElementById('themeSelect');
  var value = select.options[select.selectedIndex].innerHTML;

  var cachedText = cache[value];
  if (cachedText) {
    setStyle(cachedText);
    return;
  }

  select.disabled = true;

  var throbber = document.getElementById('throbberImg');
  throbber.style.display = 'inline';

  request = sh_getXMLHttpRequest();
  var url = '/static/shjs-0.6/css/sh_' + value + '.css';
  request.open('GET', url, true);
  request.onreadystatechange = handler;
  request.send(null);
}

function body_load() {
  if (/Konqueror/.test(navigator.userAgent)) {
    var previous = document.getElementById('previous');
    previous.innerHTML = '&lt;';
    var next = document.getElementById('next');
    next.innerHTML = '&gt;';
  }

  loadStyle();
  sh_highlightDocument();

  // Opera needs this, or else it truncates the pre
  var pre = document.getElementById('codePre');
  var width = pre.scrollWidth + 'px';
  pre.style.width = width;

  // freeze the width of the caption
  var caption = document.getElementById('caption');
  caption.style.width = width;
}
