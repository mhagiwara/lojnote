from webserver.models import start_session
from webserver.models.user import add_user, get_user


def test_db():
    with start_session() as sess:
        user_id = add_user(sess,
                           alias='johndoe',
                           email='johndoe@example.com',
                           password='pass')
        user = get_user(sess, user_id)
        assert user.alias == 'johndoe'
        assert user.email == 'johndoe@example.com'

