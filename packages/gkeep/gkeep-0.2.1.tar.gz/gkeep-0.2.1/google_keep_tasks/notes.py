# -*- coding: utf-8 -*-
import click
import gkeepapi
import sys

from google_keep_tasks.exceptions import InvalidColor
from google_keep_tasks.management import cli


COLORS = {
    gkeepapi.node.ColorValue.Gray: {'bg': 'black', 'fg': 'white'},
    gkeepapi.node.ColorValue.Red: {'bg': 'red', 'fg': 'white'},
    gkeepapi.node.ColorValue.Green: {'bg': 'green'},
    gkeepapi.node.ColorValue.Yellow: {'bg': 'green', 'fg': 'black'},
    gkeepapi.node.ColorValue.Blue: {'bg': 'cyan', 'fg': 'white'},
    gkeepapi.node.ColorValue.DarkBlue: {'bg': 'blue', 'fg': 'white'},
    gkeepapi.node.ColorValue.Purple: {'bg': 'magenta', 'fg': 'white'},
    gkeepapi.node.ColorValue.White: {'bg': 'white', 'fg': 'black'},
}


def get_color(color):
    if not color:
        return
    color = color.title()
    if color and not hasattr(gkeepapi.node.ColorValue, color):
        raise InvalidColor(color)
    return getattr(gkeepapi.node.ColorValue, color)


def get_click_color(ctx, param, value):
    return get_color(value)


def find_or_create_label(keep, label_name):
    label = keep.findLabel(label_name)
    if not label:
        label = keep.createLabel(label_name)
    return label


def add_labels(keep, note, labels):
    if not labels:
        return
    for label in labels:
        note.labels.add(find_or_create_label(keep, label))


def get_labels(keep, labels):
    return list(filter(bool, map(keep.findLabel, labels)))


def comma_separated(ctx, param, value):
    return value.split(',') if value else []


def query_params(keep, **kwargs):
    kwargs['colors'] = (list(filter(bool, [get_color(kwargs.pop('color'))])) if 'color' in kwargs else []) or None
    labels = get_labels(keep, kwargs.pop('labels', []))
    deleted = kwargs.pop('deleted', None)
    title = kwargs.pop('title', None)
    text = kwargs.pop('text', None)
    if any(filter(lambda x: x is not None, [deleted, title, text])) or labels:
        kwargs['func'] = lambda x: all(filter(lambda y: isinstance(y, bool),
                                              [x.deleted == deleted if deleted is not None else None,
                                               x.title == title if title is not None else None,
                                               x.text == text if text is not None else None,
                                               set(x.labels.all()) == set(labels) if labels is not None else None]))
    return kwargs


def print_note(note):
    params = COLORS.get(note.color, {})
    note_id = (u'⚲ ' if note.pinned else '') + '(note id {})'.format(note.id)
    note_id += u' 🗑' if note.deleted or note.trashed else ''
    click.echo(click.style(note_id, **params))
    click.echo(click.style('"' * len(note_id), **params))
    if note.title:
        click.echo(click.style(note.title, bold=True))
    click.echo(note.text)
    if note.labels:
        click.echo()
        click.echo(' '.join(click.style('[{}]'.format(label.name), underline=True, bold=True)
                            for label in note.labels.all()))
    click.echo(click.style('"' * len(note_id), **params))
    click.echo('\n')


def get_note_instance(keep, id=None, **kwargs):
    if id:
        note = keep.get(id)
    else:
        notes = keep.find(**query_params(keep, **kwargs))
        note = next(notes, None)
    return note


@cli.command('add-note')
@click.option('--color', default='', callback=get_click_color)
@click.option('--labels', default='', callback=comma_separated)
@click.argument('title')
@click.argument('text')
@click.pass_context
def add_note(ctx, color, labels, title, text):
    keep = ctx.obj['keep']
    gnote = keep.createNote(title, text)
    if color:
        gnote.color = color
    add_labels(keep, gnote, labels)
    keep.sync()


@cli.command('search-notes')
@click.option('--color', default='', callback=get_click_color)
@click.option('--labels', default='', callback=comma_separated)
@click.option('--deleted/--not-deleted', default=None)
@click.option('--trashed/--not-trashed', default=None)
@click.option('--pinned/--not-pinned', default=None)
@click.option('--archived/--not-archived', default=None)
@click.option('--title', default=None)
@click.option('--text', default=None)
@click.argument('query', default='')
@click.pass_context
def search_notes(ctx, **kwargs):
    keep = ctx.obj['keep']
    for note in keep.find(**query_params(keep, **kwargs)):
        print_note(note)


@cli.command('get-note')
@click.argument('id', default=None, required=False)
@click.option('--title', default=None)
@click.option('--query', default='')
@click.pass_context
def get_note(ctx, **kwargs):
    keep = ctx.obj['keep']
    note = get_note_instance(keep, **kwargs)
    if note:
        print_note(note)
    else:
        click.echo('The note was not found', err=True)
        sys.exit(2)


@cli.command('edit-note')
@click.option('--title', default=None, required=False)
@click.option('--text', default=None, required=False)
@click.option('--filter-id', default=None, required=False)
@click.option('--filter-title', default=None)
@click.option('--filter-query', default='')
@click.option('--color', default='', callback=get_click_color)
@click.option('--labels', default='', callback=comma_separated)
@click.pass_context
def edit_note(ctx, title, text, color, labels, filter_id, filter_title, filter_query):
    keep = ctx.obj['keep']
    note = get_note_instance(keep, id=filter_id, title=filter_title, query=filter_query)
    if not note:
        click.echo('The note was not found', err=True)
        sys.exit(2)
    updated = {}
    for param in ['title', 'text', 'color', 'labels']:
        value = locals()[param]
        if value:
            updated[param] = (getattr(note, param), value)
            setattr(note, param, value)
    if labels:
        add_labels(keep, note, labels)
    keep.sync()
    click.echo('Updated note fields:\n\n' + ('\n'.join([u'{}: {} 🠞 {}'.format(param, values[0], values[1])
                                                        for param, values in updated.items()])))


@cli.command('delete-note')
@click.argument('id', default=None, required=False)
@click.option('--title', default=None)
@click.option('--query', default='')
@click.pass_context
def delete_note(ctx, **kwargs):
    keep = ctx.obj['keep']
    note = get_note_instance(keep, **kwargs)
    if note and (note.deleted or note.trashed):
        click.echo('The note "{}" had already been deleted.'.format(note.title))
    elif note:
        note.delete()
        keep.sync()
        click.echo('Note with title "{}" deleted.'.format(note.title))
    else:
        click.echo('The note was not found', err=True)
        sys.exit(2)
