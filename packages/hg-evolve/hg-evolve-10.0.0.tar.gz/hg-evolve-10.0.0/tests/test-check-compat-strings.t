Enable obsolescence to avoid the warning issue when obsmarkers are found

  $ cat << EOF >> $HGRCPATH
  > [experimental]
  > evolution = all
  > EOF

  $ $TESTDIR/../contrib/check-compat-strings.sh "$TESTDIR/../hgext3rd/" "$RUNTESTDIR/.."
