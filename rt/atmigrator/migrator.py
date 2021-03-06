# -*- coding: utf-8 -*-


def makeFolderMigrator(context, src_type, dst_type, src_metatype, dst_metatype):
    """ generate a migrator for the given at-based folderish portal type """
    from Products.contentmigration.archetypes import InplaceATFolderMigrator

    class ATFolderMigrator(InplaceATFolderMigrator):
        src_portal_type = src_type
        src_meta_type = src_metatype
        dst_portal_type = dst_type
        dst_meta_type = dst_metatype

    return ATFolderMigrator


def makeContentMigrator(context, src_type, dst_type, src_metatype, dst_metatype):
    """ generate a migrator for the given at-based portal type """
    from Products.contentmigration.archetypes import InplaceATItemMigrator

    class ATContentMigrator(InplaceATItemMigrator):
        src_portal_type = src_type
        src_meta_type = src_metatype
        dst_portal_type = dst_type
        dst_meta_type = dst_metatype

    return ATContentMigrator


def migrateContents(context, src_type, dst_type, src_metatype, dst_metatype, query={}):
    from Products.contentmigration.walker import CustomQueryWalker
    #BBB: i can't find a better way to know if a given portal_type is folderish or not
    is_folderish = False
    temp_obj = context.restrictedTraverse('portal_factory/%s/tmp_id' % src_type)
    if temp_obj:
        plone_view = temp_obj.restrictedTraverse('@@plone')
        if plone_view.isStructuralFolder():
            is_folderish = True
    portal_types = context.portal_types
    src_infos = portal_types.getTypeInfo(src_type)
    dst_infos = portal_types.getTypeInfo(dst_type)
    if is_folderish:
        migrator = makeFolderMigrator(context,
                                     src_type,
                                     dst_type,
                                     src_metatype,
                                     dst_metatype)
    else:
        migrator = makeContentMigrator(context,
                                      src_type,
                                      dst_type,
                                      src_metatype,
                                      dst_metatype)
    if migrator:
        if not src_metatype:
            src_metatype = src_infos.content_meta_type
        if not dst_metatype:
            dst_metatype = dst_infos.content_meta_type
        migrator.src_meta_type = src_metatype
        migrator.dst_meta_type = dst_metatype
        walker = CustomQueryWalker(context, migrator,
                                  src_portal_type=src_type,
                                  dst_portal_type=dst_type,
                                  src_meta_type=src_metatype,
                                  dst_meta_type=dst_metatype,
                                  query=query,
                                  use_savepoint=True)
        walker.go()
        walk_infos = {'error': walker.errors,
                      'msg': walker.getOutput().splitlines(),
                      'counter': walker.counter}
        return walk_infos
