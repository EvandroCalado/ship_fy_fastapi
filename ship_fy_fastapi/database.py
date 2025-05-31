import sqlite3

from .schemas import ShipmentCreate, ShipmentUpdate


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('shipments.db', check_same_thread=False)
        self.cur = self.conn.cursor()

        self.create_table('shipment')

    def create_table(self, name: str):
        self.cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                content TEXT,
                weight REAL,
                destination INTEGER,
                status TEXT
            )
         """
        )

    def create(self, shipment: ShipmentCreate) -> dict[str, any]:
        self.cur.execute(
            """
            INSERT INTO shipment (
                         content,
                         weight,
                         destination,
                         status
                         ) VALUES (
                            :content,
                            :weight,
                            :destination,
                            :status
                        )
                    """,
            {
                **shipment.model_dump(),
                'status': 'placed',
            },
        )
        self.conn.commit()

        shipment_id = self.cur.lastrowid

        return self.get(shipment_id)

    def get(self, id: int):
        result = self.cur.execute(
            """
            SELECT * FROM shipment
            WHERE id = ?
        """,
            (id,),
        ).fetchone()

        return (
            {
                'id': result[0],
                'content': result[1],
                'weight': result[2],
                'destination': result[3],
                'status': result[4],
            }
            if result
            else None
        )

    def update(self, id: int, shipment: ShipmentUpdate):
        current = self.get(id)
        if not current:
            return None

        update_data = shipment.model_dump(exclude_unset=True)
        merged = {**current, **update_data}

        self.cur.execute(
            """
            UPDATE shipment
            SET content = :content,
                weight = :weight,
                destination = :destination,
                status = :status
            WHERE id = :id
        """,
            ({
                'id': id,
                'content': merged['content'],
                'weight': merged['weight'],
                'destination': merged['destination'],
                'status': merged['status'],
            }),
        )
        self.conn.commit()

        return self.get(id)

    def delete(self, id: int):
        self.cur.execute(
            """
            DELETE FROM shipment
            WHERE id = ?
        """,
            (id,),
        )
        self.conn.commit()

    def delete_all(self):
        self.cur.execute(
            """
            DELETE FROM shipment
        """,
        )
        self.conn.commit()

    def close(self):
        self.conn.close()
