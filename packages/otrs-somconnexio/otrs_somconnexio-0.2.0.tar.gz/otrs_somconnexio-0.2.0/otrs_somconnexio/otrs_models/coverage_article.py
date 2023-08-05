# coding: utf-8
from pyotrs.lib import Article


class CoverageArticle:
    """
    This entity gets created from a CoverageTicket.
    """
    dynamic_fields_names = (
        "tipusVia", "nomVia", "numero", "bloc", "portal", "pis", "escala", "porta",
        "poblacioServei", "provinciaServei", "CPservei", "altresCobertura", "coberturaADSL",
        "coberturaFibraMM", "coberturaFibraVdf", "IDhogar"
    )

    def __init__(self, ticket):
        self.ticket = ticket

    def build(self):
        return Article({
            "Subject": "Sol·licitud cobertura",
            "Body": self._body(),
            "ContentType": "text/plain; charset=utf8"
        })

    def _body(self):
        body = ""
        for df_name in self.dynamic_fields_names:
            df_value = self.ticket.getattr(df_name)
            if df_value:
                body = u"{}{}: {}\n".format(body, df_name, df_value)
        return body
