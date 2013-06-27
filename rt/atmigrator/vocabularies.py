# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName


class MetaTypesVocabulary(object):
    """
    Vocabulary factory for available meta_types in catalog.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        pc = getToolByName(context, 'portal_catalog')
        meta_types = list(pc.uniqueValuesFor('meta_type'))
        meta_types.sort()
        meta_types = [SimpleTerm(i, i, i) for i in meta_types]
        return SimpleVocabulary(meta_types)

MetaTypesVocabularyFactory = MetaTypesVocabulary()
