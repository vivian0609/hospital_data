mkdir -p ~/.streamlit/

touch ~/.streamlit/config.toml
touch ~/.streamlit/credentials.toml

echo "\
[general]\n\
email = \"yanqiliang609@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
port = 8501\n\
" > ~/.streamlit/config.toml