import sqlite3
import sys

import pytest

from reader._sqlite_utils import ddl_transaction
from reader._sqlite_utils import HeavyMigration
from reader._sqlite_utils import IntegrityError
from reader._sqlite_utils import require_sqlite_compile_options
from reader._sqlite_utils import require_sqlite_version
from reader._sqlite_utils import RequirementError
from reader._sqlite_utils import SchemaVersionError
from reader._sqlite_utils import wrap_exceptions


def dummy_ddl_transaction(db):
    """Just use a regular transaction."""
    return db


@pytest.mark.parametrize(
    'ddl_transaction',
    [
        # Fails on PyPy3 7.2.0, but not on CPython or PyPy3 7.3.1 (on macOS, at least).
        pytest.param(
            dummy_ddl_transaction,
            marks=pytest.mark.xfail(
                "sys.implementation.name == 'pypy' "
                # For some reason, this doesn't work:
                # https://travis-ci.org/github/lemon24/reader/jobs/684668462
                # "and sys.pypy_version_info <= (7, 2, 0)",
                # strict=True,
            ),
        ),
        ddl_transaction,
    ],
)
def test_ddl_transaction_create_and_insert(ddl_transaction):
    db = sqlite3.connect(':memory:')

    with db:
        db.execute("create table t (a, b);")
        db.execute("insert into t values (1, 2);")

    assert list(db.execute("select * from t order by a;")) == [(1, 2)]

    with pytest.raises(ZeroDivisionError):
        with ddl_transaction(db):
            db.execute("insert into t values (3, 4);")
            db.execute("alter table t add column c;")
            1 / 0

    assert list(db.execute("select * from t order by a;")) == [(1, 2)]


@pytest.mark.parametrize(
    'ddl_transaction',
    [
        # still fails, even on Python 3.6+
        pytest.param(dummy_ddl_transaction, marks=pytest.mark.xfail(strict=True)),
        ddl_transaction,
    ],
)
def test_ddl_transaction_create_only(ddl_transaction):
    db = sqlite3.connect(':memory:')

    assert len(list(db.execute("PRAGMA table_info(t);"))) == 0

    with pytest.raises(ZeroDivisionError):
        with ddl_transaction(db):
            db.execute("create table t (a, b);")
            1 / 0

    assert len(list(db.execute("PRAGMA table_info(t);"))) == 0


class SomeError(Exception):
    pass


def test_wrap_exceptions():
    db = sqlite3.connect('file::memory:?mode=ro', uri=True)

    with pytest.raises(SomeError):
        with wrap_exceptions(SomeError):
            # should raise OperationalError: unable to open database file
            db.execute('create table t (a)')

    # non- "cannot operate on a closed database" ProgrammingError
    with pytest.raises(sqlite3.Error):
        with wrap_exceptions(SomeError):
            db.execute('values (:a)', {})

    # works now
    db.execute('values (1)')

    # doesn't after closing
    db.close()
    with pytest.raises(SomeError):
        with wrap_exceptions(SomeError):
            db.execute('values (1)')


class WeirdError(Exception):
    pass


def create_db_1(db):
    db.execute("CREATE TABLE t (one INTEGER);")


def create_db_2(db):
    db.execute("CREATE TABLE t (one INTEGER, two INTEGER);")


def create_db_2_error(db):
    create_db_2(db)
    raise WeirdError('create')


def update_from_1_to_2(db):
    db.execute("ALTER TABLE t ADD COLUMN two INTEGER;")


def update_from_1_to_2_error(db):
    update_from_1_to_2(db)
    raise WeirdError('update')


def test_migration_create():
    db = sqlite3.connect(':memory:')
    migration = HeavyMigration(create_db_2, 2, {})
    # should call migration.create but not migration.migrations[1]
    migration.migrate(db)
    columns = [r[1] for r in db.execute("PRAGMA table_info(t);")]
    assert columns == ['one', 'two']


def test_migration_create_error():
    db = sqlite3.connect(':memory:')
    migration = HeavyMigration(create_db_2_error, 2, {})
    # should call migration.create but not migration.migrations[1]
    with pytest.raises(WeirdError) as excinfo:
        migration.migrate(db)
    assert excinfo.value.args == ('create',)
    columns = [r[1] for r in db.execute("PRAGMA table_info(t);")]
    assert columns == []


def test_migration_update():
    db = sqlite3.connect(':memory:')
    migration = HeavyMigration(create_db_1, 1, {})
    migration.migrate(db)
    migration = HeavyMigration(create_db_2_error, 2, {1: update_from_1_to_2})
    # should call migration.migrations[1] but not migration.create
    migration.migrate(db)
    columns = [r[1] for r in db.execute("PRAGMA table_info(t);")]
    assert columns == ['one', 'two']


def test_migration_no_update():
    db = sqlite3.connect(':memory:')
    migration = HeavyMigration(create_db_2, 2, {})
    migration.migrate(db)
    migration = HeavyMigration(create_db_2_error, 2, {})
    # should call neither migration.create nor migration.migrations[1]
    migration.migrate(db)
    columns = [r[1] for r in db.execute("PRAGMA table_info(t);")]
    assert columns == ['one', 'two']


def test_migration_update_error():
    db = sqlite3.connect(':memory:')
    migration = HeavyMigration(create_db_1, 1, {})
    migration.migrate(db)
    migration = HeavyMigration(create_db_2_error, 2, {1: update_from_1_to_2_error})
    # should call migration.migrations[1] but not migration.create
    with pytest.raises(WeirdError) as excinfo:
        migration.migrate(db)
    assert excinfo.value.args == ('update',)
    columns = [r[1] for r in db.execute("PRAGMA table_info(t);")]
    assert columns == ['one']


def test_migration_unsupported_old_version():
    db = sqlite3.connect(':memory:')
    migration = HeavyMigration(create_db_1, 1, {})
    migration.migrate(db)
    migration = HeavyMigration(create_db_2, 2, {})
    with pytest.raises(SchemaVersionError) as excinfo:
        migration.migrate(db)
    columns = [r[1] for r in db.execute("PRAGMA table_info(t);")]
    assert columns == ['one']


def test_migration_unsupported_intermediary_version():
    db = sqlite3.connect(':memory:')
    migration = HeavyMigration(create_db_1, 1, {})
    migration.migrate(db)
    migration = HeavyMigration(create_db_2, 3, {1: update_from_1_to_2})
    with pytest.raises(SchemaVersionError) as excinfo:
        migration.migrate(db)
    columns = [r[1] for r in db.execute("PRAGMA table_info(t);")]
    assert columns == ['one']


def test_migration_invalid_version():
    db = sqlite3.connect(':memory:')
    migration = HeavyMigration(create_db_2, 2, {})
    migration.migrate(db)
    migration = HeavyMigration(create_db_1, 1, {})
    with pytest.raises(SchemaVersionError) as excinfo:
        migration.migrate(db)
    columns = [r[1] for r in db.execute("PRAGMA table_info(t);")]
    assert columns == ['one', 'two']


def test_migration_integrity_error():
    def create_db(db):
        db.execute("CREATE TABLE t (one INTEGER PRIMARY KEY);")
        db.execute(
            "CREATE TABLE u (two INTEGER NOT NULL, FOREIGN KEY (two) REFERENCES t(one));"
        )

    def update_from_1_to_2(db):
        db.execute("INSERT INTO u VALUES (1);")

    db = sqlite3.connect(':memory:')
    db.execute("PRAGMA foreign_keys = ON;")

    migration = HeavyMigration(create_db, 1, {})
    migration.migrate(db)
    migration = HeavyMigration(create_db, 2, {1: update_from_1_to_2})
    with pytest.raises(IntegrityError):
        migration.migrate(db)


def test_require_sqlite_version(monkeypatch):
    monkeypatch.setattr('sqlite3.sqlite_version_info', (3, 15, 0))

    with pytest.raises(RequirementError):
        require_sqlite_version((3, 16, 0))

    # shouldn't raise an exception
    require_sqlite_version((3, 15, 0))
    require_sqlite_version((3, 14))


class MockCursor:
    def __init__(self):
        self._execute_args = None
        self._fetchall_rv = None

    def execute(self, *args):
        self._execute_args = args

    def fetchall(self):
        return self._fetchall_rv

    def close(self):
        pass


class MockConnection:
    def __init__(self):
        self._cursor = MockCursor()

    def cursor(self):
        return self._cursor


def test_require_sqlite_compile_options():
    db = MockConnection()
    db._cursor._fetchall_rv = [('ONE',), ('TWO',)]

    with pytest.raises(RequirementError):
        require_sqlite_compile_options(db, ['THREE'])
    with pytest.raises(RequirementError):
        require_sqlite_compile_options(db, ['ONE', 'THREE'])

    # shouldn't raise an exception
    require_sqlite_compile_options(db, ['ONE'])
    require_sqlite_compile_options(db, ['ONE', 'TWO'])
