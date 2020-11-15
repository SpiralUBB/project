from math import ceil

from flask import request
from mongoengine import QuerySet

from config import MAX_PAGINATED_LIMIT
from utils.errors import PaginationPageInvalid, PaginationLimitInvalid


def default_mapping_fn(item):
    return item.to_dict()


def get_paginated_items_from_qs(qs: QuerySet, mapping_fn=default_mapping_fn):
    page = request.args.get('page', default='0')
    limit = request.args.get('limit', default='0')

    try:
        page = int(page)
    except ValueError:
        raise PaginationPageInvalid()

    try:
        limit = int(limit)
    except ValueError:
        raise PaginationLimitInvalid()

    limit = min(limit, MAX_PAGINATED_LIMIT)
    skip = page * limit

    qs = qs.skip(skip).limit(limit)

    no_total_items = qs.count()
    no_items = qs.count(with_limit_and_skip=True)
    no_pages = ceil(no_total_items / limit)

    return {
        'limit': limit,
        'skip': skip,
        'page': page,
        'no_items': no_items,
        'no_total_items': no_total_items,
        'no_pages': no_pages,
        'items': [mapping_fn(item) for item in qs],
    }
