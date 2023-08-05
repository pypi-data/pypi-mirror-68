# coding: utf-8
import unittest
from mock import Mock

from pyotrs.lib import Article
from otrs_somconnexio.otrs_models.coverage_article import CoverageArticle


class CoverageArticleTestCase(unittest.TestCase):

    def setUp(self):
        self.coverage_ticket = Mock(spec=['getattr'])

        def getattr_side_effect(name):
            if name == "tipusVia":
                return "street"

        self.coverage_ticket.getattr.side_effect = getattr_side_effect

    def test_build(self):
        coverage_article = CoverageArticle(self.coverage_ticket).build()

        self.assertIsInstance(coverage_article, Article)

    def test_build_Subject(self):
        coverage_article = CoverageArticle(self.coverage_ticket).build()

        self.assertEqual(coverage_article.field_get("Subject"), "Sol·licitud cobertura")

    def test_build_Body(self):
        coverage_article = CoverageArticle(self.coverage_ticket).build()

        self.assertEqual(coverage_article.field_get("Body"), "tipusVia: street\n")

    def test_build_ContentType(self):
        coverage_article = CoverageArticle(self.coverage_ticket).build()

        self.assertEqual(coverage_article.field_get("ContentType"), "text/plain; charset=utf8")
