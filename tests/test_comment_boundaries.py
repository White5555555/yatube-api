from http import HTTPStatus

import pytest

from posts.models import Comment

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('method', ('get', 'put', 'patch', 'delete'))
def test_comment_unavailable_under_another_post(
    user_client, post, comment_1_another_post, method,
):
    comment = comment_1_another_post
    original_text = comment.text
    response = getattr(user_client, method)(
        f'/api/v1/posts/{post.id}/comments/{comment.id}/',
        data={'text': 'Changed'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == original_text


@pytest.mark.parametrize('method', ('get', 'post'))
def test_comments_of_missing_post(user_client, post, method):
    post_id = post.id
    post.delete()
    count = Comment.objects.count()
    response = getattr(user_client, method)(
        f'/api/v1/posts/{post_id}/comments/', data={'text': 'New'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == count


def test_author_can_delete_own_comment(user_client, comment_1_post):
    comment = comment_1_post
    response = user_client.delete(
        f'/api/v1/posts/{comment.post_id}/comments/{comment.id}/',
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not Comment.objects.filter(pk=comment.id).exists()
