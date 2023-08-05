try:
    from com.dtmilano.android.viewclient import ViewClient
    from StringIO import StringIO
except ImportError:
    from androidviewclient3.viewclient import ViewClient
    from io import StringIO

import threading
import datetime
import time

from activitystatemachine import ActivityStateMachine
from logger import Logger

ERROR_MSG = "the handler has not been initialized, please call .walk_through()"

def utf8str(s):
    try:
        return unicode(s).encode("UTF-8")
    except:
        return s

class GMControlPanel(object):
    def __init__(self, gmhandler):
        self.handler = gmhandler
        info = gmhandler.cache["control_panel"]
        self.progress_pos = info["progress"]["position"]
        self.progress_xb = info["progress"]["xbounds"]
        self.playpause_pos = info["play_pause"]["position"]
        self.prev_pos = info["prev"]["position"]
        self.next_pos = info["next"]["position"]

    def get_current_song(self):
        vc = ViewClient(self.handler.device, self.handler.serialno)
        so = StringIO()
        vc.traverse(stream=so)
        line = [line for line in so.getvalue().splitlines() if GoogleMusicApp.CONTROL_PANEL_TRACKNAME_KEY in line]
        line = line[0] if len(line) > 0 else None
        if line:
            name = utf8str(line.split(GoogleMusicApp.CONTROL_PANEL_TRACKNAME_KEY)[-1].strip())
            for playcard_title, info in self.handler.cache["playcard"].items():
                if "songs" in info.keys() and name in info["songs"].keys():
                    song = dict(info["songs"][name])
                    song["name"] = name
                    song["playcard"] = playcard_title
                    return song
        return None

    def play(self):
        if not self.handler.is_playing():
            self.play_pause()

    def pause(self):
        if self.handler.is_playing():
            self.play_pause()

    def play_pause(self):
        self.handler.device.touch(*self.playpause_pos)

    def next(self):
        self.handler.device.touch(*self.next_pos)

    def previous(self):
        self.handler.device.touch(*self.prev_pos)

    def seek(self, percentage):
        if percentage < 0 or percentage > 1.0:
            raise ValueError("the percentage should be in [0.0, 1.0]")
        _, y = self.progress_pos
        xmin, xmax = self.progress_xb
        self.handler.device.touch((xmax-1-xmin)*percentage + xmin, y)


class GoogleMusicApp(ActivityStateMachine):
    COMPONENT = "com.google.android.music/com.android.music.activitymanagement.TopLevelActivity"

    PLAY_CARD_KEY = "com.google.android.music:id/play_card"
    LI_TITLE_KEY = "com.google.android.music:id/li_title"
    LI_SUBTITLE_KEY = "com.google.android.music:id/li_subtitle"
    CONTAINER_KEY = "com.google.android.music:id/drawer_container"
    ART_PAGER_KEY = "com.google.android.music:id/art_pager"
    PLAY_PAUSE_HEADER_KEY = "com.google.android.music:id/play_pause_header"

    CONTROL_PANEL_TRACKNAME_KEY = "com.google.android.music:id/trackname"
    CONTROL_PANEL_PROGRESS_KEY = "android:id/progress"
    CONTROL_PANEL_PLAY_PAUSE_KEY = "com.google.android.music:id/pause"
    CONTROL_PANEL_PREV_KEY = "com.google.android.music:id/prev"
    CONTROL_PANEL_NEXT_KEY = "com.google.android.music:id/next"

    class State(object):
        UNKNOWN = "Unknown"
        TOP_ACTIVITY = "TopActivity"
        TRACK_LIST = "TrackList"
        CONTROL_PANEL = "ControlPanel"

        TOP_ACTIVITY_STATE = {
            "name": TOP_ACTIVITY,
            "check": lambda s: \
                "com.google.android.music:id/play_card" in s or \
                "com.google.android.music:id/empty_text" in s
        }
        TRACK_LIST_STATE = {
            "name": TRACK_LIST,
            "check": lambda s: \
                    "com.google.android.music:id/controls_container" in s and \
                not "com.google.android.music:id/play_card" in s
        }
        CONTROL_PANEL_STATE = {
            "name": CONTROL_PANEL,
            "check": lambda s: \
                "com.google.android.music:id/play_controls" in s
        }

        ALL_STATES = [
            TOP_ACTIVITY_STATE,
            TRACK_LIST_STATE,
            CONTROL_PANEL_STATE
        ]

    def __init__(self, device, serialno):
        super(GoogleMusicApp, self).__init__(device, serialno)
        self.extra = {
            "dump": [],
            "dump-lock": threading.Lock()
        }
        self.control_panel = None
        self.cache = {}
        self.cache_init = False

    def log(self, text):
        Logger.log("GoogleMusicApp", text)

    def dump(self):
        self.extra["dump-lock"].acquire()
        Logger.log("GoogleMusicApp", "dump called")
        Logger.log("GoogleMusicApp", "----------------------------------------------")
        map(lambda x: Logger.log("GoogleMusicApp::dump", "\"{}\"".format(x)), self.extra["dump"])
        Logger.log("GoogleMusicApp", "----------------------------------------------")
        del self.extra["dump"][:]
        self.extra["dump-lock"].release()

    def push_dump(self, text):
        self.extra["dump-lock"].acquire()
        self.extra["dump"].append("[{}] {}".format(datetime.datetime.now(), text))
        self.extra["dump-lock"].release()

    def clear_dump(self):
        self.extra["dump-lock"].acquire()
        del self.extra["dump"][:]
        self.extra["dump-lock"].release()

    def walk_through(self):
        if not self.to_top():
            Logger.log("GoogleMusicApp", "walk_through failed: unable to go to top activity")
            self.cache_init = False
            return False

        # Get the playcard titles
        vc = ViewClient(self.device, self.serialno)

        self.cache_init = True

        container_key = GoogleMusicApp.CONTAINER_KEY
        container = [v for v in vc.getViewsById().values() if v.getId() == container_key]
        container = container[0] if len(container) > 0 else None
        if container:
            self.cache["screen-info"] = container.getBounds()[1]
            self.push_dump("screen-info: {}".format(self.cache["screen-info"]))

        so = StringIO()
        vc.traverse(stream=so)
        lines = so.getvalue().splitlines()
        play_card_key = GoogleMusicApp.PLAY_CARD_KEY
        playcards_idices = [idx for idx, line in enumerate(lines) if play_card_key in line]
        playcards_idices.append(len(lines))
        playcards_titles = []
        last_idx = playcards_idices[0]

        li_title_key = GoogleMusicApp.LI_TITLE_KEY
        for idx in playcards_idices[1:]:
            li_title_texts = [line for line in lines[last_idx:idx] if li_title_key in line]
            last_idx = idx

            if len(li_title_texts) != 1:
                self.push_dump("li_title_texts has length {}".format(len(li_title_texts)))

            playcards_titles.append(utf8str(li_title_texts[0].split(li_title_key)[-1].strip()))
            self.push_dump("playcards_titles.append('{}')".format(playcards_titles[-1]))

        # Get the track list of each playcard
        views = [v for v in vc.getViewsById().values() if v.getId() == li_title_key and utf8str(v.getText()) in playcards_titles]
        self.cache["playcard"] = {}

        for v in views:
            if utf8str(v.getText()) in self.cache["playcard"]:
                self.cache["playcard"][utf8str(v.getText())]["position"].append(v.getCenter())
            else:
                self.cache["playcard"][utf8str(v.getText())] = { "position": [v.getCenter()] }

        map(lambda v: self.push_dump("view: {}".format(utf8str(v))), views)
        map(lambda title: self.push_dump("playcard title: '{}'".format(title)), self.cache["playcard"].keys())

        if len(views) == 0:
            self.cache_init = False
            return False

        self.cache["shuffle_key"] = playcards_titles[0]
        self.push_dump("get the shuffle keyword '{}'".format(self.cache["shuffle_key"]))
        self.touch_playcard(self.cache["shuffle_key"])
        time.sleep(1)

        retry_count = 3
        while retry_count > 0:
            vc.dump()
            play_pause_header_key = GoogleMusicApp.PLAY_PAUSE_HEADER_KEY
            play_pause_btn_view = [v for v in vc.getViewsById().values() if v.getId() == play_pause_header_key]
            play_pause_btn_view = play_pause_btn_view[0] if len(play_pause_btn_view) > 0 else None
            if play_pause_btn_view:
                play_desc = utf8str(play_pause_btn_view.getContentDescription())
                self.check_play_status = lambda desc: desc == play_desc
                self.cache["play_pause_btn"] = { "position": play_pause_btn_view.getCenter(), "desc_feat": play_desc }

                art_pager_key = GoogleMusicApp.ART_PAGER_KEY
                art_pager_view = [v for v in vc.getViewsById().values() if v.getId() == art_pager_key]
                art_pager_view = art_pager_view[0] if len(art_pager_view) > 0 else None
                if not art_pager_view:
                    retry_count -= 1
                    continue
                self.cache["art_pager_view"] = { "position": art_pager_view.getCenter() }

                play_pause_btn_view.touch()
                break
            else:
                self.push_dump("cannot find the play/pause button, retry: {}".format(retry_count))
                retry_count -= 1

        if retry_count == 0:
            return False

        for li_title in self.cache["playcard"].keys():
            if li_title == self.cache["shuffle_key"]:
                continue
            self.push_dump("now fetching information in the playcard '{}'".format(li_title))
            self.cache["playcard"][li_title]["songs"] = []
            for idx in range(len(self.cache["playcard"][li_title]["position"])):
                if self.touch_playcard(li_title=li_title, idx=idx):
                    time.sleep(1)
                    self.cache["playcard"][li_title]["songs"].append(self._fetch_songs())
                    self.to_top()

        # Get the information of the control panel
        retry_count = 3
        while self.get_state() != GoogleMusicApp.State.CONTROL_PANEL and retry_count > 0:
            self.device.touch(*self.cache["art_pager_view"]["position"])
            retry_count -= 1

        if retry_count == 0 and self.get_state() != GoogleMusicApp.State.CONTROL_PANEL:
            self.to_top()
            time.sleep(5)
            self.touch_playcard(self.cache["shuffle_key"])
            time.sleep(2)
            self.device.touch(*self.cache["play_pause_btn"]["position"])
            time.sleep(2)
            self.device.touch(*self.cache["art_pager_view"]["position"])
            time.sleep(2)
            if self.get_state() != GoogleMusicApp.State.CONTROL_PANEL:
                self.push_dump("cannot get the information of the control panel")
                self.cache_init = False
                return False

        def find_view_position(vc, res_id):
            v = [v for v in vc.getViewsById().values() if v.getId() == res_id]
            if len(v) == 0:
                return ((-1, -1), (-1, -1)), (-1, -1)
            return v[0].getBounds(), v[0].getCenter()

        vc.dump()
        progress_bounds, progress_pos = find_view_position(vc, GoogleMusicApp.CONTROL_PANEL_PROGRESS_KEY)
        self.cache["control_panel"] = {
            "progress": { "position": progress_pos, "xbounds": [progress_bounds[0][0], progress_bounds[1][0]] },
            "prev": { "position": find_view_position(vc, GoogleMusicApp.CONTROL_PANEL_PREV_KEY)[1] },
            "next": { "position": find_view_position(vc, GoogleMusicApp.CONTROL_PANEL_NEXT_KEY)[1] },
            "play_pause": { "position": find_view_position(vc, GoogleMusicApp.CONTROL_PANEL_PLAY_PAUSE_KEY)[1] }
        }
        self.control_panel = GMControlPanel(self)
        self.push_dump("successfully walked through, now back to top")
        self.to_top()

        self.cache_init = True
        return True

    def is_playing(self):
        vc = ViewClient(self.device, self.serialno)
        play_pause_header_key = GoogleMusicApp.PLAY_PAUSE_HEADER_KEY
        play_pause_btn_view = [v for v in vc.getViewsById().values() if v.getId() == play_pause_header_key]
        play_pause_btn_view = play_pause_btn_view[0] if len(play_pause_btn_view) > 0 else None

        if play_pause_btn_view:
            return self.check_play_status(utf8str(play_pause_btn_view.getContentDescription()))

        ctrl_panel_play_pause_key = GoogleMusicApp.CONTROL_PANEL_PLAY_PAUSE_KEY
        ctrl_panel_play_pause_view = [v for v in vc.getViewsById().values() if v.getId() == ctrl_panel_play_pause_key]
        ctrl_panel_play_pause_view = ctrl_panel_play_pause_view[0] if len(ctrl_panel_play_pause_view) > 0 else None

        if ctrl_panel_play_pause_view:
            return self.check_play_status(utf8str(ctrl_panel_play_pause_view.getContentDescription()))

        return False

    def get_playcards(self):
        if not self.cache_init:
            raise RuntimeError(ERROR_MSG)

        if "playcard" in self.cache.keys():
            return self.cache["playcard"]
        return {}

    def _drag_up(self, drag_up_count=1):
        w, h = self.cache["screen-info"]
        for _ in range(drag_up_count):
            self.device.drag((w/2, h/2), (w/2, 0), duration=1000)

    def _fetch_songs(self):
        vc = ViewClient(self.device, self.serialno, autodump=False)
        songs = {}
        drag_up_count = 0
        li_title_key = GoogleMusicApp.LI_TITLE_KEY
        while True:
            song_props = self._fetch_songs_on_current_screen(vc=vc)
            song_props = list(filter(lambda prop: not prop[0] in songs.keys(), song_props))
            if len(song_props) == 0:
                break
            for name, duration in song_props:
                v = [v for v in vc.getViewsById().values() if v.getId() == li_title_key and utf8str(v.getText()) == name]
                if len(v) != 1:
                    self.push_dump("in _fetch_songs, got multiple songs with the same name '{}'".format(name))
                v = v[0] if len(v) > 0 else None
                songs[name] = {
                    "duration": duration,
                    "drag_up_count": drag_up_count,
                    "position": v.getCenter() if v else (-1, -1)
                }
            self._drag_up()
            drag_up_count += 1

        for name, info in songs.items():
            self.push_dump("{}: {}".format(name, info))

        return songs

    def _fetch_songs_on_current_screen(self, vc):
        vc.dump()
        so = StringIO()
        vc.traverse(stream=so)
        traverse_str = so.getvalue()
        self.push_dump("in _fetch_songs_on_current_screen: got the traverse string\n{}".format(traverse_str))
        lines = traverse_str.splitlines()
        li_title_key = GoogleMusicApp.LI_TITLE_KEY
        li_subtitle_key = GoogleMusicApp.LI_SUBTITLE_KEY
        song_feat_strs = [lines[idx:idx+2] \
            for idx, line in enumerate(lines[:-1]) if li_title_key in line and li_subtitle_key in lines[idx+1]]

        def str2sec(time_str):
            if len(time_str.split(":")) == 2:
                timeformat = "%M:%S"
                zerostr = "0:0"
            elif len(time_str.split(":")) == 3:
                timeformat = "%H:%M:%S"
                zerostr = "0:0:0"
            else:
                return time_str

            t = datetime.datetime.strptime(time_str, timeformat)
            t0 = datetime.datetime.strptime(zerostr, timeformat)
            return (t - t0).total_seconds()

        song_properties = map( \
            lambda feat: ( \
                    utf8str(feat[0].split(li_title_key)[-1].strip()), str2sec(feat[1].split(li_subtitle_key)[-1].strip()) \
                ), song_feat_strs)
        map(lambda prop: self.push_dump("song_prop: {}".format(prop)), song_properties)
        return song_properties

    def to_control_panel(self):
        if not self.cache_init:
            raise RuntimeError(ERROR_MSG)

        self.device.touch(*self.cache["art_pager_view"]["position"])
        return self.get_state() == GoogleMusicApp.State.CONTROL_PANEL

    def find_song(self, song_title):
        if not self.cache_init:
            raise RuntimeError(ERROR_MSG)

        found = []
        for playcard_title, info in self.cache["playcard"].items():
            if "songs" in info.keys() and song_title in info["songs"].keys():
                found.append((playcard_title, info["songs"][song_title]))

        return found

    def touch_song(self, song):
        if not self.cache_init:
            raise RuntimeError(ERROR_MSG)

        self._drag_up(drag_up_count=song["drag_up_count"])
        self.device.touch(*song["position"])
        return self.is_playing()

    def touch_playcard(self, li_title, idx=0):
        if not self.cache_init:
            raise RuntimeError(ERROR_MSG)

        if not li_title in self.cache["playcard"].keys():
            self.push_dump("the li_title '{}' does not exist".format(li_title))
            return False

        self.device.touch(*self.cache["playcard"][li_title]["position"][idx])
        return True

    def get_state(self):
        vc = ViewClient(self.device, self.serialno)
        so = StringIO()
        vc.traverse(stream=so)
        states = [state for state in GoogleMusicApp.State.ALL_STATES if state["check"](so.getvalue())]
        if len(states) > 1:
            self.push_dump("get_state returns more than one states: [{}]".format( \
                    ", ".join(map(lambda state: "'{}'".format(state["name"]), states)) \
                ))
        if len(states) > 0:
            return states[0]["name"]

        return GoogleMusicApp.State.UNKNOWN

    def to_top(self):
        self.push_dump("to_top called")

        current_state = self.get_state()
        if current_state == GoogleMusicApp.State.TOP_ACTIVITY:
            self.push_dump("return directly")
            return True

        if current_state == GoogleMusicApp.State.UNKNOWN:
            self.push_dump("unknown state, back to home")
            self.device.press("HOME")
            time.sleep(1)
            self.push_dump("start the google music")
            self.device.startActivity(GoogleMusicApp.COMPONENT)
            time.sleep(5)

        current_state = self.get_state()
        if current_state != GoogleMusicApp.State.TOP_ACTIVITY:
            self.push_dump("the state is '{}', press back key".format(current_state))
            self.device.press("BACK")
            time.sleep(1)
        else:
            return True

        current_state = self.get_state()
        if current_state != GoogleMusicApp.State.TOP_ACTIVITY:
            self.push_dump("the state is '{}', press back key".format(current_state))
            self.device.press("BACK")
            time.sleep(1)
        else:
            return True

        return self.get_state() == GoogleMusicApp.State.TOP_ACTIVITY
