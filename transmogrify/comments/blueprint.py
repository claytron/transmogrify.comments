from datetime import datetime
from zope.interface import classProvides
from zope.interface import implements
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import Matcher
from collective.transmogrifier.utils import defaultKeys
try:
    from plone.app.discussion.comment import CommentFactory
    from plone.app.discussion.interfaces import IConversation
    PAD_INSTALLED = True
except ImportError:
    PAD_INSTALLED = False


class CommentsSection(object):
    """A blueprint for importing comments into plone
    """
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context
        if 'path-key' in options:
            pathkeys = options['path-key'].splitlines()
        else:
            pathkeys = defaultKeys(options['blueprint'], name, 'parent_path')
        self.pathkey = Matcher(*pathkeys)
        if 'comment-type-key' in options:
            comment_type_keys = options['comment-type-key'].splitlines()
        else:
            comment_type_keys = defaultKeys(
                options['blueprint'], name, 'comment_type')
        self.comment_type_key = Matcher(*comment_type_keys)
        self.date_format = options.get('date-format', '%Y/%m/%d %H:%M:%S')

    def __iter__(self):
        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]
            typekey = self.comment_type_key(*item.keys())[0]
            # item doesn't exist or the type of comment cannot be
            # created
            if not pathkey or not typekey:
                # TODO: log a note
                yield item
                continue

            comment_type = item[typekey]
            if comment_type == "plone.app.discussion" and not PAD_INSTALLED:
                # TODO: log a note
                yield item
                continue

            path = item[pathkey]
            obj = self.context.unrestrictedTraverse(path.lstrip('/'), None)
            # path doesn't exist
            if obj is None:
                yield item
                continue

            # TODO: check to see if the object supports commenting...
            title = item.get('title', '')
            text = item.get('text', '')
            creator = item.get('author_name', '')
            creation_date = item.get('published', '')
            modification_date = item.get('updated', '')
            if comment_type == "plone.app.discussion":
                conversation = IConversation(obj)
                # create a reply object
                comment = CommentFactory()
                comment.title = title
                comment.text = text
                comment.creator = creator
                # TODO: strptime is is python2.5+, need python2.4 solution
                if not isinstance(creation_date, datetime):
                    creation_date = datetime.strptime(
                        creation_date,
                        self.date_format)
                comment.creation_date = creation_date
                if not isinstance(modification_date, datetime):
                    modification_date = datetime.strptime(
                        modification_date,
                        self.date_format)
                comment.modification_date = modification_date
                conversation.addComment(comment)
                # TODO: fire events
            if comment_type == "plone":
                # TODO: create default plone content
                pass
            yield item
