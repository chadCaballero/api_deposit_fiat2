from .controllers import (countries_per_money, payments_per_moneycountry, collectors_per_moneyCountryPayment,
                          commissions_per_moneycountrypaymentcollector, payment_instructions_per_moneycountry,
                          payment_instructions_per_moneycountrypaymentcollector, countries, collectors,
                          payments, payment_instructions_per_moneycountrypayment,
                          payment_instructions_per_moneycountrycollector)
from apps.public import endpoints_publics

# Listar los Países --ok
endpoints_publics.add_url_rule('/countries', view_func=countries, methods=["GET"])

# Listar Países por moneda  --ok
endpoints_publics.add_url_rule('/countries/moneys/<int:id_money>', view_func=countries_per_money, methods=["GET"])

# Listar todos los Métodos de Pago  --ok
endpoints_publics.add_url_rule('/payments',
                               view_func=payments, methods=["GET"])

# Listar Métodos de Pago por nomeda y pais  --ok
endpoints_publics.add_url_rule('/payments/moneys/<int:id_money>/countries/<int:id_country>',
                               view_func=payments_per_moneycountry, methods=["GET"])

# Listar todos los Recaudadores --ok
endpoints_publics.add_url_rule('/collectors',
                               view_func=collectors, methods=["GET"])

# Listar Recaudadores por moneda, pais, metodo de pago  --ok
endpoints_publics.add_url_rule('/collectors/moneys/<int:id_money>/countries/<int:id_country>/payments/<int:id_payment>',
                               view_func=collectors_per_moneyCountryPayment, methods=["GET"])

# Obtener Comisiones por moneda, pais, metodo de pago, recaudador   --ok
endpoints_publics.add_url_rule(
    '/commissions/moneys/<int:id_money>/countries/<int:id_country>/payments/<int:id_payment>/collectors/<int:id_collect>',
    view_func=commissions_per_moneycountrypaymentcollector, methods=["GET"])

# Obtener Datos Bancarios/Instrucciones de Pagos por moneda y pais  -- +0-
endpoints_publics.add_url_rule(
    '/payment-instructions/moneys/<int:id_money>/countries/<int:id_country>/lang/<int:id_lang>',
    view_func=payment_instructions_per_moneycountry, methods=["GET"])

# Obtener Datos Bancarios/Instrucciones de Pagos por moneda, pais, payment y language
endpoints_publics.add_url_rule(
    '/payment-instructions/moneys/<int:id_money>/countries/<int:id_country>/payments/<int:id_payment>/lang/<int:id_lang>',
    view_func=payment_instructions_per_moneycountrypayment, methods=["GET"])

# Obtener Datos Bancarios/Instrucciones de Pagos por moneda, pais, collector and language   -- +0-
endpoints_publics.add_url_rule(
    '/payment-instructions/moneys/<int:id_money>/countries/<int:id_country>/collectors/<int:id_collect>/lang/<int:id_lang>',
    view_func=payment_instructions_per_moneycountrycollector, methods=["GET"])

# Obtener Datos Bancarios/Instrucciones de Pagos por moneda, pais, payment, collector and language  -- +0-
endpoints_publics.add_url_rule(
    '/payment-instructions/moneys/<int:id_money>/countries/<int:id_country>/payments/<int:id_payment>/collectors/<int:id_collect>/lang/<int:id_lang>',
    view_func=payment_instructions_per_moneycountrypaymentcollector, methods=["GET"])
