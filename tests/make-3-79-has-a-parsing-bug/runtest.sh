#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /tools/make/Regression/make-3-79-has-a-parsing-bug
#   Description: make 3.79 has a parsing bug
#   Author: Michal Kolar <mkolar@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2017 Red Hat, Inc.
#
#   This program is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 2 of
#   the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see http://www.gnu.org/licenses/.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Include Beaker environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

CMD="make"
BIN="$(which $CMD)"
PACKAGE="make"
export PACKAGE="${PACKAGE:-$(rpm -qf --qf='%{name}\n' $BIN)}"

rlJournalStart
  rlPhaseStartSetup
    rlShowRunningKernel
    rlAssertRpm $PACKAGE
    rlRun "TmpDir=\$(mktemp -d)"
    rlRun "cp test.mk $TmpDir"
    rlRun "pushd $TmpDir"
  rlPhaseEnd

  rlPhaseStartTest
    rlRun "touch file.l"
    rlRun "make -f test.mk"
  rlPhaseEnd

  rlPhaseStartCleanup
    rlRun "popd"
    rlRun "rm -r $TmpDir"
  rlPhaseEnd
rlJournalPrintText
rlJournalEnd
