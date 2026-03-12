from datetime import datetime, timezone
from app.extensions import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)

    type = db.Column(db.Enum('post', 'blog'), nullable=False, default='post')

    # Blog-only fields
    title = db.Column(db.String(255), nullable=True)
    cover_image_url = db.Column(db.String(512), nullable=True)
    reading_time = db.Column(db.Integer, default=0)   # minutes
    is_published = db.Column(db.Boolean, default=True) # False = draft (blogs only)

    # Common fields
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.JSON, default=list)            # ['placement', 'event', ...]

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    author = db.relationship('User', backref='posts', lazy='joined')
    comments = db.relationship('Comment', backref='post', lazy=True,
                               cascade='all, delete-orphan',
                               order_by='Comment.created_at')
    likes = db.relationship('PostLike', backref='post', lazy=True,
                            cascade='all, delete-orphan')

    def like_count(self):
        return len(self.likes)

    def comment_count(self):
        return len(self.comments)

    def to_dict(self, current_user_id=None):
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'content': self.content,
            'cover_image_url': self.cover_image_url,
            'reading_time': self.reading_time,
            'is_published': self.is_published,
            'tags': self.tags or [],
            'like_count': self.like_count(),
            'comment_count': self.comment_count(),
            'liked_by_me': any(l.user_id == current_user_id for l in self.likes) if current_user_id else False,
            'author': {
                'id': self.author.id,
                'name': self.author.name,
                'branch': self.author.branch,
                'passout_year': self.author.passout_year,
            },
            'created_at': self.created_at.replace(tzinfo=timezone.utc).isoformat(),
            'updated_at': self.updated_at.replace(tzinfo=timezone.utc).isoformat(),
        }


class PostLike(db.Model):
    __tablename__ = 'post_likes'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='uq_post_like'),)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)  # nested replies
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    author = db.relationship('User', backref='comments', lazy='joined')
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]),
                              lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('CommentLike', backref='comment', lazy=True,
                            cascade='all, delete-orphan')

    def like_count(self):
        return len(self.likes)

    def to_dict(self, current_user_id=None):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'parent_id': self.parent_id,
            'content': self.content,
            'like_count': self.like_count(),
            'liked_by_me': any(l.user_id == current_user_id for l in self.likes) if current_user_id else False,
            'replies': [r.to_dict(current_user_id) for r in self.replies],
            'author': {
                'id': self.author.id,
                'name': self.author.name,
                'branch': self.author.branch,
            },
            'created_at': self.created_at.replace(tzinfo=timezone.utc).isoformat(),
        }


class CommentLike(db.Model):
    __tablename__ = 'comment_likes'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint('comment_id', 'user_id', name='uq_comment_like'),)
