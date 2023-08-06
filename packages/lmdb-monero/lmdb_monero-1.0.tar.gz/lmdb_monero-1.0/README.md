This is a universal Python binding for the LMDB ‘Lightning’ Database.

See [the documentation](https://lmdb.readthedocs.io) for more information.

---

**This is a fork especially for the use with the [Monero project](https://github.com/monero-project/monero).**

It is aimed at interacting with the Monero's blockchain database implemented in lmdb.

The main difference is the use of `dupsort` and `dupfixed` databases, that need custom compare functions by setting `mdb_set_dupsort`.

The implementaton of those compare functions is hardcoded - as can be found in the Monero source code (`/src/blockchain_db/lmdb/db_lmdb.cpp`):
* `mdb_set_dupsort` can compare 32 bit hashes by using `set_dupsort_hash32()`.
    - The sort key is the transaction hash in database `b"block_heights"` (See example below).
    - Monero source code: `int BlockchainLMDB::compare_hash32(const MDB_val *a, const MDB_val *b)`.
* `mdb_set_dupsort` can compare 64 bit integers by using `set_dupsort_uint64()`.
    - The sort key is the block height  in database `b"block_info"`.
    - Monero source code`int BlockchainLMDB::compare_uint64(const MDB_val *a, const MDB_val *b)`.

Some databases require a `dupsort` using `compare_hash32`, some use `compare_uint64`.

Example:
```
env = lmdb.open("/some_path/Monero/lmdb", subdir=True, lock=False, readonly=True, max_dbs=10)
block_heights_db = env.open_db(b"block_heights", integerkey=True, dupsort=True, dupfixed=True)
with env.begin(db=block_heights_db) as txn:                                                                                  
    txn.set_dupsort_hash32(db=block_heights_db)
    if cursor.set_key_dup(key=b'\x00\x00\x00\x00\x00\x00\x00\x00', value=b'\x0b\x1d\x88\xb1\xea\xe9\x8a\xea\xc2\xb7\xe6\xb1V\xdd\\\xac\xc20\xc4\x88\x92E\x84\x85\t\x16\xde\xea\xf2\xac8\xd1*\xfe\x1f\x00\x00\x00\x00\x00')):
        print(cursor.item())
    else:
        print("Nothing found.")
```

The implementation only works with `lmdb.cpython` or `LMDB_FORCE_CPYTHON=1`.

---

### CI State

| Platform | Branch | Status |
| -------- | ------ | ------ |
| UNIX | ``master`` | [![master](https://travis-ci.org/jnwatson/py-lmdb.png?branch=master)](https://travis-ci.org/jnwatson/py-lmdb/branches) |
| Windows | ``master`` | [![master](https://ci.appveyor.com/api/projects/status/cx2sau39bufi3t0t/branch/master?svg=true)](https://ci.appveyor.com/project/NicWatson/py-lmdb/branch/master) |
| UNIX | ``release`` | [![release](https://travis-ci.org/jnwatson/py-lmdb.png?branch=release)](https://travis-ci.org/jnwatson/py-lmdb/branches) |
| Windows | ``release`` | [![release](https://ci.appveyor.com/api/projects/status/cx2sau39bufi3t0t/branch/release?svg=true)](https://ci.appveyor.com/project/NicWatson/py-lmdb/branch/release) |

If you care whether the tests are passing, check out the repository and execute
the tests under your desired target Python release, as the Travis CI build has
a bad habit of breaking due to external factors approximately every 3 months.

# Python Version Support Statement

This project has been around for a while.  Previously, it supported all the way back to before 2.5.  Currently py-lmdb
supports Python 2.7, Python >= 3.4, and pypy.

Python 2.7 is now end-of-life.  If you are still using Python 2.7, you should strongly considering porting to Python
3.

That said, this project will continue to support running on Python 2.7 until Travis CI or Appveyor remove support for
it.

# Sponsored by The Vertex Project

My current employer, [The Vertex Project](https://vertex.link/) is generously sponsoring my time to maintain py-lmdb.
If you like open source and systems programming in Python, check us out.
