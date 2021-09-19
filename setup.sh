mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"yanqiliang609@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = process.env.Port\n\
" > ~/.streamlit/config.toml