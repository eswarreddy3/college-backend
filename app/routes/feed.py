import math
from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.models.feed import Post, PostLike, Comment, CommentLike
from app.utils.decorators import jwt_required

feed_bp = Blueprint('feed', __name__)

POSTS_PER_PAGE = 10


def _calc_reading_time(content: str) -> int:
    """Estimate reading time in minutes (avg 200 wpm)."""
    words = len(content.split())
    return max(1, math.ceil(words / 200))


# ── Posts ─────────────────────────────────────────────────────────────────────

@feed_bp.get('/posts')
@jwt_required
def list_posts():
    """List posts for the user's college, paginated. ?type=post|blog&page=1&draft=true"""
    user = g.current_user
    page = request.args.get('page', 1, type=int)
    post_type = request.args.get('type')       # 'post' | 'blog' | None (all)
    drafts_only = request.args.get('draft', 'false').lower() == 'true'

    query = Post.query.filter_by(college_id=user.college_id)

    if post_type:
        query = query.filter_by(type=post_type)

    if drafts_only:
        # Only own drafts
        query = query.filter_by(user_id=user.id, is_published=False)
    else:
        # Published only (or all own posts)
        query = query.filter(
            db.or_(Post.is_published == True, Post.user_id == user.id)
        )

    total = query.count()
    posts = query.order_by(Post.created_at.desc()) \
                 .offset((page - 1) * POSTS_PER_PAGE) \
                 .limit(POSTS_PER_PAGE).all()

    return jsonify({
        'posts': [p.to_dict(current_user_id=user.id) for p in posts],
        'total': total,
        'page': page,
        'pages': math.ceil(total / POSTS_PER_PAGE),
    }), 200


@feed_bp.post('/posts')
@jwt_required
def create_post():
    """Create a post or blog."""
    user = g.current_user
    data = request.get_json()

    post_type = data.get('type', 'post')
    content = (data.get('content') or '').strip()
    if not content:
        return jsonify({'error': 'Content is required'}), 400

    if post_type == 'blog' and not (data.get('title') or '').strip():
        return jsonify({'error': 'Title is required for blogs'}), 400

    post = Post(
        user_id=user.id,
        college_id=user.college_id,
        type=post_type,
        content=content,
        title=(data.get('title') or '').strip() or None,
        cover_image_url=data.get('cover_image_url'),
        tags=data.get('tags', []),
        is_published=data.get('is_published', True),
        reading_time=_calc_reading_time(content) if post_type == 'blog' else 0,
    )
    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_dict(current_user_id=user.id)), 201


@feed_bp.get('/posts/<int:post_id>')
@jwt_required
def get_post(post_id):
    """Get a single post with its comments."""
    user = g.current_user
    post = Post.query.filter_by(id=post_id, college_id=user.college_id).first()
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    data = post.to_dict(current_user_id=user.id)
    # top-level comments only (replies nested inside)
    top_level = [c for c in post.comments if c.parent_id is None]
    data['comments'] = [c.to_dict(current_user_id=user.id) for c in top_level]
    return jsonify(data), 200


@feed_bp.patch('/posts/<int:post_id>')
@jwt_required
def update_post(post_id):
    """Edit own post/blog (or publish a draft)."""
    user = g.current_user
    post = Post.query.filter_by(id=post_id, user_id=user.id).first()
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    data = request.get_json()
    if 'content' in data:
        post.content = data['content'].strip()
        if post.type == 'blog':
            post.reading_time = _calc_reading_time(post.content)
    if 'title' in data:
        post.title = data['title'].strip() or None
    if 'cover_image_url' in data:
        post.cover_image_url = data['cover_image_url']
    if 'tags' in data:
        post.tags = data['tags']
    if 'is_published' in data:
        post.is_published = data['is_published']

    db.session.commit()
    return jsonify(post.to_dict(current_user_id=user.id)), 200


@feed_bp.delete('/posts/<int:post_id>')
@jwt_required
def delete_post(post_id):
    """Delete own post."""
    user = g.current_user
    post = Post.query.filter_by(id=post_id, user_id=user.id).first()
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200


# ── Likes ─────────────────────────────────────────────────────────────────────

@feed_bp.post('/posts/<int:post_id>/like')
@jwt_required
def toggle_post_like(post_id):
    """Toggle like on a post."""
    user = g.current_user
    post = Post.query.filter_by(id=post_id, college_id=user.college_id).first()
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    existing = PostLike.query.filter_by(post_id=post_id, user_id=user.id).first()
    if existing:
        db.session.delete(existing)
        liked = False
    else:
        db.session.add(PostLike(post_id=post_id, user_id=user.id))
        liked = True

    db.session.commit()
    return jsonify({'liked': liked, 'like_count': post.like_count()}), 200


# ── Comments ──────────────────────────────────────────────────────────────────

@feed_bp.post('/posts/<int:post_id>/comments')
@jwt_required
def add_comment(post_id):
    """Add a top-level comment to a post."""
    user = g.current_user
    post = Post.query.filter_by(id=post_id, college_id=user.college_id).first()
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    content = (request.get_json().get('content') or '').strip()
    if not content:
        return jsonify({'error': 'Comment cannot be empty'}), 400

    comment = Comment(post_id=post_id, user_id=user.id, content=content)
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict(current_user_id=user.id)), 201


@feed_bp.post('/comments/<int:comment_id>/reply')
@jwt_required
def reply_comment(comment_id):
    """Reply to a comment."""
    user = g.current_user
    parent = Comment.query.get(comment_id)
    if not parent:
        return jsonify({'error': 'Comment not found'}), 404

    content = (request.get_json().get('content') or '').strip()
    if not content:
        return jsonify({'error': 'Reply cannot be empty'}), 400

    reply = Comment(
        post_id=parent.post_id,
        user_id=user.id,
        parent_id=comment_id,
        content=content,
    )
    db.session.add(reply)
    db.session.commit()
    return jsonify(reply.to_dict(current_user_id=user.id)), 201


@feed_bp.delete('/comments/<int:comment_id>')
@jwt_required
def delete_comment(comment_id):
    """Delete own comment."""
    user = g.current_user
    comment = Comment.query.filter_by(id=comment_id, user_id=user.id).first()
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200


@feed_bp.post('/comments/<int:comment_id>/like')
@jwt_required
def toggle_comment_like(comment_id):
    """Toggle like on a comment."""
    user = g.current_user
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    existing = CommentLike.query.filter_by(comment_id=comment_id, user_id=user.id).first()
    if existing:
        db.session.delete(existing)
        liked = False
    else:
        db.session.add(CommentLike(comment_id=comment_id, user_id=user.id))
        liked = True

    db.session.commit()
    return jsonify({'liked': liked, 'like_count': comment.like_count()}), 200
