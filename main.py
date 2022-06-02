from website import create_app

# sets up the app from the website package
app = create_app()

# will only run the app if not imported
if __name__ == '__main__':
    app.run(debug=True, port=8000)