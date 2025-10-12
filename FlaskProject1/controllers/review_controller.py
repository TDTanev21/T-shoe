from flask import Blueprint, request, jsonify, flash
from flask_login import login_required, current_user
from models.review import Review
from models.product import Shoe
from models import db

review_bp = Blueprint('review', __name__)


@review_bp.route('/add_review/<int:product_id>', methods=['POST'])
@login_required
def add_review(product_id):
    try:
        rating = request.form.get('rating')
        comment = request.form.get('comment', '').strip()

        if not rating:
            flash('Моля, изберете рейтинг.', 'error')
            return jsonify({'success': False, 'message': 'Моля, изберете рейтинг.'})

        rating = int(rating)
        if rating < 1 or rating > 5:
            flash('Рейтингът трябва да е между 1 и 5 звезди.', 'error')
            return jsonify({'success': False, 'message': 'Рейтингът трябва да е между 1 и 5 звезди.'})

        product = Shoe.query.get(product_id)
        if not product:
            flash('Продуктът не е намерен.', 'error')
            return jsonify({'success': False, 'message': 'Продуктът не е намерен.'})

        existing_review = Review.query.filter_by(
            product_id=product_id,
            user_id=current_user.id
        ).first()

        if existing_review:
            existing_review.rating = rating
            existing_review.comment = comment
            flash('Вашето ревю е актуализирано успешно!', 'success')
        else:
            new_review = Review(
                product_id=product_id,
                user_id=current_user.id,
                rating=rating,
                comment=comment
            )
            db.session.add(new_review)
            flash('Вашето ревю е добавено успешно!', 'success')

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Ревюто е запазено успешно!'
        })

    except Exception as e:
        db.session.rollback()
        flash(f'Грешка при запазване на ревюто: {str(e)}', 'error')
        return jsonify({'success': False, 'message': str(e)})


@review_bp.route('/get_reviews/<int:product_id>')
def get_reviews(product_id):
    try:
        reviews = Review.query.filter_by(product_id=product_id) \
            .order_by(Review.created_at.desc()) \
            .all()

        reviews_data = [review.to_dict() for review in reviews]

        # Изчисляване на среден рейтинг
        average_rating = 0
        if reviews:
            average_rating = sum(review.rating for review in reviews) / len(reviews)

        # Проверка дали текущият потребител е оставил ревю
        user_review = None
        if current_user.is_authenticated:
            user_review = Review.query.filter_by(
                product_id=product_id,
                user_id=current_user.id
            ).first()
            if user_review:
                user_review = user_review.to_dict()

        return jsonify({
            'success': True,
            'reviews': reviews_data,
            'average_rating': round(average_rating, 1),
            'total_reviews': len(reviews),
            'user_review': user_review
        })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@review_bp.route('/delete_review/<int:review_id>', methods=['DELETE'])
@login_required
def delete_review(review_id):
    try:
        review = Review.query.get(review_id)

        if not review:
            return jsonify({'success': False, 'message': 'Ревюто не е намерено.'})

        # Проверка дали потребителят е собственик на ревюто
        if review.user_id != current_user.id and not current_user.is_admin:
            return jsonify({'success': False, 'message': 'Нямате права да изтриете това ревю.'})

        db.session.delete(review)
        db.session.commit()

        flash('Ревюто е изтрито успешно!', 'success')
        return jsonify({'success': True, 'message': 'Ревюто е изтрито успешно!'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})