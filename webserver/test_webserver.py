from webserver.models import start_session
from webserver.models.user import add_user, get_user
from webserver.models.post import add_post, get_post, iter_all_posts_for_user


def test_db():
    with start_session() as sess:
        user_id = add_user(sess,
                           alias='johndoe',
                           email='johndoe@example.com',
                           password='pass')
        user = get_user(sess, user_id)
        assert user.alias == 'johndoe'
        assert user.email == 'johndoe@example.com'

        post_id1 = add_post(sess,
                           user_id=user_id,
                           body='lorem ipsum')
        post1 = get_post(sess, post_id1)
        assert post1.body == 'lorem ipsum'
        assert post1.user_id == user_id

        post_id2 = add_post(sess,
                            user_id=user_id,
                            body='dolor sit')

        posts = set(iter_all_posts_for_user(sess, user_id=user_id))
        assert len(posts) == 2
        assert post1 in posts
        assert get_post(sess, post_id2) in posts
