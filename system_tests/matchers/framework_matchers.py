from expects.matchers import Matcher


class have_activated_slaves(Matcher):
    def __init__(self, expected):
        self._expected = expected

    def _match(self, subject):
        state = subject.get_state()
        return state['activated_slaves'] == self._expected

    def _failure_message(self, subject):
        return 'Expected Mesos with activated slaves {subject!r} to {description}'.format(
            subject=subject.get_state()['activated_slaves'], description=self._description(subject))

class have_framework_name(Matcher):
    def __init__(self, expected):
        self._expected = expected

    def _match(self, subject):
        state = subject.get_state()
        return state['frameworks'][0]['name'] == self._expected

    def _failure_message(self, subject):
        return 'Expected Mesos with frameworks: {subject!r} to {description}'.format(
            subject=subject.get_state()['frameworks'][0]['name'], description=self._description(subject))
