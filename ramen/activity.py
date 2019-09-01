"""ramen.activity -- encapsulating bot actions."""


from vitamins.match.match import Match


class Activity:
    current_step = 0
    done = False
    countdown: int = 0
    tick: 0
    wake_time: float = 0
    subtask: "Activity" = None

    def __init__(self):
        self.stepfunc = self.step_0
        self.status = ""

    def __str__(self):
        name = type(self).__name__
        if self.status:
            return f"{name}:{self.current_step} [{self.status}]"
        else:
            return f"{name}:{self.current_step}"

    def __call__(self):
        if self.done:
            if self.current_step is not None:
                self.when_done()
                self.current_step = None
        elif self.subtask is not None:
            self.before()
            self.subtask()
            self.after()
            if self.subtask.done:
                self.subtask = None
        elif Match.time < self.wake_time:
            self.when_paused()
        elif self.countdown:
            self.when_paused()
            self.countdown -= 1
        else:
            self.before()
            self.stepfunc()
            self.after()

    def step(self, step_name=None, ticks=0, ms=0):
        self.current_step = step_name
        self.sleep(ticks, ms)
        try:
            funcname = f"step_{self.current_step}"
            self.stepfunc = getattr(self, funcname)
        except AttributeError:
            self.done = True
            raise UndefinedStepError(f"{funcname} is not defined.")

    def sleep(self, ticks=0, ms=0):
        """Pause execution for a specified number of ticks or milliseconds. The
        `step_paused` method will be called each tick in place of normal execution.
        """
        self.countdown = max(self.countdown, ticks)
        if ms > 0:
            self.countdown = 0
            self.wake_time = Match.time + ms / 1e3

    def wake(self):
        """Cancel any pause in progress."""
        self.countdown = 0
        self.wake_time = 0.0

    def before(self):
        """This will be called before the current step is executed."""

    def after(self):
        """This will be called after the current step is executed."""

    def when_paused(self):
        """This will be called instead of the current step when `self.step` has been
        invoked with a wait which isn't finished yet."""

    def when_done(self):
        """Called only once, the tick after `self.done` is set to True."""

    def step_0(self):
        pass

    def step_1(self):
        pass

    def step_2(self):
        pass

    def step_3(self):
        pass

    def step_4(self):
        pass

    def step_5(self):
        pass

    def step_6(self):
        pass

    def step_7(self):
        pass

    def step_8(self):
        pass

    def step_9(self):
        pass

    def step_10(self):
        pass


class UndefinedStepError(Exception):
    pass
