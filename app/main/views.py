from flask import render_template, redirect, url_for, abort, request
from ..models import User, Pitch, Comments, PitchCategory,Votes
from flask_login import login_required, current_user 
from .forms import PitchForm, CommentForm, UpdateProfile, CategoryForm
from .. import db, photos
from . import main
import markdown2  

@main.route ('/')
def index():
    """
    Function that returns index page and data
    """
    category = PitchCategory.get_categories()
    return render_template('index.html', categories = category)



@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by (username = uname).first()
    
    if user is None:
        abort(404)
        
    return render_template('profile/profile.html', user = user)

@main.route('/user/<uname>/update', methods = ['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by (username = uname).first()
    if user is None:
        abort(404)
        
    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('.profile', uname = user.user))
    return render_template('profile/update.html', form = form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
@main.route('/category/new-pitch/<int:id>', methods= ['GET', 'POST'])
@login_required
def new_pitch(id):
    """
    Function to fetch data 
    """
    form = PitchForm()
    category = PitchCategory.query.filter_by(id=id).first()

    if category is None:
        abort(404)
        
    if form.validate_on_submit():
        pitch = form.pitch.data
        new_pitch = Pitch(pitch = pitch, category_id = category.id, user_id= current_user.id)
        new_pitch.save_pitch()
        

        return redirect(url_for('.category', id= category.id))
    
    return render_template('new_pitch.html', pitch_form = form, category = category)    

@main.route('/add/category', methods = ['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    
    if form.validate_on_submit():
        name = form.name.data
        new_category = PitchCategory(name=name)
        new_category.save_category()
        
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('.index'))
    title = 'New Category'   
    return render_template('post_comment.html', comment_form = form, title = title)    
@main.route('/view/<int:id>', methods = ['GET', 'POST'])
@login_required
def view_pitch(id):
    """
    Function that returns a single pitch with comments
    """
    print(id)
    pitches = Pitch.query.get(id)
    if pitches is None:
        abort(404)
           
    comment = Comments.get_comments(id)
    title = 'View Pitch'
    return render_template('view.html', pitches= pitches, comment = comment, category_= id, title= title)
@main.route('/write_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def post_comment(id):
    """
    Fuction to add comments
    """
    form = CommentForm()
    title = "Add a  comment"
    pitches = Pitch.query.filter_by(id=id).first()

    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comments(comment=comment, user_id=current_user.id, pitches_id=pitches.id)
        new_comment.save_comment()
        return redirect(url_for('.view_pitch', id=pitches.id))

    return render_template('post_comment.html', comment_form=form, title=title)

# voting
@main.route('/pitch/upvote/<int:id>')
@login_required
def upvote(id):
    '''
    View function that add one to the vote_number column in the votes table
    '''
    pitch_id = Pitch.query.filter_by(id=id).first()

    if pitch_id is None:
         abort(404)

    new_vote = Votes(vote=int(1), user_id=current_user.id, pitches_id=pitch_id.id)
    new_vote.save_vote()
    return redirect(url_for('.view_pitch', id=id))



@main.route('/pitch/downvote/<int:id>')
@login_required
def downvote(id):
    pitch_id = Pitch.query.filter_by(id=id).first()

    new_vote = Votes(vote=int(2), user_id=current_user.id, pitches_id=pitch_id.id)
    new_vote.save_vote()
    return redirect(url_for('.view_pitch', id=id))

@main.route('/pitch/downvote/<int:id>')
@login_required
def vote_count(id):

    votes = Votes.query.filter_by(user_id=current_user.id).all()

    total_votes = votes.count()

    return total_votes

@main.route('/like/<int:pitch_id>/<action>')
@login_required
def like_action(comment_id, action):
    comment = Comment.query.filter_by(id=post_id).first_or_404()
    if action == 'vote':
        current_user.vote_comment(comment)
        db.session.commit()
    if action == 'downvote':
        current_user.unlike_comment(comment)
        db.session.commit()
    return redirect(request.referrer)  