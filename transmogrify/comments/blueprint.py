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
            pathkeys = defaultKeys(options['blueprint'], name, 'path')
        self.pathkey = Matcher(*pathkeys)
        self.comment_type = options.get("comment-type", "plone")
        self.enabled = True
        if self.comment_type == "plone.app.discussion" and not PAD_INSTALLED:
            # TODO: log a note
            self.enabled = False


    def __iter__(self):
        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]
            # item doesn't exist or the type of comment cannot be
            # created
            if not self.enabled or not pathkey:
                yield item
                continue

            path = item[pathkey]

            obj = self.context.unrestrictedTraverse(path.lstrip('/'), None)
            # path doesn't exist
            if obj is None:
                yield item
                continue

            # TODO: check to see if the object supports commenting...
            comments = item.get('_comments', [])
            for comment in comments:
                title = comment.get('title', '')
                text = comment.get('text', '')
                creator = comment.get('author.name', '')
                creation_date = comment.get('published', '')
                modification_date = comment.get('updated', '')
                if self.comment_type == "plone.app.discussion":
                    conversation = IConversation(obj)
                    # create a reply object
                    comment = CommentFactory()
                    comment.title = title
                    comment.text = text
                    comment.creator = creator
                    # TODO: check if the date is a datetime instance
                    comment.creation_date = creation_date
                    comment.modification_date = modification_date
                    conversation.addComment(comment)
                    # TODO: fire events
                if self.comment_type == "plone":
                    # TODO: create default plone content
                    pass
            yield item
