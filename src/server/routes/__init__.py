def register_routes(app):
  from .login import login_bp
  from .signup import signup_bp

  api_url_prefix = "/api"
  app.register_blueprint(login_bp, url_prefix=api_url_prefix)
  app.register_blueprint(signup_bp, url_prefix=api_url_prefix)