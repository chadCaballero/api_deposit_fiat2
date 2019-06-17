from .controllers import login, refresh, sworn_declarations
from apps.auth import auth_server


auth_server.add_url_rule('/login', view_func=login, methods=["POST"])
auth_server.add_url_rule('/refresh', view_func=refresh, methods=["POST"])
auth_server.add_url_rule('/sworn_declarations', view_func=sworn_declarations, methods=["POST"])

