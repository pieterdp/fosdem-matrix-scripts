#!/usr/bin/env python
from yaml import safe_load
from jinja2 import Environment, PackageLoader, select_autoescape


class Event:
    def __init__(self, event_id, event_slug, event_name, track_name, track_type, room_name):
        self.event_id = event_id
        self.slug = event_slug
        self.name = event_name
        self.track = track_name
        self.type = track_type
        self.room = room_name[1:]  # Get rid of the m/s/d/k in front of the room name

    @property
    def backstage(self):
        return '#talk-{0}:fosdem.org'.format(self.event_id)

    @property
    def audience(self):
        if self.type == 'devroom':
            return '#{0}-devroom:fosdem.org'.format(self.room)
        elif self.type == 'maintrack':
            if self.room == 'fosdem':
                return '#{0}-keynotes:fosdem.org'.format(self.room)
            else:
                return '#{0}:fosdem.org'.format(self.room)
        elif self.type == 'standtrack':
            return '#{0}-stand:fosdem.org'.format(self.room)
        else:
            return '#{0}:fosdem.org'.format(self.room)

    @property
    def audience_backstage(self):
        if self.type == 'devroom':
            return '#{0}-backstage-devroom:fosdem.org'.format(self.room)
        elif self.type == 'maintrack':
            if self.room == 'fosdem':
                return '#{0}-backstage-keynotes:fosdem.org'.format(self.room)
            else:
                return '#{0}-backstage:fosdem.org'.format(self.room)
        elif self.type == 'standtrack':
            return None
        else:
            return '#{0}-backstage:fosdem.org'.format(self.room)


def events_from_penta():
    """
    Get all events from data/pentabarf.yaml
    :return:
    """
    with open('data/pentabarf.yaml', 'r') as fh:
        schedule = safe_load(fh)
    return schedule['events']


def events_overview(penta_events):
    """
    Generate an Event for envery event in penta.
    :param penta_events:
    :return:
    """
    events = []
    for slug, penta_event in penta_events.items():
        events.append(Event(
            event_id=penta_event['event_id'],
            event_name=penta_event['title'],
            event_slug=penta_event['slug'],
            track_name=penta_event['track_name'],
            track_type=penta_event['type'],
            room_name=penta_event['room']
        ))
    return events


def table_from_events(events):
    """
    Create a markdown table in out/
    :param events:
    :return:
    """
    env = Environment(
        loader=PackageLoader('matrix_id_for_each_event'),
        autoescape=select_autoescape()
    )
    template = env.get_template('event_ids.md.j2')
    rendered = template.render(
        events=events
    )
    with open('out/event_ids.md', 'w') as fh:
        fh.write(rendered.encode('utf-8'))


def main():
    events = events_from_penta()
    event_table = events_overview(events)
    table_from_events(event_table)
    return 0


if __name__ == '__main__':
    exit(main())
