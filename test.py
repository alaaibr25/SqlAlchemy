# <!--        <form action="/update" method="POST">-->
# <!--                    <input name="id" value="{{movie.id}}" hidden>-->
# <!--                    <input type="number" name="new_rate" placeholder="Your rate out of 10">-->
# <!--                   <br><input type="text" name="new_review" placeholder="Review">-->
# <!--                    <br><button type="submit" class="btn btn-primary mb-5">Done</button>-->
# <!--        </form>-->


# @app.route('/update', methods=['POST', 'GET'])
# def update_page():
#     if request.form == 'POST':
#         movie_id = request.form['id']
#         movie_to_update = db.get_or_404(Movie, movie_id)
#         movie_to_update.rate = request.form['rate']
#         db.session.commit()
#         return redirect(url_for('home'))
#
#     movie_id = request.args.get('id')
#     movie_to_update = db.get_or_404(Movie, movie_id)
#
#     return render_template("update.html", movie=movie_to_update)

#====================================================================#
#🟡Bootstrap Flask🟡
# {% from 'bootstrap5/form.html' import render_form %}
# {{ render_form(form) }}

# class MovieForm(FlaskForm):
#     rate = IntegerField('New Rate')
#     review = StringField('Review')
#     submit = SubmitField('Submit')


# @app.route('/update', methods=['POST', 'GET'])
# def update_page():
#     movie_form = MovieForm()
#     movie_id = request.args.get('id')
#     movie_to_update = db.get_or_404(Movie, movie_id)
#
#     if movie_form.validate_on_submit():
#
#         movie_to_update.rate = movie_form.rate.data
#         movie_to_update.review = movie_form.review.data
#         db.session.commit()
#         return redirect(url_for('home'))
#
#
#
#     return render_template("update.html", movie=movie_to_update, fform=movie_form)