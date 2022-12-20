from typing import Any, Union

from nameko.rpc import rpc
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert

from sciuromorpha_core import model, static as S
from sciuromorpha_core.db.session import SessionFactory
from sciuromorpha_core.exceptions import ArgumentMissingError


class Secret:
    name = "secret"

    @rpc(sensitive_arguments=("secret_meta.data",))
    def put(self, secret_meta: dict) -> int:
        # Insert or update secret data, and return id of the row.

        # Params check.
        # TODO: Use schema or Pydantic to check.
        if (
            secret_meta.get("name", None) is None
            or secret_meta.get("key", None) is None
        ):
            raise ArgumentMissingError(
                "secret_meta need both name&key exists and should not be None."
            )

        with SessionFactory.begin() as session:
            data = secret_meta.get("data", None)
            stmt = insert(model.Secret).values(
                service=secret_meta["name"],
                key=secret_meta["key"],
                data=data,
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=["service", "key"], set_=dict(data=stmt.excluded.data)
            )
            result = session.execute(stmt)

        return result.returned_defaults[0]

    @rpc
    def get_by_id(self, secret_id: int) -> Union[dict, None]:
        with SessionFactory.begin() as session:
            secret = session.get(model.Secret, secret_id, with_for_update=False)

            if secret is None:
                return None

            result = secret.to_dict()

        return result

    @rpc
    def get(self, secret_meta: dict) -> Union[dict, None]:
        # Fetch secret data by service name & secret key.

        with SessionFactory.begin() as session:
            stmt = select(model.Secret).where(
                (model.Secret.service == secret_meta["name"])
                & (model.Secret.key == secret_meta["key"])
            )

            result = session.execute(stmt).scalar()

            if result is None:
                return None

            result = result.to_dict()

        return result

    @rpc
    def delete(self, secret_meta: dict) -> Union[dict, None]:
        # Delete a secret data by service name @ secret key.
        # It will return the content of row if it exist,
        # Otherwise return none.
        with SessionFactory.begin() as session:
            stmt = delete(model.Secret).where(
                (model.Secret.service == secret_meta["name"])
                & (model.Secret.key == secret_meta["key"])
            )

            result = session.execute(stmt).scalar()

            if result is None:
                return result

            return result.returned_defaults
