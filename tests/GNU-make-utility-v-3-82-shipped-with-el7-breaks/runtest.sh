#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /tools/make/Regression/GNU-make-utility-v-3-82-shipped-with-el7-breaks
#   Description: Test for BZ#1323206 (GNU make utility v.3.82 shipped with el7 breaks)
#   Author: Michal Kolar <mkolar@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2016 Red Hat, Inc.
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
. /usr/bin/rhts-environment.sh || exit 1
. /usr/share/beakerlib/beakerlib.sh || exit 1

CMD="make"
PACKAGE="make"
BIN="$(which $CMD)"
export PACKAGE="${PACKAGE:-$(rpm -qf --qf='%{name}\n' $BIN)}"

rlJournalStart
  rlPhaseStartSetup
    rlShowRunningKernel
    rlAssertRpm $PACKAGE
    rlRun "TmpDir=\$(mktemp -d)"
    rlRun "cp test.mk golden.output $TmpDir"
    rlRun "pushd $TmpDir"
  rlPhaseEnd

  rlPhaseStartTest
    rlRun "make -f test.mk test TEST=false >stdout"
    rlRun "sed -i -e '/Entering directory/d' -e '/Leaving directory/d' stdout"
    rlRun "diff golden.output stdout"
  rlPhaseEnd

  rlPhaseStartCleanup
    rlRun "popd"
    rlRun "rm -r $TmpDir"
  rlPhaseEnd
rlJournalPrintText
rlJournalEnd

