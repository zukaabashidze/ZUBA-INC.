from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from models import User, Post

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        abort(403)
    users = User.query.all()
    posts = Post.query.all()
    return render_template('admin.html', users=users, posts=posts)


def calculate_share(total_amount, users_count):
    if users_count == 0:
        return 0
    return total_amount / users_count