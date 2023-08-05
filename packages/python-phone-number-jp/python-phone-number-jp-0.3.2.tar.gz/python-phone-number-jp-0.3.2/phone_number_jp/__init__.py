#!/usr/bin/env python3
# coding: utf-8
from typing import Tuple

from .prefix_numbers import phone_number_prefixes

__author__ = 'ytyng'
__version__ = '0.3.2'
__license__ = 'BSD'

MAX_PREFIX_DIGIT = 5
MIN_PREFIX_DIGIT = 2


class PhoneNumberJPError(Exception):
    pass


class PhoneNumberIsNotDigits(PhoneNumberJPError):
    pass


class InvaliDigits(PhoneNumberJPError):
    pass


class PrefixNoMatch(PhoneNumberJPError):
    pass


def _split_tail(prefix: str, tail: str) -> Tuple[str, str, str]:
    # 残りが7桁の場合、3, 4 で分割
    tail_split_digits = int(len(tail) / 2)

    return prefix, tail[:tail_split_digits], tail[tail_split_digits:]


def split_phone_number(phone_number: str) -> Tuple[str, str, str]:
    if not phone_number.isdigit():
        raise PhoneNumberIsNotDigits(phone_number)

    if len(phone_number) < 10:
        raise InvaliDigits(phone_number)

    for d in range(MAX_PREFIX_DIGIT, MIN_PREFIX_DIGIT - 1, -1):
        p = phone_number[:d]
        if p in phone_number_prefixes[d]:
            return _split_tail(p, phone_number[d:])

    raise PrefixNoMatch(phone_number)


def split_phone_number_no_fail(phone_number: str) -> Tuple[str, str, str]:
    """
    無理やり3分割する。無理な時は空文字
    """
    if not phone_number:
        return '', '', ''
    try:
        return split_phone_number(phone_number)
    except PrefixNoMatch:
        return _split_tail(phone_number[:3], phone_number[3:])
    except InvaliDigits:
        if len(phone_number) > 5:
            return _split_tail(phone_number[:3], phone_number[3:])
    except PhoneNumberIsNotDigits:
        return '', '', ''
    return _split_tail('', phone_number)


def insert_hyphens(phone_number: str) -> str:
    """
    Insert hyphens.
    """
    if '-' in phone_number:
        return phone_number
    return '-'.join(split_phone_number_no_fail(phone_number))


def insert_spaces(phone_number: str) -> str:
    """
    Insert spaces.
    """
    if ' ' in phone_number:
        return phone_number
    return ' '.join(split_phone_number_no_fail(phone_number))
