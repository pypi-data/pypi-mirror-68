from django.contrib.auth.models import User, Group


def is_in_group(user: User, group: Group) -> bool:
    assert user.is_authenticated, 'User is not authenticated'
    return user.groups.filter(name=group).exists()
