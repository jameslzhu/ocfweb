from collections import namedtuple

from django.shortcuts import render
from ocflib.misc.validators import host_exists

from ocfweb.caching import cache
from ocfweb.docs.views.servers import Host


class ThingToUpgrade(namedtuple('ThingToUpgrade', (
    'host',
    'upgraded',
    'comments',
    'has_dev',
))):

    @classmethod
    def from_hostname(cls, hostname, upgraded=False, comments=None):
        has_dev = host_exists('dev-' + hostname + '.ocf.berkeley.edu')
        return cls(
            host=Host.from_ldap(hostname),
            upgraded=upgraded,
            has_dev=has_dev,
            comments=comments,
        )


@cache()
def _get_servers():
    return (
        ThingToUpgrade.from_hostname('firestorm'),
        ThingToUpgrade.from_hostname(
            'anthrax',
            comments='maybe move to marathon instead?',
        ),

        # login servers
        ThingToUpgrade.from_hostname(
            'death',
            comments='same time as all login servers',
        ),
        ThingToUpgrade.from_hostname(
            'tsunami',
            comments='same time as all login servers',
        ),
        ThingToUpgrade.from_hostname(
            'werewolves',
            comments=(
                'same time as all login servers; '
                'last time we set up an entirely new server and moved vhosts one-by-one'
            ),
        ),

        ThingToUpgrade.from_hostname('maelstrom'),
        ThingToUpgrade.from_hostname('supernova'),
        ThingToUpgrade.from_hostname('biohazard'),
        ThingToUpgrade.from_hostname('dementors'),
        ThingToUpgrade.from_hostname('flood'),
        ThingToUpgrade.from_hostname('pestilence'),
        ThingToUpgrade.from_hostname(
            'thunder',
            comments='no puppetlabs packages yet',
        ),
        ThingToUpgrade.from_hostname('whiteout'),
        ThingToUpgrade.from_hostname('reaper', upgraded=True),
        ThingToUpgrade.from_hostname('democracy'),
        ThingToUpgrade.from_hostname(
            'zombies',
            comments='in-place (not well puppeted)',
        ),
        ThingToUpgrade.from_hostname(
            'lightning',
            comments='no puppetlabs packages yet',
        ),
        ThingToUpgrade.from_hostname(
            'fallingrocks',
            comments='probably either in-place, or rebuild and manually re-mount /opt/mirrors',
        ),
        ThingToUpgrade.from_hostname('tornado', upgraded=True),

        # mesos servers
        ThingToUpgrade.from_hostname(
            'whirlwind',
            comments='no mesos packages yet',
        ),
        ThingToUpgrade.from_hostname(
            'pileup',
            comments='no mesos packages yet',
        ),
        ThingToUpgrade.from_hostname(
            'monsoon',
            comments='no mesos packages yet',
        ),

        # raspberry pi
        ThingToUpgrade.from_hostname(
            'overheat',
            upgraded=True,
            comments='not puppeted, still needs ocflib and a wrapper around the LED sign',
        ),

        # physical servers
        ThingToUpgrade.from_hostname(
            'riptide',
            upgraded=True,
            comments='it was made this way',
        ),
        ThingToUpgrade.from_hostname(
            'jaws',
            comments='probably in-place, too hard to move stuff around',
        ),
        ThingToUpgrade.from_hostname(
            'pandemic',
            comments='probably in-place, too hard to move stuff around unless installing new drives too',
        ),
        ThingToUpgrade.from_hostname(
            'hal',
            comments='changing soon when installing new drives, so it will be upgraded with replacement',
        ),
    )


def stretch_upgrade(doc, request):
    return render(
        request,
        'docs/stretch-upgrade.html',
        {
            'title': doc.title,
            'servers': _get_servers(),
        },
    )