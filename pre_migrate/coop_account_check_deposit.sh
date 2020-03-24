CURRDB=$1

psql -d $CURRDB -c "delete from ir_ui_view where name = 'account.journal.inherit.form' and arch_fs = 'account_check_deposit/views/account_journal_view.xml';"
