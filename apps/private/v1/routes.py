from apps.private import endpoints_privates
from .controllers import (deposit_per_platform, deposits_post,
                          deposit_per_platformmoneycountrypaymentcollectorstatus, asoc_country_with_money,
                          asoc_collector_with_country, collectors, asoc_payment_with_collector,
                          payments, companies, bank_data, languages, instructions, deposits_put)

# (1) Listar solicitud(es) de Depósito por plataforma
endpoints_privates.add_url_rule('/deposits/platforms/<string:platform>', view_func=deposit_per_platform,
                                methods=["GET"])

# (2) Listar solicitud(es) de Depósito por plataforma, moneda, pais, metodo de pago, recaudador y estado
endpoints_privates.add_url_rule(
    '/deposits/platforms/<string:platform>/moneys/<int:id_money>/countries/<int:id_country>/payments/<int:id_payment>/collectors/<int:id_collect>/<int:status>',
    view_func=deposit_per_platformmoneycountrypaymentcollectorstatus, methods=["GET"])

# (3) Crear, aceptar, cancelar, rechazar Depósito(s)
endpoints_privates.add_url_rule('/deposits', view_func=deposits_post, methods=["POST"])

# (3.1) aceptar, cancelar, rechazar Depósito(s)
endpoints_privates.add_url_rule('/deposits', view_func=deposits_put, methods=["PUT"])

# (4) Crear asociación país por moneda
endpoints_privates.add_url_rule('/countries/<int:id_country>/money/<int:id_money>', view_func=asoc_country_with_money,
                                methods=["POST", "PUT"])

# (5) Deshasociar pais de moneda
# endpoints_privates.add_url_rule('/countries/<int:id_country>', view_func=countries, methods=["PUT"])

# (6) Crear asociación recaudador con país
endpoints_privates.add_url_rule('/collectors/<int:id_collect>/countries/<int:id_country>',
                                view_func=asoc_collector_with_country,
                                methods=["POST"])

# (7) Deshabilitar recaudador
endpoints_privates.add_url_rule('/collectors/<int:id_collect>', view_func=collectors, methods=["PUT"])

# (8) Crear asociación metodo de pago con recaudador
endpoints_privates.add_url_rule('/payments/<int:id_payment>/collectors/<int:id_collect>',
                                view_func=asoc_payment_with_collector,
                                methods=["POST"])

# (9) Deshabilitar método de pago
endpoints_privates.add_url_rule('/payments/<int:id_payment>', view_func=payments, methods=["PUT"])

# (10) listar compañias o crear
endpoints_privates.add_url_rule('/companies', view_func=companies, methods=["GET", "POST"])

# (11) listar o actualizar compañia
endpoints_privates.add_url_rule('/companies/<int:id_company>', view_func=companies, methods=["GET", "PUT"])

# (12) listar o agregar datos bancarios
endpoints_privates.add_url_rule('/bank-data', view_func=bank_data, methods=["GET", "POST"])

# (13) editar datos bancarios
endpoints_privates.add_url_rule('/bank-data/<int:bank_data>', view_func=bank_data, methods=["GET", "PUT"])

# (14) listar lenguajes
endpoints_privates.add_url_rule('/languages', view_func=languages, methods=["GET"])

# (15) listar o agregar instrucciones de Pagos
endpoints_privates.add_url_rule('/payment-instructions', view_func=instructions, methods=["GET", "POST"])

# (16) editar instrucciones de Pagos
endpoints_privates.add_url_rule('/payment-instructions/<int:id_instruction>', view_func=instructions, methods=["PUT"])
