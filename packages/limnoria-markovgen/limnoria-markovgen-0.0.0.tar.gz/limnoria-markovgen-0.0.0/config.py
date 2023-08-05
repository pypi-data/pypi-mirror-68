###
# Copyright (c) 2014, Valentin Lorentz
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.conf as conf
import supybot.registry as registry
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Markovgen')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified themself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Markovgen', True)


Markovgen = conf.registerPlugin('Markovgen')
# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(Markovgen, 'someConfigVariableName',
#     registry.Boolean(False, _("""Help for someConfigVariableName.""")))
conf.registerChannelValue(Markovgen, 'enable',
    registry.Boolean(False, _("""Determines whether the plugin is enabled
    on a channel. This defaults to False to avoid useless resources
    consumption.""")))
conf.registerChannelValue(Markovgen, 'probability',
    registry.Probability(0, _("""Determine the probability the bot has to
    reply to a message.""")))
conf.registerChannelValue(Markovgen, 'stripRelayedNick',
    registry.Boolean(True, _("""Determines whether the bot will strip
    strings like <XXX> at the beginning of messages.""")))

conf.registerGroup(Markovgen, 'onNick')
conf.registerChannelValue(Markovgen.onNick, 'probability',
    registry.Probability(0, _("""Determine the probability the bot has to
    reply to a message containing its nick.""")))
conf.registerChannelValue(Markovgen.onNick, 'replaceNick',
    registry.Boolean(True, _("""Determine whether the bot will replace its
    nick by the original author's when replying to a message containing
    its nick.""")))


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
