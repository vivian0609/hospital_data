mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"yanqiliang609@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
" > ~/.streamlit/config.toml

var port = process.env.PORT || 8000