import re
import time
import requests as http_req
from datetime import datetime, timezone, timedelta

# In-memory cache: username -> (data_dict, fetched_at_epoch)
_IG_CACHE: dict = {}
_IG_CACHE_TTL = 3600  # re-fetch after 1 hour
from flask import Blueprint, request, jsonify, g, Response
from app.extensions import db
from app.models.user import User
from app.models.activity_log import ActivityLog
from app.models.coding_problem import CodingSubmission
from app.models.streak import UserStreak
from app.utils.decorators import role_required, jwt_required
from app.utils.helpers import hash_password, verify_password

student_bp = Blueprint('student', __name__)


@student_bp.get('/ig-image')
def ig_image_proxy():
    """Proxy Instagram CDN images with correct Referer so they load in the browser."""
    url = request.args.get('url', '')
    if not url or ('cdninstagram.com' not in url and 'fbcdn.net' not in url):
        return '', 400
    try:
        resp = http_req.get(url, headers={
            'Referer': 'https://www.instagram.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }, timeout=10, stream=True)
        content_type = resp.headers.get('Content-Type', 'image/jpeg')
        return Response(resp.content, status=resp.status_code, content_type=content_type,
                        headers={'Cache-Control': 'public, max-age=86400'})
    except Exception:
        return '', 502


@student_bp.get('/profile')
@role_required('student', 'college_admin', 'super_admin')
def get_profile():
    return jsonify(g.current_user.to_dict()), 200


@student_bp.patch('/profile')
@role_required('student', 'college_admin', 'super_admin')
def update_profile():
    user = g.current_user
    data = request.get_json(silent=True) or {}

    updatable = ['name', 'phone', 'linkedin', 'github', 'branch', 'section',
                 'roll_number', 'passout_year',
                 'email_notifications', 'assignment_reminders', 'leaderboard_updates']

    for field in updatable:
        if field in data:
            setattr(user, field, data[field])

    if 'current_password' in data and 'new_password' in data:
        if not verify_password(data['current_password'], user.password_hash):
            return jsonify({'error': 'Current password is incorrect'}), 400
        if len(data['new_password']) < 8:
            return jsonify({'error': 'New password must be at least 8 characters'}), 400
        user.password_hash = hash_password(data['new_password'])

    db.session.commit()
    return jsonify({'message': 'Profile updated', 'user': user.to_dict()}), 200


@student_bp.get('/dashboard')
@role_required('student')
def dashboard():
    user = g.current_user

    # College rank by points
    rank = (
        User.query
        .filter_by(college_id=user.college_id, role='student')
        .filter(User.points > user.points)
        .count()
    ) + 1

    total_in_college = User.query.filter_by(college_id=user.college_id, role='student').count()

    # Solved problems count
    solved_count = (
        db.session.query(CodingSubmission.problem_id)
        .filter_by(user_id=user.id, status='accepted')
        .distinct()
        .count()
    )

    # Recent activity (last 10)
    recent_activity = (
        ActivityLog.query
        .filter_by(user_id=user.id)
        .order_by(ActivityLog.created_at.desc())
        .limit(10)
        .all()
    )

    # Streak from user_streaks table
    streak_row = UserStreak.query.filter_by(user_id=user.id).first()
    current_streak = streak_row.current_streak if streak_row else 0
    longest_streak = streak_row.longest_streak if streak_row else 0

    # Active days this month (for streak calendar)
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_logs = (
        ActivityLog.query
        .filter(ActivityLog.user_id == user.id, ActivityLog.created_at >= month_start)
        .all()
    )
    active_days = sorted(set(log.created_at.day for log in monthly_logs))

    return jsonify({
        'points': user.points,
        'streak': current_streak,
        'longest_streak': longest_streak,
        'rank': rank,
        'total_in_college': total_in_college,
        'solved_count': solved_count,
        'active_days': active_days,
        'recent_activity': [a.to_dict() for a in recent_activity],
    }), 200


@student_bp.get('/leaderboard')
@role_required('student')
def leaderboard():
    user = g.current_user
    scope = request.args.get('scope', 'college')  # college | branch | section

    query = User.query.filter_by(college_id=user.college_id, role='student')
    if scope == 'branch' and user.branch:
        query = query.filter_by(branch=user.branch)
    elif scope == 'section' and user.section:
        query = query.filter_by(branch=user.branch, section=user.section)

    students = query.order_by(User.points.desc()).all()

    result = []
    for i, s in enumerate(students):
        result.append({
            'rank': i + 1,
            'id': s.id,
            'name': s.name,
            'branch': s.branch,
            'section': s.section,
            'points': s.points,
            'streak': s.streak,
            'is_current_user': s.id == user.id,
        })

    return jsonify(result), 200


def _fetch_instagram_posts(url, college=None):
    """Fetch recent posts. Returns cached list when Instagram rate-limits."""
    cached = None
    try:
        m = re.search(r'instagram\.com/([^/?#\s]+)', url)
        if not m:
            return []
        username = m.group(1).strip('/')

        # In-memory cache (fresh)
        entry = _IG_CACHE.get(username)
        if entry and (time.time() - entry[1]) < _IG_CACHE_TTL:
            return entry[0]
        cached = entry[0] if entry else None

        resp = http_req.get(
            f'https://i.instagram.com/api/v1/users/web_profile_info/?username={username}',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                'x-ig-app-id': '936619743392459',
                'Accept': 'application/json',
                'Referer': 'https://www.instagram.com/',
            },
            timeout=8,
        )
        if resp.status_code != 200:
            if cached is not None:
                return cached
            if college and college.instagram_cache:
                return college.instagram_cache
            return []

        data = resp.json()
        user = data.get('data', {}).get('user', {})
        edges = user.get('edge_owner_to_timeline_media', {}).get('edges', [])
        posts = []
        for edge in edges[:12]:
            node = edge.get('node', {})
            caption_edges = node.get('edge_media_to_caption', {}).get('edges', [])
            caption = caption_edges[0]['node']['text'] if caption_edges else ''
            shortcode = node.get('shortcode', '')
            posts.append({
                'shortcode': shortcode,
                'url': f'https://www.instagram.com/p/{shortcode}/',
                'thumbnail': node.get('thumbnail_src') or node.get('display_url', ''),
                'caption': caption[:140],
                'likes': node.get('edge_liked_by', {}).get('count', 0),
                'is_video': node.get('is_video', False),
                'timestamp': node.get('taken_at_timestamp', 0),
            })

        _IG_CACHE[username] = (posts, time.time())
        if college:
            college.instagram_cache = posts
            college.instagram_cache_at = datetime.utcnow()
            db.session.commit()
        return posts
    except Exception:
        if cached is not None:
            return cached
        if college and college.instagram_cache:
            return college.instagram_cache
        return []


def _fetch_linkedin_posts(url):
    """
    LinkedIn blocks all unauthenticated scraping. We extract the profile handle
    and return metadata only — the frontend links directly to the profile.
    """
    try:
        m = re.search(r'linkedin\.com/(in|company|school)/([^/?#\s]+)', url)
        if not m:
            return None
        kind = m.group(1)   # 'in' | 'company' | 'school'
        handle = m.group(2).strip('/')
        return {'handle': handle, 'kind': kind, 'url': url}
    except Exception:
        return None


@student_bp.get('/college-social-posts')
@role_required('student', 'college_admin', 'super_admin')
def get_college_social_posts():
    college = g.current_user.college
    if not college:
        return jsonify({'instagram': None, 'linkedin': None}), 200

    instagram_data = None
    linkedin_info = None

    if college.instagram_url:
        instagram_data = _fetch_instagram_posts(college.instagram_url, college)

    if college.linkedin_url:
        linkedin_info = _fetch_linkedin_posts(college.linkedin_url)

    return jsonify({'instagram': instagram_data, 'linkedin': linkedin_info}), 200


@student_bp.get('/college-info')
@role_required('student', 'college_admin', 'super_admin')
def get_college_info():
    user = g.current_user
    college = user.college
    if not college:
        return jsonify({}), 200
    return jsonify({
        'id': college.id,
        'name': college.name,
        'location': college.location,
        'linkedin_url': college.linkedin_url,
        'linkedin_post_embeds': college.linkedin_post_embeds or [],
        'instagram_url': college.instagram_url,
        'instagram_post_embeds': college.instagram_post_embeds or [],
    }), 200


@student_bp.get('/resume')
@role_required('student', 'college_admin', 'super_admin')
def get_resume():
    return jsonify({'resume_data': g.current_user.resume_data or {}}), 200


@student_bp.put('/resume')
@role_required('student', 'college_admin', 'super_admin')
def save_resume():
    data = request.get_json(silent=True) or {}
    g.current_user.resume_data = data
    db.session.commit()
    return jsonify({'message': 'Resume saved'}), 200
