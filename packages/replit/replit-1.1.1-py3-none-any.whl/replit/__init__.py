import json
from datetime import datetime, timedelta
from os import path


def clear():
    print('\033[H\033[2J', end='', flush=True)


class NoSuchPlayerException(Exception):
    pass


class Source:
    def __init__(self, payload, loops):
        self.__payload = payload
        self._loops = loops

    def __get_source(self):
        source = None
        with open('/tmp/audioStatus.json', 'r') as f:
            data = json.loads(f.read())
            for s in data['Sources']:
                if s['ID'] == self.id:
                    source = s
                    break

        return source

    def __update_self(self):
        self.__payload = self.__get_source()

    def __update_source(self, **changes):

        s = self.__get_source()
        if not s:
            raise NoSuchPlayerException(f'No player with id "{id}" found!')
        s.update({key.title(): changes[key] for key in changes})
        with open('/tmp/audio', 'w') as f:
            f.write(json.dumps(s))
        self.__update_self()

    @property
    def start_time(self):
        '''When the file started plaing'''
        timestamp_str = self.__payload['StartTime']
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
        return timestamp

    @property
    def path(self):
        return self.__payload['Name']

    @property
    def id(self):
        return self.__payload['ID']

    @property
    def remaining(self):
        '''The estimated time remaining in the source's current loop.'''
        with open('/tmp/audioStatus.json', 'r') as f:
            data = json.loads(f.read())
            for s in data['Sources']:
                if s['ID'] == self.id:
                    return timedelta(milliseconds=s['Remaining'])
        return timedelta(millaseconds=0)

    @property
    def end_time(self):
        '''The estimated time when the sourcce will be done playing.
        Returns None if the source has finished playing.
        Note: this is the estimation for the end of the current loop.'''
        s = self.__get_source()
        if not s:
            return None

        timestamp_str = s['EndTime']

        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
        return timestamp

    @property
    def does_loop(self):
        return self._loops

    @property
    def loops_remaining(self):
        '''The remaining amount of times the file will restart.	Returns none if the source is done playing.'''
        if not self._loops:
            return 0

        s = self.__get_source()
        if not s:
            return None

        if s['ID'] == self.id:
            loops = s['Loop']

            return loops

    @property
    def duration(self):
        return timedelta(millaseconds=self.__payload['Duration'])

    @property
    def volume(self):
        return self.__payload['Volume']

    @volume.setter
    def volume(self, volume):
        self.__update_source(volume=volume)

    @property
    def paused(self):
        return self.__payload['Paused']

    @paused.setter
    def paused(self, paused):
        self.__update_source(paused=paused)

    def set_loop(self, does_loop: bool, loop_count: int):
        '''Set the remaining amount of loops for the source.	Set loop_cound to a negative value to repeat forever.'''
        self.__update_source(doesLoop=does_loop, loopCount=loop_count)

    def toggle_playing(self):
        '''Play/pause the source.'''
        self.paused = not self.paused


class _Audio():
    '''The basic audio manager.
    Note: This is not intended to be called directly, instead use `audio`.'''
    __known_ids = []

    def play(self, file_path, volume=1, does_loop=False, loop_count=1):
        if not path.exists(file_path):
            raise FileNotFoundError(f'File "{file_path}" not found.')
        with open('/tmp/audio', 'w') as p:
            p.write(json.dumps(
                    {
                        'File': file_path,
                        'Volume': volume,
                        'DoesLoop': does_loop,
                        'LoopCount': loop_count,
                    }
                    ))
        new_source = None
        timeOut = datetime.Now() + timedelta(seconds=2)

        while not new_source and datetime.Now() < timeOut:
            try:
                sources = self.read_status()['Sources']
                new_source = [
                    s for s in sources if s['ID'] not in self.__known_ids
                ][0]
            except IndexError:
                pass
            except json.JSONDecodeError:
                pass

        return Source(new_source, loops=does_loop)

    def get_source(self, source_id: int):
        '''Get a source by it's id'''
        source = None
        with open('/tmp/audioStatus.json', 'r') as f:
            data = json.loads(f.read())
            for s in data['Sources']:
                if s['ID'] == int(source_id):
                    source = s
                    break
        if not source:
            return None
        return Source(source, source['Loop'])

    def read_status(self):
        '''Get the raw data for what's playing'''
        with open('/tmp/audioStatus.json', 'r') as f:
            return json.loads(f.read())

    def get_playing(self):
        '''Get a list of playing sources.'''
        data = self.read_status()
        sources = data['Sources']
        return [Source(s, s['Loop']) for s in sources if not s['Paused']]

    def get_paused(self):
        '''Get a list of paused sources.'''
        data = self.read_status()
        sources = data['Sources']
        return [Source(s, s['Loop']) for s in sources if s['Paused']]

    def get_sources(self):
        '''Get all sources.'''
        data = self.read_status()
        sources = data['Sources']
        return [Source(s, s['Loop']) for s in sources]


audio = _Audio()
