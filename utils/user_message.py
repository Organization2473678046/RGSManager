# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        # 'user_id': user.id,
        # 'username': user.username
    }
