#-------------------------------------------------------------------------------
#  \file ncbi_alias_table.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.1.0
#  \description
#-------------------------------------------------------------------------------


import sqlite3
from typing import Tuple, Type


from ncbi_taxonomist.db.table import basetable


class NameTable(basetable.BaseTable):

  def __init__(self, database:str):
    super().__init__('names', database=database)

  def create(self, connection:Type[sqlite3.Connection]) -> __qualname__:
    stmt = """CREATE TABLE IF NOT EXISTS {}
              (id           INTEGER PRIMARY KEY,
                taxon_id     INT,
                name         TEXT,
                type         TEXT NULL,
                FOREIGN KEY (taxon_id) REFERENCES taxa(taxon_id) ON DELETE CASCADE,
                UNIQUE(name))""".format(self.name)
    connection.cursor().execute(stmt)
    stmt = """CREATE TRIGGER IF NOT EXISTS delete_names DELETE ON names
              BEGIN DELETE FROM names WHERE taxon_id=old.taxon_id; END;"""
    connection.cursor().execute(stmt)
    self.create_index(connection)
    return self

  def create_index(self, connection:Type[sqlite3.Connection])->None:
    stmt = """CREATE UNIQUE INDEX IF NOT EXISTS {0} ON {1} (name)""".format(self.idx, self.name)
    connection.cursor().execute(stmt)

  def get_rows(self, connection:Type[sqlite3.Connection])->Type[sqlite3.Cursor]:
    return connection.cursor().execute("SELECT taxon_id, name, type FROM {0}".format(self.name))

  def insert(self, connection:Type[sqlite3.Connection], namevalues:Tuple[int, str, str]) -> None:
    stmt = """INSERT OR IGNORE INTO {0} (taxon_id, name, type) VALUES (?,?,?)""".format(self.name)
    connection.cursor().executemany(stmt, namevalues)
    connection.commit()

  def name_to_taxid(self, connection:Type[sqlite3.Connection], name)->Type[sqlite3.Cursor]:
    stmt = """SELECT name, taxon_id FROM names WHERE name=?"""
    return connection.cursor().execute(stmt, (name,))
