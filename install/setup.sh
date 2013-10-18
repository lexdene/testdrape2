touch app/config/distribution.py
cat > app/config/distribution.py <<EOF
LIBCDN = '/libs'
TEMPLATE_DIR = 'data/compiled/html'
EOF

mkdir -p data
chmod a+w data

cd frontend
make

# libs
cd ~/workspace/webpage/
mkdir -p libs
cd libs
if ! [ -d jquery ];then
    mkdir -p jquery/1.9.1
    cd jquery/1.9.1
    wget http://code.jquery.com/jquery-1.9.1.min.js -O jquery.min.js
    cd -
fi
if ! [ -d underscore ];then
    mkdir -p underscore/1.5.2/
    cd underscore/1.5.2/
    wget http://underscorejs.org/underscore-min.js
    cd -
fi
if ! [ -d showdown ];then
    git clone https://github.com/coreyti/showdown.git
fi
if ! [ -d emoji ];then
    git clone https://github.com/arvida/emoji-cheat-sheet.com.git emoji
fi
