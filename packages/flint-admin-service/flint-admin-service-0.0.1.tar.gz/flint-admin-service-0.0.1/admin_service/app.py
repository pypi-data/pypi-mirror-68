from admin_service.admin import create_app
from admin_service.login import authentication


app = create_app()
app.register_authentication(authentication)

if __name__ == "__main__":
    app.start()
