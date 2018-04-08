from webserver.models import start_session
from webserver.models.user import add_user, get_user
from webserver.models.post import add_post, get_post


def test_db():
    with start_session() as sess:
        user_id = add_user(sess,
                           alias='johndoe',
                           email='johndoe@example.com',
                           password='pass')
        user = get_user(sess, user_id)
        assert user.alias == 'johndoe'
        assert user.email == 'johndoe@example.com'

        post_id = add_post(sess,
                           user_id=user_id,
                           body='lorem ipsum')
        post = get_post(sess, post_id)
        assert post.body == 'lorem ipsum'
        assert post.user_id == user_id
