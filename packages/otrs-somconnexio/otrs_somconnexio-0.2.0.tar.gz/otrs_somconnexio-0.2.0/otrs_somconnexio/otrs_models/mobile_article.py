# coding: utf-8
from abstract_article import AbstractArticle


class MobileArticle(AbstractArticle):
    def __init__(self, service_type, eticom_contract):
        self.subject = "Sol·licitud {} {}".format(
            service_type,
            eticom_contract.id
        )
