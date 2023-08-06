from rigidanalytics_tracker import Tracker


def start(sender, **extra):
    from flask import request

    tracker = sender.extensions["rigidanalytics_tracker"]
    tracker.start(request)
    tracker.set_intercepted_data("view_name", request.endpoint)


def stop(sender, **extra):
    sender.extensions["rigidanalytics_tracker"].stop(extra.get("response"))


class FlaskTracker(Tracker):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.extensions = getattr(app, "extensions", {})
        app.extensions["rigidanalytics_tracker"] = self
        self.app = app
        self.init_tracker()

    def init_tracker(self):
        from flask import signals

        if signals.signals_available and not self.is_disabled():
            self.init_signals()
        super(FlaskTracker, self).init_tracker()

    def init_signals(self):
        self.init_request_started()
        self.init_request_finished()

    def init_request_started(self):
        from flask import request_started

        request_started.connect(start, sender=self.app)

    def init_request_finished(self):
        from flask import request_finished

        request_finished.connect(stop, sender=self.app)

    @property
    def app_settings(self):
        return self.app.config

    def get_app_setting(self, setting, default=None):
        return self.app_settings.get(setting, default)

    def get_headers(self):
        return self.request.headers

    def format_header(self, header):
        return "HTTP_{}".format(header).upper().replace("-", "_")

    def extract_request_headers(self):
        return {self.format_header(k): v for k, v in self.get_headers()}

    def get_full_url(self):
        return self.request.url

    def get_session_id(self):
        return self.request.cookies.get('sessionid')

    def get_response_data(self):
        return {
            "status_code": self.response.status_code,
            "cookies": self.request.cookies,
        }
