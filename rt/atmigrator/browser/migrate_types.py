# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from rt.atmigrator import atmigratorMessageFactory as _
from rt.atmigrator import logger
from rt.atmigrator.migrator import migrateContents
from zope.component import getUtility
from zope.app.schema.vocabulary import IVocabularyFactory


class MigrateView(BrowserView):
    """
    A view that allows to migrate a portal-type into another
    """
    def __call__(self):
        """
        Check values in the request, and make the right action
        """
        if 'form.button.Cancel' in self.request.form.keys():
            return self.doReturn(_("migration_error_cancel",
                                   defaul=u"Migration canceled."), 'info')
        if not 'form.button.Migrate' in self.request.form.keys():
            return self.index()
        if not self.request.form.get('src_type', '') and not self.request.form.get('dst_type', ''):
            return self.doReturn(_("migration_error_validation",
                                   defaul=u"You need to fill both required fields."), 'error')
        migration = self.doMigration()
        if migration:
            return self.doReturn(_("migration_done_msg",
                                 default=u"Migration done."), 'info')
        else:
            return self.doReturn(_("migration_error_msg",
                                   defaul=u"Errors in migration process. See the log for more infos."), 'error')

    def doMigration(self):
        """
        handle migration from a portal_type to anther, and log all outputs given
        """
        #BBB: i can't find a better way to know if a given portal_type is folderish or not
        is_folderish = False
        src_type = self.request.form.get('src_type', '')
        dst_type = self.request.form.get('dst_type', '')
        temp_obj = self.context.restrictedTraverse('portal_factory/%s/tmp_id' % src_type)
        if temp_obj:
            plone_view = temp_obj.restrictedTraverse('@@plone')
            if plone_view.isStructuralFolder():
                is_folderish = True
        logger.info("*********** Migration start ***********")
        output = migrateContents(self.context, src_type, dst_type, is_folderish)
        pu = getToolByName(self.context, "plone_utils")
        pu.addPortalMessage("Migration from %s to %s: found %s items." % (src_type,
                                                                          dst_type,
                                                                          output.get('counter', '')), 'info')
        for m in output.get('msg', []):
            logger.info(m)
        logger.info("*********** Migration done ***********")
        if output.get('error', []):
            for error in output.get('error', []):
                pu.addPortalMessage(error.get('msg', ''), 'error')
                return False
        return True

    def getTypesList(self):
        """
        Return an user friendly list of portal_types
        """
        utility = getUtility(IVocabularyFactory,
                             "plone.app.vocabularies.UserFriendlyTypes")
        if utility:
            return utility(self.context)._terms

    def doReturn(self, message, type):
        """
        Add a portal message and make a redirect
        """
        pu = getToolByName(self.context, "plone_utils")
        pu.addPortalMessage(message, type=type)
        return_url = "%s/view" % self.context.absolute_url()
        self.request.RESPONSE.redirect(return_url)
