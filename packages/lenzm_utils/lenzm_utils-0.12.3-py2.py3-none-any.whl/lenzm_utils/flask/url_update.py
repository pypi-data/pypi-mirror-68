"""Tools to build a URL using the current URL as defaults."""
from collections import Iterable

from flask import request, url_for
from werkzeug.datastructures import MultiDict


def url_update_args(**kwargs):
	"""Take the current URL and update only some parameters.

	Keeping all unspecified params the same and only update the passed parms.
	"""
	return url_update_endpoint_args(request.endpoint, **kwargs)


def url_update_endpoint_args(endpoint, **kwargs):
	"""Like url_for by using current URL for unspecified parameters.

	Return the URL for passed endpoint using args from current request and kwargs.
	"""
	# request.args contains parameters from the query string
	# request.view_args contains parameters that matched the view signature
	args = MultiDict(request.args)
	args.update(request.view_args)
	for arg, value in kwargs.items():
		if isinstance(value, Iterable) and not isinstance(value, str):
			args.setlist(arg, value)
		else:
			args[arg] = value
	# Now set any individual args to the object instead of a list of len 1
	# TODO Issue #4
	#  this is broken if it supposed to be a list of Iterables (e.g. strings)
	args = args.to_dict(flat=False)
	for key in set(args.keys()):
		values = args[key]
		if len(values) == 1:
			args[key] = values[0]
	return url_for(endpoint, **args)


def url_update(*args, **kwargs):
	if args:
		if len(args) > 1:
			raise ValueError('Can only pass one positional argument')
		return url_update_endpoint_args(args[0], **kwargs)
	else:
		return url_update_endpoint_args(request.endpoint, **kwargs)
