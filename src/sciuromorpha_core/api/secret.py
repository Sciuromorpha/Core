from typing import Any, Union

from nameko.rpc import rpc
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from sciuromorpha_core import model, static as S
from sciuromorpha_core.db.session import SessionFactory
from sciuromorpha_core.exceptions import ArgumentMissingError


class Secret:
    name = "secret"

    @rpc
    def put(self, service_meta: dict) -> int:
        # Insert or update secret data, and return id of the row.

        # Params check.
        # TODO: Use schema or Pydantic to check.
        if (
            service_meta.get("name", None) is None
            or service_meta.get("secret_key", None) is None
        ):
            raise ArgumentMissingError(
                "service_meta need both name&secret_key exists and should not be None."
            )

        with SessionFactory.begin() as session:
            data = service_meta.get("secret_data", None)
            stmt = insert(model.Secret).values(
                service=service_meta["name"],
                key=service_meta["secret_key"],
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
    def get(self, service_meta: dict) -> Union[dict, None]:
        # Fetch secret data by service name & secret key.

        with SessionFactory.begin() as session:
            stmt = select(model.Secret).where(
                (model.Secret.service == service_meta["name"])
                & (model.Secret.key == service_meta["secret_key"])
            )

            result = session.execute(stmt).scalar()

            if result is None:
                return None

            result = result.to_dict()

        return result
