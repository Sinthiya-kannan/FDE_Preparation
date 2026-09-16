import sqlite3
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import text

from database.connection import engine
from models.customer import Customer
from models.user import User
from models.invitation import Invitation


SQLITE_DB = "fde_customer.db"


def parse_datetime(value):
    if not value:
        return None

    return datetime.fromisoformat(value)


def migrate():
    sqlite_conn = sqlite3.connect(SQLITE_DB)
    sqlite_conn.row_factory = sqlite3.Row

    with Session(engine) as db:

        # Safety: remove existing target data.
        # invitations first because it references users.
        db.query(Invitation).delete()
        db.query(User).delete()
        db.query(Customer).delete()
        db.commit()

        # -------------------------
        # Customers
        # -------------------------
        customer_rows = sqlite_conn.execute(
            """
            SELECT
                customer_id,
                customer_name,
                domain,
                website,
                status,
                rejection_reason,
                created_at
            FROM customers
            ORDER BY customer_id
            """
        ).fetchall()

        for row in customer_rows:
            customer = Customer(
                customer_id=row["customer_id"],
                customer_name=row["customer_name"],
                domain=row["domain"],
                website=row["website"],
                status=row["status"],
                rejection_reason=row["rejection_reason"],
                created_at=parse_datetime(row["created_at"])
            )

            db.add(customer)

        db.commit()

        # -------------------------
        # Users
        # -------------------------
        user_rows = sqlite_conn.execute(
            """
            SELECT
                user_id,
                customer_id,
                first_name,
                last_name,
                email,
                phone,
                password_hash,
                role,
                status,
                created_at
            FROM users
            ORDER BY user_id
            """
        ).fetchall()

        for row in user_rows:
            user = User(
                user_id=row["user_id"],
                customer_id=row["customer_id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                phone=row["phone"],
                password_hash=row["password_hash"],
                role=row["role"],
                status=row["status"],
                created_at=parse_datetime(row["created_at"])
            )

            db.add(user)

        db.commit()

        # -------------------------
        # Invitations
        # -------------------------
        invitation_rows = sqlite_conn.execute(
            """
            SELECT
                invitation_id,
                user_id,
                token,
                status,
                sent_at,
                expires_at,
                accepted_at,
                created_at
            FROM invitations
            ORDER BY invitation_id
            """
        ).fetchall()

        for row in invitation_rows:
            invitation = Invitation(
                invitation_id=row["invitation_id"],
                user_id=row["user_id"],
                token=row["token"],
                status=row["status"],
                sent_at=parse_datetime(row["sent_at"]),
                expires_at=parse_datetime(row["expires_at"]),
                accepted_at=parse_datetime(row["accepted_at"]),
                created_at=parse_datetime(row["created_at"])
            )

            db.add(invitation)

        db.commit()

        # Reset PostgreSQL sequences because we inserted explicit IDs.
        db.execute(
    text("""
        SELECT setval(
            pg_get_serial_sequence('customers', 'customer_id'),
            COALESCE((SELECT MAX(customer_id) FROM customers), 1)
        )
    """)
)
        db.execute(
            text("""
            SELECT setval(
                pg_get_serial_sequence('users', 'user_id'),
                COALESCE((SELECT MAX(user_id) FROM users), 1)
            )
            """)
        )

        db.execute(
             text("""
            SELECT setval(
                pg_get_serial_sequence('invitations', 'invitation_id'),
                COALESCE((SELECT MAX(invitation_id) FROM invitations), 1)
            )
            
        """)
        )

        db.commit()

    sqlite_conn.close()

    print("SQLite → PostgreSQL migration completed successfully")


if __name__ == "__main__":
    migrate()